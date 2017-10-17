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

try:
    while True:
        #posdb = root.child('value').get()
        #print(posdb['value'])
        motor.set_speed(20)
        motor.update()
        time.sleep(5)
        motor.stop()
except KeyboardInterrupt:
    dock.stop()
