# -*- coding: utf-8 -*-
"""
This script will serve as the main function set used for the operations of boom
tracking algorithm.

"""

import RPi.GPIO as gp
from time import sleep
import picamera
import cv2
import numpy as np
import argparse
#import imutils

def take_photo_set():
    #
    # Set the first camera 
    #
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    #
    # Take a photo with the first camera
    #
    #camera.capture('image_A.jpg')
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.framerate = 24
        image = np.empty((1024 * 768 * 3), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image_B = image.reshape((768, 1024, 3))
        #
        # Set the second camera 
        #
    gp.output(7, True)
    gp.output(11, False)
    gp.output(12, True)
    #
    # Take a photo with the second camera
    # 
    # camera.capture('image_B.jpg')
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.framerate = 24
        image = np.empty((1024 * 768 * 3), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image_A = image.reshape((768, 1024, 3))

    return image_A, image_B

##
 
def threshhold_images(image_A, image_B):
    #
    img_gray_A = cv2.cvtColor(image_A, cv2.COLOR_BGR2GRAY)
    img_gray_B = cv2.cvtColor(image_B, cv2.COLOR_BGR2GRAY)
    #
    #gaus_adapt_A = cv2.adaptiveThreshold(img_gray_A, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
    #                                   cv2.THRESH_BINARY, 91, 12)
    #gaus_adapt_B = cv2.adaptiveThreshold(img_gray_B, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
    #                                   cv2.THRESH_BINARY, 91, 12)
    _,gaus_adapt_A = cv2.threshold(img_gray_A,50,255,cv2.THRESH_BINARY)
    _,gaus_adapt_B = cv2.threshold(img_gray_B,50,255,cv2.THRESH_BINARY)
    
    
    return gaus_adapt_A, gaus_adapt_B
##
    
def centroid_images(gaus_adapt_A, gaus_adapt_B):
    #    
    centroids_A = []
    centroids_B = []
    #
    cnts_A = cv2.findContours(gaus_adapt_A, 1, 2)
    cnts_A = cnts_A[0]

    ii = 1;
    for c in cnts_A:
        # compute the center of the contour
        M = cv2.moments(c)
        if int(M["m00"]) != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #
            if ii == 1:
               centroids_A = np.array([cX, cY])
               ii = 0
            else:
               dum = np.array([cX, cY])
               centroids_A = np.vstack((centroids_A, dum))
    
    cnts_B = cv2.findContours(gaus_adapt_B, 1, 2)
    cnts_B = cnts_B[0]

    ii = 1;
    for c in cnts_B:
        # compute the center of the contour
        M = cv2.moments(c)
        if int(M["m00"]) != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            #
            if ii == 1:
               centroids_B = np.array([cX, cY])
               ii = 0
            else:
               dum = np.array([cX, cY])
               centroids_B = np.vstack((centroids_B, dum))
        
    return centroids_A, centroids_B

 
gp.setwarnings(False)
gp.setmode(gp.BOARD)

#Setup the stack layer 1 board
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

#Disable stack layer 1 board output
gp.output(11, True)
gp.output(12, True)

##

#image_A, image_B  = take_photo_set()
image_A = cv2.imread("image_A.jpg", 1)
image_B = cv2.imread("image_B.jpg", 1)
gaus_adapt_A, gaus_adapt_B = threshhold_images(image_A, image_B)
centroids_A, centroids_B = centroid_images(gaus_adapt_A, gaus_adapt_B)

print(centroids_A)
#cv2.imshow("gaus_adapt_A", gaus_adapt_A)
#cv2.waitKey(0)






