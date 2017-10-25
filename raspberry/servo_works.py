import firebase_admin
from firebase_admin import  credentials
from firebase_admin import db
import RPi.GPIO as GPIO
import time


cred = credentials.Certificate('wheeloffortune-18d6d-firebase-adminsdk-vn804-4f020fab3d.json')
default_app = firebase_admin.initialize_app(cred,{'databaseURL':'https://wheeloffortune-18d6d.firebaseio.com/'})

root = db.reference()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)

f = 50
t = (1 / f)

p = GPIO.PWM(18, f)
p.start(2.5)
stopped = False


try:
	while True:
		posdb = root.child('value').get()
		picked = posdb['picked']
		value = posdb['value']
		print "picked:  " + str(picked) + " value:  " + str(value) + " stopped:  " + str(stopped)

		if picked:
			if stopped == False:
				print "stopping"
				stopped = True
				p.ChangeDutyCycle(value)
				time.sleep(5)
				p.stop()
				GPIO.cleanup()

			else:
				print "stopped"		
		else:
			if stopped: 
				print "restarting"
				stopped = False
				p.start(2.5)
			print "busy"
			p.ChangeDutyCycle(2.5)
			time.sleep(1)

			p.ChangeDutyCycle(12)
			time.sleep(1)
			
		

except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
