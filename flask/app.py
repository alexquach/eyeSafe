from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO, emit
from io import StringIO
import io
import base64
from PIL import Image
import imutils
import numpy as np
import cv2
from datetime import datetime, timedelta
import random

import dlib
from scipy.spatial import distance as dist

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) #remove constant logs and set to error only


#### Bug Fix: ValueError(Too many packets in payload)
from engineio.payload import Payload
Payload.max_decode_packets = 500
#### --- bug fix --- ###

JAWLINE_POINTS = list(range(0, 17))
RIGHT_EYEBROW_POINTS = list(range(17, 22))
LEFT_EYEBROW_POINTS = list(range(22, 27))
NOSE_POINTS = list(range(27, 36))
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
MOUTH_OUTLINE_POINTS = list(range(48, 61))
MOUTH_INNER_POINTS = list(range(61, 68))

EYE_AR_THRESH = 0.22
EYE_AR_CONSEC_FRAMES = 3
EAR_AVG = 0

COUNTER=0
TOTAL=[]
BOX_CHALLENGE = False
START, END, AREA = None, None, None

def eye_aspect_ratio(eye):
    # compute the euclidean distance between the vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])

    # compute the EAR
    ear = (A + B) / (2 * C)
    return ear

def gt(dt_str):
    """ Converts str to datetime """
    dt, _, us = dt_str.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z"), 10)
    return dt + timedelta(microseconds=us)

def filter_space_between(arr, us=500000):
    """ Ensures theres at least `us` microseconds between array items """
    i = 0
    init = None
    while len(arr) > i:
        if init is None:
            init = arr[i]
            i += 1
            continue
        if arr[i] - init < timedelta(microseconds=us):
            del arr[i]
        else:
            init = arr[i]
            i += 1
    return arr

def filter_duplicates():
    global TOTAL
    
    converted = list(map(gt, TOTAL))
    TOTAL = filter_space_between(converted)
    TOTAL = list(map(datetime.isoformat, TOTAL))
        
def get_random_box(frame):
    height = random.randint(0, frame.shape[0])
    width = random.randint(0, frame.shape[1])

    height = 250
    width = 100

    d_height = 100
    d_width = 70

    return (width, height), (width+d_width, height+d_height), d_height*d_width


# to detect the facial region
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/poll', methods=['GET'])
def poll():
    global TOTAL
    filter_duplicates()
    print(TOTAL)
    response = {"count": len(TOTAL), "sentTime": datetime.now().isoformat(), "datetime_array": TOTAL}

    TOTAL = []
    return jsonify(response)

@app.route('/getbox', methods=['GET'])
def getbox():
    global BOX_CHALLENGE

    return jsonify({'box_challenge_status': BOX_CHALLENGE})

@app.route('/setbox', methods=['GET'])
def setbox():
    global BOX_CHALLENGE
    BOX_CHALLENGE = True

    return jsonify({'set_box_challenge': BOX_CHALLENGE})

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('second.html')

@socketio.on('image')
def image(data_image):
    global COUNTER
    global TOTAL
    global BOX_CHALLENGE
    global START
    global END
    global AREA

    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)
    for rect in rects:
        x = rect.left()
        y = rect.top()
        x1 = rect.right()
        y1 = rect.bottom()

        if (BOX_CHALLENGE): 
            if not START:
                START, END, AREA = get_random_box(frame)
            else:
                x_diff = abs(x-START[0])
                y_diff = abs(y-START[1])
                area_diff = abs(AREA- (x1-x) * (y1-y) )

                print("X: {}".format(x_diff))
                print("Y: {}".format(y_diff))
                print("Area: {}".format(area_diff))

                if x_diff < 10 and y_diff < 10 and area_diff < 5000:
                    BOX_CHALLENGE = False
                    START, END, AREA = None, None, None


        # get the facial landmarks
        landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, rect).parts()])
        # get the left eye landmarks
        left_eye = landmarks[LEFT_EYE_POINTS]
        # get the right eye landmarks
        right_eye = landmarks[RIGHT_EYE_POINTS]
        # draw contours on the eyes
        left_eye_hull = cv2.convexHull(left_eye)
        right_eye_hull = cv2.convexHull(right_eye)
        cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1) # (image, [contour], all_contours, color, thickness)
        cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
        # compute the EAR for the left eye
        ear_left = eye_aspect_ratio(left_eye)
        # compute the EAR for the right eye
        ear_right = eye_aspect_ratio(right_eye)
        # compute the average EAR
        ear_avg = (ear_left + ear_right) / 2.0
        # detect the eye blink
        
        if ear_avg < EYE_AR_THRESH:
            TOTAL.append(datetime.now().isoformat())
            print(ear_avg) #blinked!
            
        # if ear_avg < EYE_AR_THRESH:
        #     COUNTER += 1
        # else:
        #     if COUNTER >= EYE_AR_CONSEC_FRAMES:
        #         TOTAL += 1
        #         print("{} Eye blinked {}".format(TOTAL, ear_avg))
        #     COUNTER = 0
    if START:
        cv2.rectangle(frame, START, END, (0, 0, 255), 2)
    imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')