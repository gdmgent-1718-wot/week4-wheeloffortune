
"""
==============================================
Wheel Of Fortune
==============================================
Course:     Web Of Things (WOT)
Option:     New Media Development
Department: Graphic and Digital Media
College:    Artevelde University College Ghent
----------------------------------------------
Authors:
    - Adriaan Glibert
    - Basiel Smitz
----------------------------------------------
Resources:
    - http://rpi.science.uoit.ca/lab/servo/
    - https://firebase.google.com/docs/admin/setup
    - https://i.stack.imgur.com/sVvsB.jpg
==============================================
"""
import firebase_admin
from firebase_admin import  credentials
from firebase_admin import db
import RPi.GPIO as GPIO
import time


cred = credentials.Certificate('wheeloffortune-18d6d-firebase-adminsdk-vn804-4f020fab3d.json')
default_app = firebase_admin.initialize_app(cred,{'databaseURL':'https://wheeloffortune-18d6d.firebaseio.com/'})

root = db.reference()
GPIO.setmode(GPIO.BOARD)
#Connect the yellow cable to GPIO pin 18
GPIO.setup(18, GPIO.OUT)
#Connect the ground to the 7th top pin starting from the left
#Connect the V5 to the first top pin starting from the left

f = 50
t = (1 / f)

p = GPIO.PWM(18, f)
p.start(2.5)
try:
	while True:
		#get values from Firebase and put them in variables
		posdb = root.child('value').get()
		picked = posdb['picked']
		# value should be between 2.5 and 12.5
		# correct values are 11, 9, 7.5, 5, 3.5
		value = posdb['value']

		#if result is picked move to result position and stop spinning
		if picked:
			print "stopping"
			p.ChangeDutyCycle(value)
			time.sleep(1)
	
		else:
			
			print "spinning"
			p.ChangeDutyCycle(2.5)
			time.sleep(1)
			p.ChangeDutyCycle(12)
			time.sleep(1)
			
		

except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
