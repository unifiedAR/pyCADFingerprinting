#!/usr/bin/env python
import cv2
import numpy as np

def display_webcam():
    # capturing video from camera, storing in 'cap'. 0 selects the camera

    cap = cv2.VideoCapture(0)
    n=0
    while True:

        # frame gets the next frame in the camera via cap
        # ret is a boolean for success of capturing frame
        ret, frame = cap.read()

        edges = cv2.Canny(frame,100,200)

        n += 1
        print(n)

        # display the image
        cv2.imshow('This is a window!!', edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('An error occured')
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_webcam()
