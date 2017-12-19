import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
#Connect the yellow cable to GPIO pin 18
GPIO.setup(7, GPIO.OUT)
#Connect the ground to the 7th top pin starting from the left
#Connect the V5 to the first top pin starting from the left
f = 50
t = (1 / f)

p = GPIO.PWM(7, f)
p.start(2.5)
try:
    while True:
        print "spinning"
			p.ChangeDutyCycle(2.5)
			time.sleep(1)
			p.ChangeDutyCycle(12)
			time.sleep(1)
except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
