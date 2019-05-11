#!/usr/bin/env python
import cv2
import numpy as np

"""if you want to see the pixels on a black background, set rect = -1; otherwise,
set it equal to 0"""
rect = -1


def display_webcam():
    # capturing video from camera, storing in 'cap'. 0 selects the camera

    cap = cv2.VideoCapture(0)
    n=0
    while True:

        # frame gets the next frame in the camera via cap
        # ret is a boolean for success of capturing frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
        corners = np.int0(corners)
        cv2.rectangle(frame, (0,0), (frame.shape[1],frame.shape[0]), (0,0,0), rect)

        for i in corners:
            x,y = i.ravel()
            cv2.circle(frame,(x,y),2,255,-1)

        # keep track of the number of frames
        n += 1
        print(n)
        print(corners)

        # display the image
        cv2.imshow('This is a window!!', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('An error occured')
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_webcam()
