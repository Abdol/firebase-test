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

DEFAULT_CONFIG_LOCATION = os.path.join(os.path.dirname(__file__), 'cloud_config.ini')

def update_display(display, msg):
    with canvas(display) as draw:
        draw.text((0, 0), msg, fill='white')
def _none_to_nan(val):
    return float('nan') if val is None else val

def coral_main():
    # Pull arguments from command line.
    parser = argparse.ArgumentParser(description='Enviro Kit Demo')
    parser.add_argument('--display_duration',
                        help='Measurement display duration (seconds)', type=int,
                        default=5)
    parser.add_argument('--upload_delay', help='Cloud upload delay (seconds)',
                        type=int, default=300)
    parser.add_argument(
        '--cloud_config', help='Cloud IoT config file', default=DEFAULT_CONFIG_LOCATION)
    args = parser.parse_args()
    # Create instances of EnviroKit and Cloud IoT.
    global enviro
    with CloudIot(args.cloud_config) as cloud:
        # Indefinitely update display and upload to cloud.
        sensors = {}
        read_period = int(args.upload_delay / (2 * args.display_duration))
        for read_count in itertools.count():
            # First display temperature and RH.
            sensors['temperature'] = enviro.temperature
            sensors['humidity'] = enviro.humidity
            msg = 'Temp: %.2f C\n' % _none_to_nan(sensors['temperature'])
            msg += 'RH: %.2f %%' % _none_to_nan(sensors['humidity'])
            update_display(enviro.display, msg)
            sleep(args.display_duration)
            # After 5 seconds, switch to light and pressure.
            sensors['ambient_light'] = enviro.ambient_light
            sensors['pressure'] = enviro.pressure
            msg = 'Light: %.2f lux\n' % _none_to_nan(sensors['ambient_light'])
            msg += 'Pressure: %.2f kPa' % _none_to_nan(sensors['pressure'])
            update_display(enviro.display, msg)
            sleep(args.display_duration)
            # If time has elapsed, attempt cloud upload.
            if read_count % read_period == 0 and cloud.enabled():
                cloud.publish_message(sensors)

# Parameters
temp = 0.0 
hum = 0.0
lux = 0.0
bar = 0.0
delay = 4
path = "odroid_dmu"
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

while 1:
    # Get data from sensors
    coral_main()
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
    print("Uploading :")
    print(data)
    time_string = str(int(time.time()))
    db.child(path).child(time_string).set(data)

    # Retrieve database
    # data = db.child(path).get()
    # print(data.val())
    time.sleep(delay)
