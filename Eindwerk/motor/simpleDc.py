import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import sleep


cred = credentials.Certificate("wheeloffortune2-c0e4a-firebase-adminsdk-xx83k-8a28c73b1e.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://wheeloffortune2-c0e4a.firebaseio.com/'})
root = db.reference()
GPIO.setmode(GPIO.BOARD)

GPIO.setup(03, GPIO.OUT)
GPIO.setup(05, GPIO.OUT)
GPIO.setup(07, GPIO.OUT)

pwm = GPIO.PWM(07, 100)

pwm.start(0)
GPIO.output(03, True)
GPIO.output(05, False)

try:
    while True:
        # get values from Firebase and put them in variables
        posdb = root.child('game').child('motor').get()
        # is motor turning?
        turning = posdb['turning']
        # speed > 70 && < 100
        speed = posdb['speed']
        if turning:
            print 'turning'
            # sleep(2)
            GPIO.output(07, True)
            pwm.ChangeDutyCycle(speed)
        else:
            print 'stopped'
            sleep(2)
            GPIO.output(07, False)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
