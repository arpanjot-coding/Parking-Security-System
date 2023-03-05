import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5 import QtGui, QtCore
import os
import sys
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import torch
import time

# from cons import Snake


app = QApplication(sys.argv)


# self.reader = easyocr.Reader(['en'])

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("dashboard.ui", self)
        # self.LOGIN.clicked.connect(self.loginfunction)
        # self.SIGNUP.clicked.connect(self.gotocreate)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def loginfunction(self):
        user = self.usern.toPlainText()
        password = self.passw.toPlainText()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")

        else:
            if '123' == password:
                print("Successfully logged in.")
                tabs = MyTableWidget()
                widget.addWidget(tabs)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            else:
                self.error.setText("Invalid username or password")


class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("SIGNUP.ui", self)
        self.SIGNUP.clicked.connect(self.signupfunction)
        self.BACK.clicked.connect(self.backtoLogin)

    def backtoLogin(self):
        self.BACK.setText("LOGIN")
        create = WelcomeScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def signupfunction(self):
        user = self.usern.toPlainText()
        password = self.passw.toPlainText()
        confirmpassword = self.passw2.toPlainText()

        if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0:
            self.error.setText("Please fill in all inputs.")
        else:
            self.backtoLogin()


class MyTableWidget(QWidget):

    def __init__(self, m1, m2, m3):
        super(QWidget, self).__init__()
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        # self.addTAB()

        tabBtn = QPushButton('ADD NEW TAB')
        tabBtn.clicked.connect(self.addTAB)

        self.tabs.resize(1100, 700)
        self.ew = ErrorWidget()
        # Add tabs to widget
        self.layout.addWidget(tabBtn)
        self.layout.addWidget(self.ew)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.model1 = m1
        self.model2 = m2
        self.model3 = m3

    def addTAB(self):
        name, done1 = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter video Id/Name :')
        if done1:
            self.ew.addMessage("Tab " + name + " Added", "lightgreen")

            tab1 = QWidget()
            self.tabs.addTab(tab1, "VIDEO " + str(name))
            tab1.layout = QHBoxLayout(self)
            mask = Snake(self.model1, self.model2, self.model3, self.ew, name)

            tab1.layout.addWidget(CameraFeed(mask, name))
            tab1.layout.addWidget(mask)

            tab1.setLayout(tab1.layout)
            # Add tabs to widget
            self.layout.addWidget(self.tabs)
            self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


class ErrorWidget(QWidget):
    def __init__(self):
        super(ErrorWidget, self).__init__()
        self.setFixedHeight(200)
        self.setStyleSheet("""
        background-color:rgb(255, 255, 255);
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.tabs = []
        for i in range(8):
            q1 = QLabel("", self)
            self.layout.addWidget(q1)
            self.tabs.append(q1)

        self.setLayout(self.layout)
        self.tabCount = 0

    def addMessage(self, x, color):
        y = " " * 12
        if self.verifyInput(y + x):
            temp = QLabel(y + x, self)
            temp.setStyleSheet("color: " + color)
            self.layout.replaceWidget(self.tabs[self.tabCount], temp)
            self.tabs[self.tabCount] = temp
            self.tabCount = (self.tabCount + 1) % 8

    def resetMessages(self):
        self.tabCount = 0
        for i in range(len(self.tabs)):
            temp = QLabel("", self)
            self.layout.replaceWidget(self.tabs[i], temp)
            self.tabs[i] = temp

    def verifyInput(self, msg):
        # for i in range(len(self.tabs)):
        #    if msg == self.tabs[i].text():
        #        return False
        return True


class CameraFeed(QWidget):
    def __init__(self, video, name):
        super(CameraFeed, self).__init__()

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)

        self.Worker1 = Worker1()
        if int(name) <= 10:
            filename, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                          "All Files (*);;Text Files (*.mp4)")
            if filename != "":
                self.Worker1.setVideoMask(video, filename)
        else:
            self.Worker1.setVideoMask(video, 0)

        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()


class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def setVideoMask(self, video, n):
        self.video = video
        self.op = n

    def run(self):
        self.ThreadActive = True

        Capture = cv2.VideoCapture(self.op)

        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                self.video.simulate(FlippedImage)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0],
                                           QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ',' + str(self.y) + ")"


class Snake(QWidget):
    score = 0
    CP1x = 15
    CP1y = 15
    CP2x = 15
    CP2y = 15
    PP1x = 15
    PP1y = 15
    PP2x = 15
    PP2y = 15

    def __init__(self, m1, m2, m3, msg, name):
        super(Snake, self).__init__()
        self.RDict = {}
        self.setFixedSize(550, 400)
        # Loding the modelling files
        try:
            os.mkdir('test')
        except:
            pass

        self.model1 = m1
        self.model2 = m2
        self.model3 = m3
        self.msg = msg
        # self.reader = easyocr.Reader(['en'])
        self.name = name
        self.n2d = True
        self.videoSet = False
        self.initUI()

    def initUI(self):
        self.highscore = 0
        self.newGame()
        self.setStyleSheet("QWidget { background: #A9F5D0 }")

    def setVideo(self, path):
        self.cap = cv2.VideoCapture(path)
        self.videoSet = True

    # Default method name
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)
        self.drawSnake(qp)
        qp.end()

    def setRdict(self, r):
        self.RDict = r

    # Not default method.
    def newGame(self):
        self.timer = QtCore.QBasicTimer()
        self.speed = 100
        self.start()

    # Not default method.
    def pause(self):
        self.isPaused = True
        self.timer.stop()
        self.update()

    # Not default method.
    def start(self):
        self.isPaused = False
        self.timer.start(self.speed, self)
        self.update()

    # Not default method.
    def update(self):
        if self.videoSet or True:
            # self.simulate()
            if 'CAR' in self.RDict.keys() and 'PERSON' in self.RDict.keys():
                self.CP1x = int(550 * (self.RDict['CAR']['p1'].x / 4560))
                self.CP1y = int(400 * (self.RDict['CAR']['p1'].y / 2564))

                self.CP2x = int(550 * (self.RDict['CAR']['p2'].x / 4560))
                self.CP2y = int(400 * (self.RDict['CAR']['p2'].y / 2564))

                self.PP2x = int(550 * (self.RDict['PERSON']['p2'].x / 5560))
                self.PP2y = int(400 * (self.RDict['PERSON']['p2'].y / 2564))

                self.PP1x = self.PP2x - 5
                self.PP1y = self.PP2y - 5

            else:

                self.CP1x = 1
                self.CP1y = 1

                self.CP2x = 2
                self.CP2y = 2

                self.PP1x = 1
                self.PP1y = 1

                self.PP2x = 2
                self.PP2y = 2
        else:
            self.CP1x = 1
            self.CP1y = 1

            self.CP2x = 2
            self.CP2y = 2

            self.PP1x = 1
            self.PP1y = 1

            self.PP2x = 2
            self.PP2y = 2

        self.repaint()

    # Not default method.
    def drawSnake(self, qp):
        # for car
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(255, 80, 0, 255))
        qp.drawRect(self.CP1x, self.CP1y, self.CP2x, self.CP2y)
        # for person
        qp.setBrush(QtGui.QColor(50, 255, 0, 255))
        qp.drawRect(self.PP1x, self.PP1y, self.PP2x, self.PP2y)

    # Default method name
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            # The code bellow is used to
            self.update()
            self.repaint()
        else:
            QtGui.QFrame.timerEvent(self, event)

        """
    - Fuction is used to resize image by maintaining the actual ratio of image
    - Arguements Image, width or height (according to which resizing should be done)
    - Returns the resized cv2 image
    """

    def image_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image

        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)

        else:
            r = width / float(w)
            dim = (width, int(h * r))

        resized = cv2.resize(image, dim, interpolation=inter)
        return resized

    """
    - This function is used to check if the 2 functions intersecting or not.
    - Arguments are the different Objects containg the x-axis and y-axis of the bounding boxes's coordinates.
    - Returns true if the there's intersection else true
    """

    def do_overlap(self, O1, O2):
        l1 = O1['p1']
        r1 = O1['p2']

        l2 = O2['p1']
        r2 = O2['p2']

        if l1.x == r1.x or l1.y == r1.y or r2.x == l2.x or l2.y == r2.y:
            return False

        if l1.x > r2.x or l2.x > r1.x:
            return False

        return True

    """
    - This function is being used to get the number from the images.
    - It is used to get the number out of number plate image
    - Argument's are the image, data containg the information
      of bounding boxes around the number plate
    - return number from number plate.
    """

    def getNumberPlate(self, frame, data):
        p1 = data['p1']
        p2 = data['p2']

        frame = frame[int(p1.y):int(p2.y), int(p1.x):int(p2.x)]

        cv2.imwrite("test/n.jpg", frame)
        output = ""  # self.reader.readtext("test/n.jpg")
        num = ""
        for i in output:
            num += " - " + i[1]

        return num

    """
    - this is the function used to check if the date given is today's.
    - Argument is the date.
    - returns the Boolean.
    """

    def verifyDate(self, date):
        t = time.localtime()
        return (str(t[2]) + "/" + str(t[1]) + "/" + str(t[0])) == date

    """
    Code for detections and conditions
    By running the video frame 1 by 1 using while loop
    """

    def simulate(self, frame, ret=True):
        # reading frame and success of the frame
        # ret, frame = self.cap.read()

        # if successful then checking conditions
        if ret:
            # Getting predictions from model1 about frame
            results1 = self.model1(frame)
            dat1 = results1.pandas().xyxy[0]
            result1 = dat1.values
            img = np.squeeze(results1.render())

            # Getting predictions from model2 about frame
            results2 = self.model2(img)
            dat2 = results2.pandas().xyxy[0]
            result2 = dat2.values
            img = np.squeeze(results2.render())

            # Getting predictions from model1 about frame
            results3 = self.model3(img)
            dat3 = results3.pandas().xyxy[0]
            result3 = dat3.values
            img = np.squeeze(results3.render())

            # img is the final image with bounding boxes from all the images.

            self.RDict = {}  # used to collect the information about the frame in dictionary.
            i = 0
            CarDoorOpen = False

            # count the number of cars available or person etc...
            carCount = 1
            personCount = 1
            numberPlateCount = 1
            toolCount = 1
            securityCount = 1

            # now first of all lets get the objects of model 1 results
            for obj in result1:
                # checking 'car door open' object is available in results
                if 'Car door open' == obj[
                    -1] and 'CAR' in self.RDict.keys():  # and if the 1 'CAR' was already there in the dictionary
                    if self.RDict['CAR']['C'] > obj[4]:
                        self.RDict['CAR']['count'] += 1
                        # if the model is confusing the 'car door open and car door close then take car with high confidence
                    else:
                        # collect the car
                        self.RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                             'count': carCount}
                        carCount += 1

                    # if car door is open and the confidence is above 70% then say the car door is open
                    if obj[4] > 0.70:
                        CarDoorOpen = True
                        # writing on frame that the car door is open
                        cv2.putText(img, "CAR DOOR OPEN", (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                                    cv2.LINE_4)
                        self.msg.addMessage("Tab " + self.name + " : CAR DOOR OPEN", "red")

                elif 'Car door close' == obj[-1] and 'CAR' not in self.RDict.keys():
                    # checking 'car door close' object is available in results and adding it to the dictionary
                    self.RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                         'count': carCount}
                    carCount += 1

                elif 'Car door close' == obj[
                    -1] and 'CAR' in self.RDict.keys():  # and if the 1 'CAR' was already there in the dictionary
                    # checking 'car door close' object is available in results
                    if self.RDict['CAR']['C'] > obj[4]:
                        self.RDict['CAR']['count'] += 1
                    else:
                        # collect the car
                        self.RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                             'count': carCount}
                        carCount += 1

                elif 'Car door open' == obj[-1] and 'CAR' not in self.RDict.keys():
                    # checking 'car door open' object is available in results and adding it to the dictionary
                    self.RDict['CAR'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                         'count': carCount}
                    carCount += 1
                    # if car door is open and the confidence is above 70% then say the car door is open
                    if obj[4] > 0.70:
                        # writing on frame that the car door is open
                        CarDoorOpen = True
                        self.msg.addMessage("Tab " + self.name + " : CAR DOOR OPEN", "red")

                elif 'number plate' == obj[-1]:
                    # checking 'number plate' object is available in results and adding it to the dictionary
                    self.RDict['PLATE'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                           'count': numberPlateCount}
                    numberPlateCount += 1

            # now lets get the objects of model 2 results
            for obj in result2:
                # checking 'Person' object is available in results and adding it to the dictionary
                if 'Person' == obj[-1]:
                    # if Person is in frame and the confidence is above 70% then person is confirm
                    if obj[4] > 0.5:
                        self.RDict['PERSON'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                                'count': personCount}
                        personCount += 1

                # checking 'Security' object is available in results and adding it to the dictionary
                elif 'Security' == obj[-1]:
                    # if Security is in frame and the confidence is above 70% then person is confirm
                    if obj[4] > 0.6:
                        self.RDict['SECURITY'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                                  'count': securityCount}
                        securityCount += 1

            keys = self.RDict.keys()

            # getting the results of Tools model
            for obj in result3:
                # Storing the TOOL information in the Dictionary
                self.RDict['TOOL'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4],
                                      'count': toolCount}
                toolCount += 1

                # Checking if the CAR is in frame and the PERSON is also there
                if 'CAR' in keys and 'PERSON' in keys:
                    # checking if the person is intersecting with the tools or not
                    if self.do_overlap(self.RDict['TOOL'], self.RDict['PERSON']) and self.do_overlap(self.RDict['TOOL'],
                                                                                                     self.RDict['CAR']):
                        # if intersecting then saying 'someone is trying to breakin"
                        self.msg.addMessage("Tab " + self.name + " : SOMEONE IS BREAKING IN THE CAR", "red")

            keys = self.RDict.keys()

            # Checking if the car is in frame + person is also present + if car door is open or not + is today the checkin date or not
            if 'CAR' in keys and 'PERSON' in keys and CarDoorOpen and not self.verifyDate("4/2/2023"):
                # if car and person is overlaping then saying its 'manual robbery'
                if self.do_overlap(self.RDict['CAR'], self.RDict['PERSON']):
                    self.msg.addMessage("Tab " + self.name + " : MANUAL ROBBERY", "red")

            # if tool and person is intersecting then saying 'potential robbery'
            if 'PERSON' in keys and 'TOOL' in keys and self.do_overlap(self.RDict['TOOL'], self.RDict['PERSON']):
                self.msg.addMessage("Tab " + self.name + " : POTENTIAL ROBBERY", "blue")

            # displaying the frame
            # cv2.imshow('YOLO',self.image_resize(img,width=1000))

            # if number plate is in frame then geting the number from number plate
            if 'PLATE' in keys:
                print(self.getNumberPlate(frame, self.RDict['PLATE']))

            if 'CAR' in keys and 'PERSON' in keys:
                pass

            # self.msg.resetMessages()
            return img

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()


model1 = torch.hub.load('ultralytics/yolov5', 'custom', path='D1-V1/train/exp/weights/best.pt',
                                force_reload=True)
model2 = torch.hub.load('ultralytics/yolov5', 'custom', path='D2-V1/train/exp/weights/best.pt',
                        force_reload=True)
model3 = torch.hub.load('ultralytics/yolov5', 'custom', path='Tool-V1/train/exp/weights/best.pt',
                        force_reload=True)
welcome = MyTableWidget(model1, model2, model3)
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(700)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec_())
except:
    pass
