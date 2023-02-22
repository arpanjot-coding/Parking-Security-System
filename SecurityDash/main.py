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
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
#from cons import Snake

global app
app = QApplication(sys.argv)


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("dashboard.ui", self)
        #self.LOGIN.clicked.connect(self.loginfunction)
        #self.SIGNUP.clicked.connect(self.gotocreate)

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

    def __init__(self):
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


    def addTAB(self):
        name, done1 = QtWidgets.QInputDialog.getText(self, 'Input Dialog', 'Enter video Id/Name :')
        if done1:
            self.ew.addMessage("Tab "+name+" Added","lightgreen")
            tab1 = QWidget()
            self.tabs.addTab(tab1, "VIDEO " + str(name))
            tab1.layout = QHBoxLayout(self)
            if int(name) <= 10:
                tab1.layout.addWidget(Window())
                tab1.layout.addWidget(Snake())
            else:
                tab1.layout.addWidget(CameraFeed())
                tab1.layout.addWidget(Snake())

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
        super(ErrorWidget,self).__init__()
        self.setFixedHeight(200)
        self.setStyleSheet("""
        background-color:rgb(255, 255, 255);
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)

        self.tabs = []
        for i in range(8):
            q1=QLabel("",self)
            self.layout.addWidget(q1)
            self.tabs.append(q1)

        self.setLayout(self.layout)
        self.tabCount = 0

    def addMessage(self,x,color):
        y = " "*12
        temp = QLabel(y+x,self)
        temp.setStyleSheet("color: "+color)
        self.layout.replaceWidget(self.tabs[self.tabCount],temp)
        self.tabs[self.tabCount] = temp
        self.tabCount = (self.tabCount+1)%8


class Window(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.init_ui()

    def init_ui(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'

        videowidget = QVideoWidget()

        openBtn = QPushButton('SELECT FROM FILES')
        openBtn.clicked.connect(self.open_file)

        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)

        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


class CameraFeed(QWidget):
    def __init__(self):
        super(CameraFeed, self).__init__()

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)

        self.Worker1 = Worker1()

        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()

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

    def __init__(self):
        super(Snake, self).__init__()
        self.RDict = {}
        # Loding the modelling files
        """
        self.model1 = torch.hub.load('ultralytics/yolov5', 'custom', path='D1-V1/train/exp/weights/best.pt',
                                force_reload=True)
        self.model2 = torch.hub.load('ultralytics/yolov5', 'custom', path='D2-V1/train/exp/weights/best.pt',
                                force_reload=True)
        self.model3 = torch.hub.load('ultralytics/yolov5', 'custom', path='Tool-V1/train/exp/weights/best.pt',
                                force_reload=True)
        self.reader = easyocr.Reader(['en'])
        """
        #self.cap = cv2.VideoCapture('a.mp4')
        self.initUI()

    def initUI(self):
        self.highscore = 0
        self.newGame()
        self.setStyleSheet("QWidget { background: #A9F5D0 }")
        #self.setFixedSize(550, 400)
        #self.setWindowTitle('Snake')
        #self.show()

    # Default method name
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.begin(self)
        self.drawSnake(qp)
        qp.end()

    def setRdict(self,r):
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
        #self.simulate()
        if 'CAR' in self.RDict.keys() and 'PERSON' in self.RDict.keys():
            self.CP1x = int(1249*(self.RDict['CAR']['p1'].x / 4560))
            self.CP1y = int(700*(self.RDict['CAR']['p1'].y / 2564))

            self.CP2x = int(1249*(self.RDict['CAR']['p2'].x / 4560))
            self.CP2y = int(700*(self.RDict['CAR']['p2'].y / 2564))

            self.PP1x = int(1249*(self.RDict['PERSON']['p1'].x / 4560))
            self.PP1y = int(700*(self.RDict['PERSON']['p1'].y / 2564))

            self.PP2x = int(1249*(self.RDict['PERSON']['p2'].x / 4560))
            self.PP2y = int(700*(self.RDict['PERSON']['p2'].y / 2564))

        else:
            self.CP1x = 100
            self.CP1y = 100

            self.CP2x = 120
            self.CP2y = 120

            self.PP1x = 200
            self.PP1y = 180

            self.PP2x = 250
            self.PP2y = 200

        self.repaint()

    # Not default method.
    def drawSnake(self, qp):
        # for car
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(255, 80, 0, 255))
        qp.drawRect(self.CP1x, self.CP1y,self.CP2x, self.CP2y)
        # for person
        qp.setBrush(QtGui.QColor(50, 255, 0, 255))
        qp.drawRect(self.PP1x, self.PP1y,self.PP2x, self.PP2y)

    # Default method name
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            # The code bellow is used to
            self.update()
            self.repaint()
        else:
            QtGui.QFrame.timerEvent(self, event)

welcome = MyTableWidget()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(700)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec_())
except:
    pass
