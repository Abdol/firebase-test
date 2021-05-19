import time
import pyrebase

from coral.enviro.board import EnviroBoard
from coral.cloudiot.core import CloudIot
from luma.core.render import canvas
from PIL import ImageDraw
from time import sleep
import argparse
import itertools
import os
import sys

# Parameters
temp = 0.0 
hum = 0.0
lux = 0.0
bar = 0.0
delay = 60
path = "coral_dmu"
config = {
  "apiKey": "ck4RWASrUCpO3LZG1LivjeyVQWi8hn3d9YF0AtTM",
  "authDomain": "nergy-lab-1.firebaseapp.com",
  "databaseURL": "https://energy-lab-1-default-rtdb.firebaseio.com",
  "storageBucket": "nergy-lab-1.appspot.com",
  "serviceAccount": "energy-lab-1-firebase-adminsdk-9inby-7e9f14c603.json"
}

# Start board
enviro = EnviroBoard()

# Connect to Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def update_display(display, msg):
    with canvas(display) as draw:
        draw.text((0, 0), msg, fill='white')
def _none_to_nan(val):
    return float('nan') if val is None else val

def coral_display():
    msg = 'Temp: %.2f C\n' % _none_to_nan(temp)
    msg += 'RH: %.2f %%' % _none_to_nan(hum)
    update_display(enviro.display, msg)
    sleep(delay * 0.2)
    msg = 'Light: %.2f lux\n' % _none_to_nan(lux)
    msg += 'Pressure: %.2f kPa' % _none_to_nan(bar)
    update_display(enviro.display, msg)
    sleep(delay * 0.8)

while 1:
    # Get data from sensors
    temp = enviro.temperature
    hum = enviro.humidity
    bar = enviro.pressure
    lux = enviro.ambient_light
    
    # Store data in database
    data = {
        'temp': temp,
        'hum': hum,
        'lux': lux,
        'bar': bar,
    }
    print("Uploading...")
    print(data)
    time_string = str(int(time.time()))
    db.child(path).child(time_string).set(data)
    db.child(path).child('latest').set(data)
    coral_display()
    # Retrieve database
    # data = db.child(path).get()
    # print(data.val())
    # time.sleep(delay)
