import RPi.GPIO as gp
from time import sleep
from picamera import PiCamera

def switch_camera():
 #
 # Set the first camera 
 #
 gp.output(7, False)
 gp.output(11, False)
 gp.output(12, True)
 #
 # Take a photo with the first camera
 #
 camera.capture('image_A.jpg')
 #
 # Set the second camera 
 #
 gp.output(7, True)
 gp.output(11, False)
 gp.output(12, True)
 #
 # Take a photo with the second camera
 # 
 camera.capture('image_B.jpg')

gp.setwarnings(False)
gp.setmode(gp.BOARD)

#Setup the stack layer 1 board
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

#Disable stack layer 1 board output
gp.output(11, True)
gp.output(12, True)

camera  = PiCamera()
camera.resolution = (1024, 768)

sleep(2)

#
# Run function
#
switch_camera()

