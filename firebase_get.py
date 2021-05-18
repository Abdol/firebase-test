import pyrebase
import json

# Parameters
temp = 0.0
hum = 0.0
lux = 0.0
bar = 0.0
delay = 2
path = "odroid_dmu"
config = {
  "apiKey": "ck4RWASrUCpO3LZG1LivjeyVQWi8hn3d9YF0AtTM",
  "authDomain": "nergy-lab-1.firebaseapp.com",
  "databaseURL": "https://energy-lab-1-default-rtdb.firebaseio.com",
  "storageBucket": "nergy-lab-1.appspot.com",
  "serviceAccount": "energy-lab-1-firebase-adminsdk-9inby-7e9f14c603.json"
}

# Connect to Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Retrieve database
data = db.child(path).child('latest').get()
print(json.dumps(data.val(), indent = 4))
