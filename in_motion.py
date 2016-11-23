import cv2
import numpy as np

contours_min_area = 18000
frame_size = (1200, 800)


def capture(input = 0):
    dilation_kernal = np.ones((26,26), np.uint8)

    cap = cv2.VideoCapture(input)
    previous_frame = current_frame = next_frame = None
    d1 = d2 = result = None

    while True:
        success, original = cap.read()

        if not success:
            return
            #throw exception

        original = cv2.resize(original, frame_size)
        frame = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

        frame = cv2.GaussianBlur(frame, (21, 21), 30)
        frame = cv2.dilate(frame, dilation_kernal, iterations=3)

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

        d1 = cv2.absdiff(previous_frame, next_frame)
        d2 = cv2.absdiff(current_frame, next_frame)
        andResult = result = cv2.bitwise_and(d1, d2)

        andResult = result = cv2.threshold(result, 5, 255, cv2.THRESH_BINARY)[1]

        andResult = cv2.dilate(result, dilation_kernal, iterations=1)

        (_, contours, _) = cv2.findContours(result.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #function is destructive, copy frame

        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)  # generating too many of these
            cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw rectangle TODO remove magic numbers

        cv2.imshow('frame', andResult)

        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break  # q to exit feedq

capture()