
import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)



# Motor1A = 16
# Motor1B = 18
Motor1E = 24

# GPIO.setup(Motor1A,GPIO.OUT)
# GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

print "Turning motor on"
# GPIO.output(Motor1A,GPIO.HIGH)
# GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor1E,GPIO.HIGH)

sleep(30)

print "Stopping motor"
GPIO.output(Motor1E,GPIO.LOW)

GPIO.cleanup()
