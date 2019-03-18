# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 23:17:16 2019

This script will serve to capture a set of images that will be used for testing
the tracking algorithm. These images will be stored in the form of a numpy array 
and then post-processed. A time-stamp will also be added for each image as it will
be needed for the filtering function. 

@author: Trevor
"""

import RPi.GPIO as gp
from time import sleep
import picamera
import cv2
import numpy as np
import argparse
import time 
import pickle

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
        t_A = int(round(time.time() * 1000))
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
        t_B = int(round(time.time() * 1000))


    return image_A, image_B, t_A, t_B

##
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
# call function and store images 
class save_data():
    pass

save_image_A = save_data()
save_image_B = save_data()
save_time_A = save_data()
save_time_B = save_data()


for ii in range(0, 20):
    #
    image_A, image_B, t_A, t_B = take_photo_set()
    save_image_A.ii = image_A
    save_image_B.ii = image_B
    save_time_A.ii = t_A
    save_time_B.ii = t_B
    
file_dump_A = open('image_A_save.obj', 'w') 
file_dump_B = open('image_B_save.obj', 'w') 
pickle.dump(save_image_A, file_dump_A)
pickle.dump(save_image_B, file_dump_B)
    
    

