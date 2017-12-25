import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(03, GPIO.OUT)
GPIO.setup(05, GPIO.OUT)
GPIO.setup(07, GPIO.OUT)

pwm=GPIO.PWM(07, 100)

pwm.start(0)
GPIO.output(03, True)
GPIO.output(05, False)

pwm.ChangeDutyCycle(75)
GPIO.output(07, True)
sleep(2)
pwm.ChangeDutyCycle(40)
sleep(2)
GPIO.output(07, False)

