from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys
from LoginPage import WelcomeScreen
import firebase_admin
from firebase_admin import db,auth,credentials
import torch

# LOADING MODELS
# Load the three models
model1 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                                path='C:/Users/sarpa/OneDrive/Desktop/Project/TestingResources/Models/D1/best.pt',
                                source='local')
model2 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                                path='C:/Users/sarpa/OneDrive/Desktop/Project/TestingResources/Models/D2/best.pt',
                                source='local')

model3 = torch.hub.load('C:/Users/sarpa/OneDrive/Desktop/yolov5', 'custom',
                                path='C:/Users/sarpa/OneDrive/Desktop/Project/TestingResources/Models/Tools/best.pt',
                                source='local')


# CONNECTING TO THE FIREBASE
cred = credentials.Certificate("accountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://parkingsystemdatabasefyp-default-rtdb.firebaseio.com/',
    'storageBucket': 'parkingsystemdatabasefyp.appspot.com'
})

# RETRIEVING AND STORING ALL USER ID'S IN DICTIONARY
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

def goto_create():
    create = CreateAccScreen(back_to_login, widget, model1, model2, model3, UserData)
    widget.addWidget(create)
    widget.setCurrentIndex(widget.currentIndex() + 1)


def back_to_login():
    login_page = WelcomeScreen(goto_create, widget, model1, model2, model3, UserData)
    widget.addWidget(login_page)
    widget.setCurrentIndex(widget.currentIndex() + 1)

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login_page = WelcomeScreen(goto_create, widget,model1, model2, model3, UserData)
widget.addWidget(login_page)
widget.setFixedHeight(1400)
widget.setFixedWidth(2400)
widget.show()

try:
    sys.exit(app.exec_())
except:
    pass
