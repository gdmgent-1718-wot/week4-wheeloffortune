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
        print "motor going 7.5"
        p.ChangeDutyCycle (12.5)
        time.sleep(0.5)
        print 'motor going 2.5'
        p.ChangeDutyCycle (2.5)
        time.sleep (0.5)

except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
