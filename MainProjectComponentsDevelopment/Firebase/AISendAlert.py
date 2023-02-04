import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("accountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://parkingsystemdatabasefyp-default-rtdb.firebaseio.com/',
    'storageBucket': 'parkingsystemdatabasefyp.appspot.com'
    })
# Put your local file path 
fileName = r"Files/frame_000003.PNG"
bucket = storage.bucket()
blob = bucket.blob(fileName)
blob.upload_from_filename(fileName)
# Opt : if you want to make public access from the URL
blob.make_public()
print("your file url", blob.public_url)

data = {
    "uId": "XudUph8LeUYACo8emS7eb81Aini1",
    "message": "Your car is stolen",
    "numPlate": "ABC 123",
    "image": blob.public_url,
    "time": 1675538430872,
    "read": False
}


alertRef = db.reference('Alerts').child('for users').child('XudUph8LeUYACo8emS7eb81Aini1')
alertRef.set(data)

print("Upload complete")
print(alertRef.get())
print("Program ended.......")