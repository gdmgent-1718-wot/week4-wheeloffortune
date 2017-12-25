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

pwm.ChangeDutyCycle(10)
GPIO.output(07, True)
sleep(1)
pwm.ChangeDutyCycle(30)
sleep(1)
pwm.ChangeDutyCycle(50)
sleep(1)
pwm.ChangeDutyCycle(70)
sleep(1)
pwm.ChangeDutyCycle(90)
sleep(1)
pwm.ChangeDutyCycle(100)
sleep(10)
pwm.ChangeDutyCycle(90)
sleep(1)
pwm.ChangeDutyCycle(70)
sleep(1)
pwm.ChangeDutyCycle(50)
sleep(1)
pwm.ChangeDutyCycle(30)
sleep(1)
pwm.ChangeDutyCycle(10)
sleep(1)

GPIO.output(07, False)

