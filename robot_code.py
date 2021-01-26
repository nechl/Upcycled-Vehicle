#!/usr/bin/python3
import io, RPi.GPIO as GPIO
"""
Programm by Daniel Huber and Nicolas Perruchoud, 2020. 
To use it properly, highly recommended to add it to startup when using a RPI
This program is used to steer 2 DC motors via a radio mouse.

* : high
_ : low
logic table for driving
         A1 A2 B1 B2
front -> *  _  *  _
left  -> _  *  *  _
right -> *  _  _  *
off   -> _  _  _  _
"""

def Main() -> None:
        A1 = A2 = B1 = B2 = toggle_val = 0 # initiating everything to 0
        turningLeft = turningRight= False
        while True:
                v = mouse.read(6) # non-blocking input check
                if not v:
                        print(".",end="")
                        continue      # no input to handle

                if v == '\n\x00\x00\x08\x00\x00'and turningRight == False: #RIGHT mouse button is pressed, direction l <-, r ->, now turning right, only if not turning right now
                        A1 = 1         
                        A2 = 0
                        B1 = 0 
                        B2 = 1
                        turningLeft = False
                        turningRight = True

                elif v == '\t\x00\x00\x08\x00\x00' and turningLeft == False: #left mouse button is pressed	, only if not turning right now
                        # direction l ->, r <-
                        A1 = 0        
                        A2 = 1
                        B1 = 1 
                        B2 = 0
                        turningLeft = True
                        turningRight = False
                
                elif v == '\n\x00\x00\x08\x00\x00'and turningRight == True:
                        A1 = 0
                        A2 = 0
                        B1 = 0
                        B2 = 0
                        turningLeft = False
                        turningRight = False

                elif v == '\t\x00\x00\x08\x00\x00' and turningLeft == True:
                        A1 = 0
                        A2 = 0
                        B1 = 0
                        B2 = 0
                        turningRight = False
                        turningLeft = False   
                                           
                elif v == '\x08\x00\x00\x08\x00\x00':	# middle mouse button is rolled
                        mouse.flush() #
                        # turn wheels either on or off
                        toggle_val = not toggle_val         # toggle between 1 and 0
                        A1 = toggle_val        
                        A2 = 0
                        B1 = toggle_val 
                        B2 = 0
                        turningLeft = False
                        turningRight = False

                else:
                        print("Invalid io read: ", v)
                        mouse.flush()

	#write the new values to the pins
                #motor A
                GPIO.output(24, A1)
                GPIO.output(23, A2)
                #motor B
                GPIO.output(22, B1)     
                GPIO.output(25, B2)

if __name__ == '__main__':
        try:
                GPIO.setwarnings(False)
                # setting up pins & pin layout
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(22, GPIO.OUT) # direction left wheel
                GPIO.setup(23, GPIO.OUT) # direction right wheel
                GPIO.setup(24, GPIO.OUT) # power for motor left
                GPIO.setup(25, GPIO.OUT) # power for motor right
                mouse = io.open("/dev/input/mouse0", mode="r") # read mouse input
                Main()
        except Exception as e:
	#display error message, for debbuging
                print("Err: ", e) # mostly for debugging
                exit(-1)



