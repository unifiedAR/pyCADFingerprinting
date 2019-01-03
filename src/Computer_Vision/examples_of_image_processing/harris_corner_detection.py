#!/usr/bin/env python
import cv2
import numpy as np

# Some code adapted from: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html

"""if you want to see the pixels on a black background, set rect = -1; otherwise,
set it equal to 0"""
rect = -1
"""to display the accurate points (centroids of the raw data points), set =True.
Set this =False if you want to see all of the points, set =False"""
display_accurate = True
"""threshold is a value that by default is set to 0.01 - try playing around with
different values to see how that changes the results"""
threshold = 0.01

def display_webcam():
    # capturing video from camera, storing in 'cap'. 0 selects the camera

    cap = cv2.VideoCapture(0)
    n=0
    while True:

        # frame gets the next frame in the camera via cap
        # ret is a boolean for success of capturing frame
        ret, frame = cap.read()

        src = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        src = np.float32(src)
        cv2.rectangle(frame, (0,0), (frame.shape[1],frame.shape[0]), (0,0,0), rect)

        #find the corners with cv2.cornerHarris(img, blockSize, ksize, k[, dst[, borderType]]) -> dst
        #which calculates a 2x2 gradient covariance matrix M^{(x,y)} over a blockSizexblockSize neighborhood
        dst = cv2.cornerHarris(src,2,3,0.04)
        dst = cv2.dilate(dst,None)
        ret, dst = cv2.threshold(dst,threshold*dst.max(),255,0)
        dst = np.uint8(dst)

        ################# find centroids
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

        # define the criteria to stop and refine the corners
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(src,np.float32(centroids),(5,5),(-1,-1),criteria)

        # Now draw them
        res = np.hstack((centroids,corners))
        res = np.int0(res)
        #################

        # check for values that could be outside of the frame and set them to
        # the bottom right corner
        num_points = len(res[:,3])
        for i in range(num_points):
            num = res[i,3]
            if num >= frame.shape[0]:
                diff = num - frame.shape[0] + 1
                res[i,3] = num - diff
        for i in range(num_points):
            num = res[i,2]
            if num >= frame.shape[1]:
                diff = num - frame.shape[1] + 1
                res[i,2] = num - diff

        points = []
        for i in range(num_points):
            # turn the ndarray into a list of vectors for the points
            points.append((res[i,2], res[i,3]))
        print(points)

        # set the color of the corners detected in the image
        if display_accurate == True:
            frame[res[:,3],res[:,2]] = [0,255,0]
        if display_accurate == False:
            frame[dst>0.01*dst.max()]=[0,0,255]

        # keep track of the number of frames
        n += 1
        print(n)

        # display the image
        cv2.imshow('This is a window!!', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('An error occured')
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_webcam()
