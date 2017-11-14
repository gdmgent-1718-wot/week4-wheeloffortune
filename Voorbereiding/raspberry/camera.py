from picamera import PiCamera
import datetime
from time import sleep
camera = PiCamera()
camera.start_preview()
camera.hflip = True
i = str(datetime.datetime.now())
print(i.replace(" ", ""))
sleep(1)

camera.capture('pictures/wheel' + i +'.jpg')
camera.stop_preview()
