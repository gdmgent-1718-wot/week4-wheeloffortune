import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)

f = 50
t = (1 / f)

p = GPIO.PWM(18, f)
p.start(2.5)

try:
    while True:
        print "motor turning"

except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
