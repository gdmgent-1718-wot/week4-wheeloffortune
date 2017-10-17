import firebase_admin
from firebase_admin import  credentials
from firebase_admin import db
import flotilla
import time

dock = flotilla.Client()
dial = dock.first(flotilla.Dial)
number = dock.first(flotilla.Number)

try:
    while True:
        pos = int(dial.position)
        print(pos)
        number = pos
        time.sleep(1)
except KeyboardInterrupt:
    dock.stop()
