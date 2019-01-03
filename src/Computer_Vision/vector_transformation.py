#!/usr/bin/env python
import cv2
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

"""
This program computes Canny edge detection on a single frame captured by the
camera. Only the edges inside the bounding box (displayed) are considered, so
that an object can be placed in the bounding box and only the object is
considered; the program selects the topmost, bottommost, leftmost, and rightmost
points of the edges (ideally of the object) within the bounding box. The program
then passes those points to a Lucas Kanade function which tracks their movement
in the frames.

Intention: find reference points that are projections of points on the object
into two dimensions. The transformation of these point vectors can then be
tracked as the object is moved in real time.

Limitations:
- Noise is a significant hinderance in being able to accurately
select the points
- Tracking the transofmation of the points/vectors has not been done yet, although
if it were it would be a straightforward implementation of matrix transformation
of vectors in a 2D plane
- If these transformations are accurately obtained, it isn't clear how these 2D
transformations translate into transformations of the 3D model of the object.
"""
#VIDEO_SRC = 'IMG_5445.MOV' # enter 0 (as an integer) for webcam
VIDEO_SRC = 'test_for_object_orientation.mov' # enter 0 (as an integer) for webcam
DELAY_AT_START = 3 # time steps
DENOISING_PARAM = 20 # 10 is recommended by OpenCV, but the higher the better
BOUNDING_BOX_PROPORTION = 7 # for a number n, the program divides the x and y
# dimensions of the image with n lines into n+1 equal parts respectively, and
# selects the n-1 parts for each dimension that are in the middle; number should
# be odd and >= 3

def display_webcam():
    n = 0
    cap = cv2.VideoCapture(VIDEO_SRC)
    while n < DELAY_AT_START:

        # frame gets the next frame in the camera via cap
        # ret is a boolean for success of capturing frame
        ret, frame = cap.read()

        denoise = cv2.fastNlMeansDenoisingColored(frame,None,DENOISING_PARAM,DENOISING_PARAM,7,21)
        edges = cv2.Canny(denoise,100,200)

        cv2.rectangle(edges, (bbtl[0], bbtl[1]), (bbbr[0], bbbr[1]), 255, 1)

        cv2.imshow('Line up object in box', edges)

        n += 1
        print('Ready to capture frame in:', 100 * n / DELAY_AT_START, '%')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('An error occured')
            break

    cap.release()
    cv2.destroyAllWindows()

def extremma(edges_in_box):
    # select the topmost pixel
    topmost_y = edges_in_box[0][1]
    topmost_x = edges_in_box[0][0]
    for i in range(len(edges_in_box)):
        if edges_in_box[i][1] > topmost_y:
            topmost_y = edges_in_box[i][1]
            topmost_x = edges_in_box[i][0]
        else:
            continue
    topmost = (topmost_x, topmost_y)

    bottommost_y = edges_in_box[0][1]
    bottommost_x = edges_in_box[0][0]
    for i in range(len(edges_in_box)):
        if edges_in_box[i][1] < bottommost_y:
            bottommost_y = edges_in_box[i][1]
            bottommost_x = edges_in_box[i][0]
        else:
            continue
    bottommost = (bottommost_x, bottommost_y)

    leftmost_x = edges_in_box[0][0]
    leftmost_y = edges_in_box[0][1]
    for i in range(len(edges_in_box)):
        if edges_in_box[i][0] < leftmost_x:
            leftmost_x = edges_in_box[i][0]
            leftmost_y = edges_in_box[i][1]
        else:
            continue
    leftmost = (leftmost_x, leftmost_y)

    rightmost_x = edges_in_box[0][0]
    rightmost_y = edges_in_box[0][1]
    for i in range(len(edges_in_box)):
        if edges_in_box[i][0] > rightmost_x:
            rightmost_x = edges_in_box[i][0]
            rightmost_y = edges_in_box[i][1]
        else:
            continue
    rightmost = (rightmost_x, rightmost_y)

    return topmost, bottommost, leftmost, rightmost

def edges_filter(edges):
    # currently, the edges are just pixels in an image; this pulls the
    # coordinates of those edges out of the image
    x_index = edges.shape[0] - 1
    y_index = edges.shape[1] - 1
    edge_pixels = []
    for i in range(x_index):
        for j in range(y_index):
            if edges[i][j] != 0:
                edge_pixels.append((i, j))

    # filter out edges that are not in the bounding box
    edges_in_box = []
    for edge in edge_pixels:
        if edge[0] > bbtl[1] and edge[0] < bbbr[1] and edge[1] > bbtl[0] and edge[1] < bbbr[0]:
            edges_in_box.append((edge[1],edge[0]))

    return edges_in_box

def initialize_points():
    # capturing video from camera, storing in 'cap'. 0 selects the camera
    n = 0
    cap = cv2.VideoCapture(VIDEO_SRC)

    # frame gets the next frame in the camera via cap
    # ret is a boolean for success of capturing frame
    ret, frame = cap.read()

    # edges is an image that the cv2.Canny function outputs - only shows edges
    denoise = cv2.fastNlMeansDenoisingColored(frame,None,DENOISING_PARAM,DENOISING_PARAM,7,21)
    edges = cv2.Canny(denoise,100,200)

    edges_in_box = edges_filter(edges)

    cap.release()
    cv2.destroyAllWindows()

    topmost, bottommost, leftmost, rightmost = extremma(edges_in_box)
    return topmost, bottommost, leftmost, rightmost

def track_vectors(topmost, bottommost, leftmost, rightmost):
    n = 0

    cap = cv2.VideoCapture(VIDEO_SRC)
    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                           qualityLevel = 0.3,
                           minDistance = 7,
                           blockSize = 7 )
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                      maxLevel = 2,
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    ret, old_frame = cap.read()
    prev_frame_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    ret, frame = cap.read()

    # organize the 4 points to track in a format readable by the point tracker
    p0 = np.ndarray((4,1,2,), dtype = np.float32)
    index = 0
    for pixel in topmost, bottommost, leftmost, rightmost:
        p0[index][0][0] = np.float32(pixel[0])
        p0[index][0][1] = np.float32(pixel[1])
        index += 1


    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)
    distances = pd.DataFrame(columns = ['Blue Vector', 'Green Vector', 'Red Vector'])
    vectors_list = []
    font = cv2.FONT_HERSHEY_COMPLEX
    while n < 300:
        ret,frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # calculate optical flow
        ########
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_frame_gray, frame_gray, p0, None, **lk_params)
        ########
        # Select good points
        vectors = p1[st==1]

        img = cv2.add(frame,mask)
        distance_list = []
        # draw the points as vectors referenced to the point: vectors[0]
        # add the length of the vectors to a dataframe
        for i in range(1,4):
            cv2.line(img, (vectors[0][0], vectors[0][1]), (vectors[i][0],vectors[i][1]), colors[i-1], 3)
            x_squared = (vectors[0][0] - vectors[i][0])**2
            y_squared = (vectors[0][1] - vectors[i][1])**2
            pythag_dist = math.sqrt(x_squared + y_squared)
            print(vectors[i][0], vectors[0][0], vectors[i][1], vectors[0][1])
            print(pythag_dist)
            distance_list.append(pythag_dist)
            # display the distances of the lines above the lines
            cv2.putText(img,
                        'Length: {} pixels'.format(round(pythag_dist, 0)),
                        (vectors[i][0],vectors[i][1]),
                        font,
                        0.5,
                        colors[i-1],
                        1
                        )
        # add the distances to the dataframe indexed by frame n - used for plotting
        distances.loc[n] = distance_list
        # log the coordinates in a list
        vectors_list.append(vectors)

        # display the image
        cv2.imshow('frame1',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # Now update the previous frame and previous points
        prev_frame_gray = frame_gray.copy()
        p0 = vectors.reshape(-1,1,2)

        # update the frame number
        print(n)
        n += 1

    cv2.destroyAllWindows()
    cap.release()

    return distances, vectors_list


if __name__ == "__main__":
    cap = cv2.VideoCapture(VIDEO_SRC)
    ret, frame = cap.read()
    img_dim = frame.shape
    colors = ((255,0,0),(0,255,0),(0,0,255))

    bbp = BOUNDING_BOX_PROPORTION
    # the boudning box is the box in which the program will look for topmost
    # and bottommost points to create the vectors.
    # bbtl stands for boudning_box_top_left
    bbtl = (int(img_dim[1] / bbp), int(img_dim[0] / bbp))
    # bbbr stands for bounding_box_bottom_right
    bbbr = (int((bbp-1) * img_dim[1] / bbp), int((bbp-1) * img_dim[0] / bbp))

    display_webcam()
    topmost, bottommost, leftmost, rightmost = initialize_points()
    distances, vectors_list = track_vectors(topmost, bottommost, leftmost, rightmost)

    # separate dataframe into columns for plotting
    blue_vector = distances.loc[:]['Blue Vector']
    green_vector = distances.loc[:]['Green Vector']
    red_vector = distances.loc[:]['Red Vector']

    # create a dataframe that containes all of the minimum vectors (there is no
    # one single minimum vector because a minimum red vector doesn't necessarily
    # correlate exactly to the minimum green and blue vectors. Thus the frame that
    # correlates to the lowest average vector magnitude is used)
    min_vectors = pd.Series()

    prev_row_mean = 1000000.0 # arabitrarily large floating point
    for i in range(blue_vector.size):
        row_i = distances.loc[i]
        row_mean = row_i.mean()
        if row_mean < prev_row_mean:
            print('##### row mean: {}'.format(row_mean), i)
            min_vectors = vectors_list[i]
            prev_row_mean = row_mean
            continue

    # plot the vectors' magnitudes
    fig = plt.figure()
    vector_magnitude_plt = fig.add_subplot(111)
    vector_magnitude_plt.set_title('Vector Magnitude vs. Time')
    vector_magnitude_plt.set_xlabel('Vector Magnitude (pixels)')
    vector_magnitude_plt.set_ylabel('Time (frames)')
    vector_magnitude_plt.legend()
    plt.plot(blue_vector.index, blue_vector, 'b',
             green_vector.index, green_vector, 'g',
             red_vector.index, red_vector, 'r')
    plt.show()

    while True:
        ret, frame = cap.read()
        # display min_vectors
        cv2.circle(frame, (int(img_dim[1]/2),int(img_dim[0]/2)), 3, (0,0,0), -1)
        print(min_vectors)
        font = cv2.FONT_HERSHEY_COMPLEX
        for i in range(1,4):
            cv2.line(frame, (min_vectors[0][0], min_vectors[0][1]), (min_vectors[i][0],min_vectors[i][1]), colors[i-1], 3)
            x_squared = (min_vectors[0][0] - min_vectors[i][0])**2
            y_squared = (min_vectors[0][1] - min_vectors[i][1])**2
            pythag_dist = math.sqrt(x_squared + y_squared)
            # display the distances of the lines above the lines
            cv2.putText(frame,
                        'Length: {} pixels'.format(round(pythag_dist, 0)),
                        (min_vectors[i][0],min_vectors[i][1]),
                        font,0.5,colors[i-1],1)

            cv2.imshow('orthogonal view', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('An error occured')
            break

    cap.release()
    cv2.destroyAllWindows()
