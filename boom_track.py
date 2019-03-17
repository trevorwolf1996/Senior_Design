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
        camera.resolution = (320, 240)
        image = np.empty((240 * 320 * 3,), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image_B = image.reshape((240, 320, 3))
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
        camera.resolution = (320, 240)
        image = np.empty((240 * 320 * 3,), dtype=np.uint8)
        camera.capture(image, 'bgr')
        image_A = image.reshape((240, 320, 3))

    return image_A, image_B

##
 
def threshhold_images(image_A, image_B):
    #
    img_gray_A = cv2.cvtColor(image_A, cv2.COLOR_BGR2GRAY)
    img_gray_B = cv2.cvtColor(image_B, cv2.COLOR_BGR2GRAY)
    #
    gaus_adapt_A = cv2.adaptiveThreshold(img_gray_A, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                       cv2.THRESH_BINARY, 91, 12)
    gaus_adapt_B = cv2.adaptiveThreshold(img_gray_B, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                       cv2.THRESH_BINARY, 91, 12)
    
    return gaus_adapt_A, gaus_adapt_B
##
    
def centroid_images(gaus_adapt_A, gaus_adapt_B):
    #
    # find contours in the thresholded image
    cnts_A = cv2.findContours(gaus_adapt_A.copy(), cv2.RETR_EXTERNAL,\
	             cv2.CHAIN_APPROX_SIMPLE)
    cnts_A = cnts_A[0]
    #cnts_A = imutils.grab_contours(cnts_A)
    cnts_B = cv2.findContours(gaus_adapt_B.copy(), cv2.RETR_EXTERNAL,\
	             cv2.CHAIN_APPROX_SIMPLE)
    cnts_B = cnts_B[0]
    #cnts_B = imutils.grab_contours(cnts_B)
    
    # Loop over the contours in image A
    size_c_A = np.size(cnts_A, 0)
    cX_A = np.zeros(size_c_A)
    cY_A = np.zeros(size_c_A)
    ii = 0
    
    for c in cnts_A:
        #
        M   = cv2.moments(cnts_A)
        cX_A[ii] = int(M["m10"] / M["m00"])
        cY_A[ii] = int(M["m01"] / M["m00"])
        ii = ii +1
      
    # Loop over the contours in image B
    size_c_B = np.size(cnts_B, 0)
    cX_B = np.zeros(size_c_B)
    cY_B = np.zeros(size_c_B)
    ii = 0
    
    for c in cnts_B:
        #
        M = cv2.moments(cnts_B)
        cX_B[ii] = int(M["m10"] / M["m00"])
        cY_B[ii] = int(M["m01"] / M["m00"])
        ii = ii +1
        
    return cX_A, cY_A, cX_B, cY_B

 
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

image_A, image_B  = take_photo_set()
gaus_adapt_A, gaus_adapt_B = threshhold_images(image_A, image_B)
cX_A, cY_A, cX_B, cY_B = centroid_images(gaus_adapt_A, gaus_adapt_B)

print(cX_A)






