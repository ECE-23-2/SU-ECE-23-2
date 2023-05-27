# Import required modules
import cv2
import numpy as np
import os
import glob
from PIL import Image
# Based on https://www.geeksforgeeks.org/camera-calibration-with-python-opencv/


def calibrateCamera():
    # Define the dimensions of checkerboard
    CHECKERBOARD = (6, 8)

    # stop the iteration when specified
    # accuracy, epsilon, is reached or
    # specified number of iterations are completed.
    criteria = (cv2.TERM_CRITERIA_EPS +
                cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Vector for 3D points
    threedpoints = []

    # Vector for 2D points
    twodpoints = []

    #  3D points real world coordinates
    objectp3d = np.zeros((1, CHECKERBOARD[0]
                          * CHECKERBOARD[1],
                          3), np.float32)
    objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
                          0:CHECKERBOARD[1]].T.reshape(-1, 2)
    prev_img_shape = None

    # Extracting path of individual image stored
    # in a given directory. Since no path is
    # specified, it will take current directory
    # jpg files alone
    images = glob.glob('imagesFolder/CalibrationPhotos/*.JPEG')

    # print('Start Calibration...')

    for filename in images:
        image = cv2.imread(filename)
        grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # cv2.imshow('img', grayColor)

        # Find the chess board corners
        # If desired number of corners are
        # found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(
            grayColor, CHECKERBOARD,
            cv2.CALIB_CB_ADAPTIVE_THRESH
            + cv2.CALIB_CB_FAST_CHECK +
            cv2.CALIB_CB_NORMALIZE_IMAGE)

        # If desired number of corners can be detected then,
        # refine the pixel coordinates and display
        # them on the images of checker board
        if ret == True:
            threedpoints.append(objectp3d)

            # Refining pixel coordinates
            # for given 2d points.
            corners2 = cv2.cornerSubPix(
                grayColor, corners, (11, 11), (-1, -1), criteria)

            twodpoints.append(corners2)

            # Draw and display the corners
            image = cv2.drawChessboardCorners(image,
                                              CHECKERBOARD,
                                              corners2, ret)

        # cv2.imshow('img_'+ filename, image)
        # cv2.waitKey(1000)

    cv2.destroyAllWindows()

    h, w = image.shape[:2]

    # Perform camera calibration by
    # passing the value of above found out 3D points (threedpoints)
    # and its corresponding pixel coordinates of the
    # detected corners (twodpoints)

    ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
        threedpoints, twodpoints, grayColor.shape[::-1], None, None)

    print('Done calibrating')

    return h, w, matrix, distortion


# Undistort Photos

def undistort(h, w, matrix, distortion, imageTitle):

    print("Getting image:", imageTitle)

    image = cv2.imread(imageTitle)
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(matrix, distortion, (w,h), 1, (w,h))

    # undistort
    distortion = cv2.undistort(image, matrix, distortion, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    distortion = distortion[y:y+h, x:x+w]

    split = imageTitle.split("/")

    # print(split)

    splitTitle = split[1].split(".")

    # print("Creating new undistorted Images...")
    newPathway = split[0] + "/final/" + splitTitle[0] + "_Fixed." + splitTitle[1]

    # print("Overwriting Distorted Images...")
    # newPathway = split[0] + "/" + splitTitle[0] + splitTitle[1]

    # print(newPathway)

    cv2.imwrite(newPathway, distortion)

    original_photo = Image.open(imageTitle)
    original_metadata = original_photo.info
    original_photo.save(newPathway, **original_metadata)

    original_photo.close()
    # # Displaying required output
    # print(" Camera matrix:")
    # print(matrix)
    #
    # print("\n Distortion coefficient:")
    # print(distortion)

    # print("\n Rotation Vectors:")
    # print(r_vecs)
    #
    # print("\n Translation Vectors:")
    # print(t_vecs)

def fixPhotos(h, w, matrix, distortion, folderPath):
    images = glob.glob(folderPath)
    print("Fixing photos...")
    counter = 0
    for file in images:
        print(counter)
        undistort(h, w, matrix, distortion, file)
        counter += 1

    print("Finished fixing")


# Example Calls


height, width, mat, distort = calibrateCamera()

undistort(height,width,mat,distort, "imagesFolder/Test4-0.JPEG")

# fixPhotos(height, width, mat, distort, "imagesFolder/*.JPEG")
