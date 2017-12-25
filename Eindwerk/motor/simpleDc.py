import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import  credentials
from firebase_admin import db
from time import sleep

cred = credentials.Certificate('wheeloffortune-18d6d-firebase-adminsdk-vn804-4f020fab3d.json')
default_app = firebase_admin.initialize_app(cred,{'databaseURL':'https://wheeloffortune-18d6d.firebaseio.com/'})
root = db.reference()
GPIO.setmode(GPIO.BOARD)

GPIO.setup(03, GPIO.OUT)
GPIO.setup(05, GPIO.OUT)
GPIO.setup(07, GPIO.OUT)

pwm=GPIO.PWM(07, 100)

pwm.start(0)
GPIO.output(03, True)
GPIO.output(05, False)

try:
	while True:
		#get values from Firebase and put them in variables
		posdb = root.child('game/motor').get()
        # is motor turning?
		turning = posdb['turning']
		# speed > 70 && < 100
		speed = posdb['speed']

		if turning:
                print "turning"
                GPIO.output(07, True)
                pwm.ChangeDutyCycle(speed)
		else:
                print "waiting"
			    GPIO.output(07, False)
except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()

