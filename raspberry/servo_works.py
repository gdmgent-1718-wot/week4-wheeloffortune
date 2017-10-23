#!/usr/bin/env python
#================================================
#
#	This program is for SunFounder SuperKit for Rpi.
#
#	Extend use of 8 LED with 74HC595.
#
#	Change the	WhichLeds and sleeptime value under
#	loop() function to change LED mode and speed.
#
#=================================================

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)

f = 20
t = (1 / f)

p = GPIO.PWM(18, f)
p.start(2.5)



while True:
	p.ChangeDutyCycle(2.5)
	time.sleep(t*100)
	p.ChangeDutyCycle(7.5)
	time.sleep(t*100)

