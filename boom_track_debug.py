# -*- coding: utf-8 -*-
"""
This script will serve as the main function set used for the operations of boom
tracking algorithm.

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

 
def threshhold_images(image_A, image_B):
    #
    #img_gray_A = cv2.cvtColor(image_A, cv2.COLOR_BGR2GRAY)
    #img_gray_B = cv2.cvtColor(image_B, cv2.COLOR_BGR2GRAY)
    img_gray_A = image_A
    img_gray_B = image_B
    #
    gaus_adapt_A = cv2.adaptiveThreshold(img_gray_A, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                       cv2.THRESH_BINARY, 91, 12)
    gaus_adapt_B = cv2.adaptiveThreshold(img_gray_B, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                       cv2.THRESH_BINARY, 91, 12)
    
    return gaus_adapt_A, gaus_adapt_B
##
    

image_A = cv2.imread('image_A.jpg', 1)
img_gray_A = cv2.cvtColor(image_A, cv2.COLOR_BGR2GRAY)
img_gray_B = img_gray_A

gaus_adapt_A, gaus_adapt_B = threshhold_images(img_gray_A, img_gray_B)
cnts_A = cv2.findContours(gaus_adapt_A, 1, 2)
cnts = cnts_A[0]

ii = 1;
for c in cnts:
	# compute the center of the contour
    M = cv2.moments(c)
    if int(M["m00"]) != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
   #
    if ii == 1:
       centroids = np.array([cX, cY])
       ii = 0
    else:
       dum = np.array([cX, cY])
       centroids = np.vstack((centroids, dum))
       
#cv2.imshow('image', gaus_adapt_A)
#cv2.waitKey(0)

