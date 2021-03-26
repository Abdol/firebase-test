import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate('energy-lab-1-firebase-adminsdk-9inby-7e9f14c603.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://energy-lab-1-default-rtdb.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference()
print(ref.get())
users_ref = ref.child('mac')
users_ref.set({
    'temp': 9,
    'hum': 0.87
})
