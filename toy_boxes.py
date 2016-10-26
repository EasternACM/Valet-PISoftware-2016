# /usr/bin/python
import numpy as np
import cv2

def calc_angle(p, c): # not really being used
    angle = np.absolute(np.arctan2(c[1]-p[1],c[0]-p[0]))
    angle = np.rad2deg(angle)
    return angle

def avg_list(list): #not really being used
    if len(list) == 0:
        return 0
    sum = 0
    for i in range(len(list)):
        sum += list[i]
    if 90 < sum / len(list) < 275:
        return (-1)
    else:
        return (1)

def watch_camera(name=0):
    cap = cv2.VideoCapture(0)
    vector_field = []
    movements = []
    min_area = 15000
    lastFrame = prev_center = None
    moving_object_in_view = False
    frame_size = (1500, 900)

    while(True): #main loop
        (success, frame) = cap.read()

        if not success:
            break

        frame = cv2.resize(frame, frame_size) #resize the frame

        #blue the image and convert to grayscale
        grayedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayFrame = cv2.GaussianBlur(grayedFrame, (21, 21), 30) #TODO remove magic numbers

        if lastFrame is None:
            lastFrame = grayedFrame
            continue # get delta on next loop

        #get the delta of the image
        frameDelta = cv2.absdiff(lastFrame, grayedFrame)
        tresh = cv2.erode(frameDelta.copy(), None, iterations=10)
        thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1] #TODO remove magic numbers

        #clear visual noise step goes here

        (_, contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        skipped = True
        for c in contours:
            #filter out small contours
            moving_object_in_view = True
            skipped = False
            if cv2.contourArea(c) < min_area:
                continue

            (x,y,w,h) = cv2.boundingRect(c) #generating too many of these

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #TODO remove magic numbers
            current = (x, y)
            if prev_center is not None:
                vector_field.append(calc_angle(prev_center, current))
            else:
                prev_center = current

        if moving_object_in_view and skipped:
            movements.append(avg_list(vector_field))
            vector_field = []
            moving_object_in_view = False
            prev_center = None

        cv2.imshow('frame', frame)

        lastFrame = grayedFrame
        if( cv2.waitKey(1) & 0xFF == ord('q')):
            break #q to exit feed
    cap.release()
    cv2.destroyAllWindows()
    if moving_object_in_view:
        movements.append(avg_list(vector_field))
    return movements
watch_camera()