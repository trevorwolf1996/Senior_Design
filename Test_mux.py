import RPi.GPIO as gp
import os

gp.setwarnings(False)
gp.setmode(gp.BOARD)

#Setup the stack layer 1 board
gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

#Disable stack layer 1 board output
gp.output(11, True)
gp.output(12, True)

def main():
 gp.output(7, False)
 gp.output(11, False)
 gp.output(12, True)
 capture(1)
 gp.output(7, True)
 gp.output(11, False)
 gp.output(12, True)
 capture(2)
 gp.output(7, False)
 gp.output(11, True)
 gp.output(12, False)
 capture(3)
 gp.output(7, True)
 gp.output(11, True)
 gp.output(12, False)
 capture(4)

def capture(cam):
 cmd = "raspistill -o capture_%d.jpg" % cam
 os.system(cmd)

if __name__ == "__main__":
 main()
 gp.output(7, False)
 gp.output(11, False)
 gp.output(12, True) 
