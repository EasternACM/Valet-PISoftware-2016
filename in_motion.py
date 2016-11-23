import cv2
import numpy as np

contours_min_area = 18000
frame_size = (1500, 900)


def capture(input = 0):
    cap = cv2.VideoCapture(input)
    previous_frame = current_frame = next_frame = None
    d1 = d2 = result = None

    while True:
        success, frame = cap.read()

        if not success:
            return
            #throw exception

        frame = cv2.resize(frame, frame_size)

        #fill the frame variables before trying to find movement
        if current_frame == None:
            current_frame = frame
            continue
        elif next_frame == None:
            next_frame = current_frame
            current_frame = frame
            continue
        else:
            previous_frame = next_frame
            next_frame = current_frame
            current_frame = frame

        #greyed_frame = cv2.cvtColor(frame, cv2.COLOR_BGRGRAY)

        d1 = cv2.absdiff(previous_frame, next_frame)
        d2 = cv2.absdiff(current_frame, next_frame)
        result = cv2.bitwise_and(d1, d2)

        result = cv2.threshold(result, 35, 255, cv2.THRESH_BINARY)[1]q

        cv2.imshow('frame', result)

        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break  # q to exit feedq

capture()