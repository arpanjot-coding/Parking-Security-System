# IMPORTS
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import torch
import sys
import firebase_admin
from firebase_admin import db,auth,credentials
from dashboard import MyTableWidget

# LOADING MODELS
model1 = torch.hub.load('ultralytics/yolov5', 'custom', path='MODELS/D1-V1/train/exp/weights/best.pt', force_reload=True)
model2 = torch.hub.load('ultralytics/yolov5', 'custom', path='MODELS/D2-V1/train/exp/weights/best.pt', force_reload=True)
model3 = torch.hub.load('ultralytics/yolov5', 'custom', path='MODELS/Tool-V1/train/exp/weights/best.pt', force_reload=True)

# CONNECTING TO THE FIREBASE
cred = credentials.Certificate("accountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://parkingsystemdatabasefyp-default-rtdb.firebaseio.com/',
    'storageBucket': 'parkingsystemdatabasefyp.appspot.com'
})

# RETRIEVEING AND STORING ALL USER ID'S IN DICTIONARY
page = auth.list_users()
UserData = {}

while page:
    for user in page.users:
        userData = db.reference("Users").child(user.uid).get()
        allBookings = db.reference("Bookings").child(user.uid).get()

        for key, value in allBookings.items():
            booking = value
            NP = booking['numPlate']
            Date = booking['to']

        UserData[user.uid] = {"Name": userData['firstName'], "NP": NP, "Date": Date}
    if not page.next_page_token:
        break
    page = auth.list_users(page.next_page_token)


# STARTING APPLICATION

app = QApplication(sys.argv)
welcome = MyTableWidget(model1, model2, model3, UserData)
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)

widget.setFixedHeight(700)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec_())
except:
    pass
