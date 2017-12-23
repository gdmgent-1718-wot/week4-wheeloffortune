import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

f = 50
t = (1 / f)

p = GPIO.PWM(7, f)
p.start(2.5)

try:
    while True:
        print "motor turning"
        p.ChangeDutyCycle (7.5)
        time.sleep(1)
        p.ChangeDutyCycle (2.5)
        time.sleep (1)

except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
