from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from io import StringIO
import io
import base64
from PIL import Image
import imutils
import numpy as np
import cv2

import dlib
from scipy.spatial import distance as dist

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) #remove constant logs and set to error only

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

global COUNTER
global TOTAL
COUNTER=0
TOTAL=0

def eye_aspect_ratio(eye):
    # compute the euclidean distance between the vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])

    # compute the EAR
    ear = (A + B) / (2 * C)
    return ear

# to detect the facial region
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('second.html')

# @socketio.on('catch-frame')
# def catch_frame(data):
#     ## getting the data frames
#     ## do some processing
#     ## send it back to client
#     emit('response_back', data)  ## ??

@socketio.on('image')
def image(data_image):
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
            print(ear_avg) #blinked!
            
        # if ear_avg < EYE_AR_THRESH:
        #     COUNTER += 1
        # else:
        #     if COUNTER >= EYE_AR_CONSEC_FRAMES:
        #         TOTAL += 1
        #         print("{} Eye blinked {}".format(TOTAL, ear_avg))
        #     COUNTER = 0

    imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)

    # # Process the image frame
    # frame = imutils.resize(frame, width=700)
    # frame = cv2.flip(frame, 1)
    # imgencode = cv2.imencode('.jpg', frame)[1]

    # # base64 encode
    # stringData = base64.b64encode(imgencode).decode('utf-8')
    # b64_src = 'data:image/jpg;base64,'
    # stringData = b64_src + stringData

    # # emit the frame back
    # emit('response_back', stringData)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')