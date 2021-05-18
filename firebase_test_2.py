import time
import pyrebase
import SI1132
import BME280
import sys


# Parameters
temp = 0.0 
hum = 0.0
lux = 0.0
bar = 0.0
delay = 60
path = "odroid_dmu"
config = {
  "apiKey": "ck4RWASrUCpO3LZG1LivjeyVQWi8hn3d9YF0AtTM",
  "authDomain": "nergy-lab-1.firebaseapp.com",
  "databaseURL": "https://energy-lab-1-default-rtdb.firebaseio.com",
  "storageBucket": "nergy-lab-1.appspot.com",
  "serviceAccount": "energy-lab-1-firebase-adminsdk-9inby-7e9f14c603.json"
}

# WB
si1132 = SI1132.SI1132(sys.argv[1])
bme280 = BME280.BME280(sys.argv[1], 0x03, 0x02, 0x02, 0x02)
def get_altitude(pressure, seaLevel):
    atmospheric = pressure / 100.0
    return 44330.0 * (1.0 - pow(atmospheric/seaLevel, 0.1903))

print("UV_index : %.2f" % (si1132.readUV() / 100.0))
print("Visible : %d Lux" % int(si1132.readVisible()))
print("IR : %d Lux" % int(si1132.readIR()))
print("======== bme280 ========")
print("temperature : %.2f 'C" % bme280.read_temperature())
print("humidity : %.2f %%" % bme280.read_humidity())
p = bme280.read_pressure()
print("pressure : %.2f hPa" % (p / 100.0))
print("altitude : %.2f m" % get_altitude(p, 1024.25))


# Connect to Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

while 1:
    # Get data from sensors
    # TODO: get data from WEATHER-BOARD
    temp = bme280.read_temperature()
    hum = bme280.read_humidity()
    bar = bme280.read_pressure() / 100.0
    lux = int(si1132.readVisible())

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
    db.child(path).child('latest').set(data)
    # Retrieve database
    # data = db.child(path).get()
    # print(data.val())
    time.sleep(delay)
