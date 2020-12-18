#!/usr/bin/python3
import io, RPi.GPIO as GPIO
"""
Programm by Daniel Huber and Nicolas Perruchoud

* : high
_ : low

	 dl dr pl pr
Pin numb:22 23 24 25
strgt -> _  _  *  *
Lturn -> _  *  -  *
rturn -> *  _  *  -
off   -> _  _  _  _
"""

def Main() -> None:
        dl = dr = pl = pr = toggle_val = 0 # initiating everything to 0
        while True:
                v = mouse.read(6) # non-blocking input check
                if not v:
                        print(".",end="")
                        continue      # no input to handle

                if v == '\n\x00\x00\x08\x00\x00':#RIGHT mouse button is pressed, direction l <-, r ->
                        dl = 0         # clear direction
                        dr = 1
                        pl = 0 # turn general speed either on or off
                        pr = 1

                elif v == '\t\x00\x00\x08\x00\x00':		# left mouse button is pressed	
                        # direction l ->, r <-
                        dl = 1         # clear direction
                        dr = 0
                        pl = 1 # turn general speed either on or off
                        pr = 0

                elif v == '\x08\x00\x00\x08\x00\x00':	# middle mouse button is rolled
                        mouse.flush() #
                        # turn wheels either on or off
                        toggle_val = not toggle_val         # toggle between 1 and 0
                        dl = 0         # clear direction
                        dr = 0
                        pl = toggle_val # turn general speed either on or off
                        pr = toggle_val

                else:
                        print("Invalid io read: ", v)
                        mouse.flush()

	#write the new values to the pins
                GPIO.output(22, dl)
                GPIO.output(23, dr)
                GPIO.output(24, pl)
                GPIO.output(25, pr)




if __name__ == '__main__':
        try:
                GPIO.setwarnings(False)
                # setting up pins
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



