import firebase_admin
from firebase_admin import  credentials
from firebase_admin import db
import flotilla
import time

dock = flotilla.Client()
dial = dock.first(flotilla.Dial)
number = dock.first(flotilla.Number)

cred = credentials.Certificate('wheeloffortune-18d6d-firebase-adminsdk-vn804-4f020fab3d.json')
default_app = firebase_admin.initialize_app(cred,{'databaseURL':'https://wheeloffortune-18d6d.firebaseio.com/'})

try:
    while True:
        pos = int(dial.position)
        print(pos)
        number = pos
        time.sleep(1)
except KeyboardInterrupt:
    dock.stop()
