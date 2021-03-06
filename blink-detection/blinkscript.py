import numpy as np
import cv2
import dlib
from scipy.spatial import distance as dist
import random

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

COUNTER = 0
TOTAL = 0

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

def get_random_box(frame):
    height = random.randint(0, frame.shape[0])
    width = random.randint(0, frame.shape[1])

    height = 250
    width = 100

    d_height = 100
    d_width = 70

    return (width, height), (width+d_width, height+d_height), d_height*d_width

def offset_text(start):
    return (start[0], start[1] - 10)

bounding = True
start, end, area = None, None, None

# capture video from live video stream
cap = cv2.VideoCapture(0)
while True:
    # get the frame
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    if ret:
        # convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        for rect in rects:

            x = rect.left()
            y = rect.top()
            x1 = rect.right()
            y1 = rect.bottom()

            if (bounding): 
                if not start:
                    start, end, area = get_random_box(frame)
                else:
                    x_diff = abs(x-start[0])
                    y_diff = abs(y-start[1])
                    area_diff = abs(area- (x1-x) * (y1-y) )

                    print("X: {}".format(x_diff))
                    print("Y: {}".format(y_diff))
                    print("Area: {}".format(area_diff))

                    if x_diff < 10 and y_diff < 10 and area_diff < 5000:
                        bounding = False
            

            #print( (x1-x) * (y1-y))

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

            #print(ear_avg)
            if ear_avg < EYE_AR_THRESH:
                COUNTER += 1
            else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1
                    print("{} Eye blinked {}".format(TOTAL, ear_avg))
                COUNTER = 0

            cv2.putText(frame, "Blinks{}".format(TOTAL), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 1)
            cv2.putText(frame, "EAR {}".format(ear_avg), (10, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 255), 1)
        if start:
            cv2.rectangle(frame, start, end, (0, 0, 255), 2)
            cv2.putText(frame, "Position face here!", offset_text(start), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 1)
        
        cv2.imshow("Winks Found", frame)
        key = cv2.waitKey(1) & 0xFF
        # When key 'Q' is pressed, exit
        if key is ord('q'):
            break

# release all resources
cap.release()
# destroy all windows
cv2.destroyAllWindows()