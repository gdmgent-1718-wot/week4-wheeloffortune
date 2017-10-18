import firebase_admin
from firebase_admin import  credentials
from firebase_admin import db
import flotilla
import time

dock = flotilla.Client()
dial = dock.first(flotilla.Dial)
number = dock.first(flotilla.Number)
motor = dock.first(flotilla.Motor)
print(motor)


cred = credentials.Certificate('wheeloffortune-18d6d-firebase-adminsdk-vn804-4f020fab3d.json')
default_app = firebase_admin.initialize_app(cred,{'databaseURL':'https://wheeloffortune-18d6d.firebaseio.com/'})

root = db.reference()
turning = True
speed = 63

try:
    while turning:
        posdb = root.child('value').get()
        print(posdb['value'])
        #min value = 6 1 tour 13.70
        #10 value = tour 7.10
        #15 value = tour 4.40
        #30 value = tour 2.20
        #40 value = tour 1.65
        motor.set_speed(speed)
        motor.update()
        speed - 1
        if (speed == 6)
            motor.stop()
            turning = False
        time.sleep(60)
        motor.stop()
        turning = False
except KeyboardInterrupt:
    dock.stop()
