import threading

import torch
import numpy as np
import cv2
import sys,time
import pandas as pd
import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QApplication


try:
    os.mkdir('test')
except:
    pass

"""
- class to store the coordinate points of the images according to x and y axis.
- It is storing the coordinates of bounding boxes
"""
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return "("+str(self.x)+','+str(self.y)+")"

class Snake(QWidget):

    score = 0
    CP1x = 15
    CP2y = 15
    PP1x = 15
    PP2x = 15
    PP2y = 15

    def __init__(self):
        super(Snake, self).__init__()
        self.RDict = {}
        # Loading the modelling files
        # self.model1 = torch.hub.load('ultralytics/yolov5', 'custom', path='Model/D1/best.pt', force_reload=True)
        # self.model2 = torch.hub.load('ultralytics/yolov5', 'custom', path='Model/D2/best.pt', force_reload=True)
        # self.model3 = torch.hub.load('ultralytics/yolov5', 'custom', path='Model/Tools/best.pt', force_reload=True)
        # This is how to load the model dependencies form local git
        self.model1 = torch.hub.load('Model/yolov5', 'custom', path='Model/D1/best.pt', source='local')
        self.model2 = torch.hub.load('Model/yolov5', 'custom', path='Model/D2/best.pt', source='local')
        self.model3 = torch.hub.load('Model/yolov5', 'custom', path='Model/Tools/best.pt', source='local')



        self.cap = cv2.VideoCapture('Files/N1.mp4')
        self.initUI()

    def initUI(self):
        self.highscore = 0
        self.newGame()
        self.setStyleSheet("QWidget { background: #A9F5D0 }")
        self.setFixedSize(800, 600)
        self.setWindowTitle('Snake')
        self.show()

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
        self.simulate()
        if 'CAR' in self.RDict.keys() :
            self.CP1x = int(1249*(self.RDict['CAR']['p1'].x / 4560))

            self.CP2y = int(700*(self.RDict['CAR']['p2'].y / 2564))

            try:
                self.PP1x = int(1249*(self.RDict['PERSON']['p1'].x / 4560))

                self.PP2x = int(1249*(self.RDict['PERSON']['p2'].x / 4560))
                self.PP2y = int(700*(self.RDict['PERSON']['p2'].y / 2564))
            except:
                self.PP1x = 0

                self.PP2x = 1
                self.PP2y = 1
        else:
            self.CP1x = 0

            self.CP2y = 1

            self.PP1x = 0

            self.PP2x = 1
            self.PP2y = 1

        self.repaint()

    # Not default method.
    def drawSnake(self, qp):
        # for car
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(0, 0, 0, 255))
        qp.drawRect(self.CP1x, self.CP2y+150, 200, -200)

        # for person
        qp.setBrush(QtGui.QColor(220,20,60, 255))
        qp.drawRect((self.PP1x+self.PP2x)/2, self.PP2y,20, 20)

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
    def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
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

        resized = cv2.resize(image, dim, interpolation = inter)
        return resized

    """
    - This function is used to check if the 2 functions intersecting or not.
    - Arguments are the different Objects containg the x-axis and y-axis of the bounding boxes's coordinates.
    - Returns true if the there's intersection else true
    """
    def do_overlap(self,O1 , O2):
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
    - this is the function used to check if the date given is today's.
    - Argument is the date.
    - returns the Boolean.
    """
    def verifyDate(self,date):
        t = time.localtime()
        return (str(t[2])+"/"+str(t[1])+"/"+str(t[0])) == date

    """
    Code for detections and conditions
    By running the video frame 1 by 1 using while loop
    """
    #RDict['CAR'] = {'p1': Point(9, 9), 'p2': Point(10, 10), 'C': 1, 'count': 0}
    #RDict['PERSON'] = {'p1': Point(9, 9), 'p2': Point(10, 10), 'C': 1, 'count': 0}


    def simulate(self):
        # reading frame and success of the frame
        ret, frame = self.cap.read()
        #if successful then checking conditions
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
                        cv2.putText(img, "CAR DOOR OPEN", (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

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
                        cv2.putText(img, "CAR DOOR OPEN", (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

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
                self.RDict['TOOL'] = {'p1': Point(obj[0], obj[1]), 'p2': Point(obj[2], obj[3]), 'C': obj[4] , 'count' : toolCount}
                toolCount+=1

                # Checking if the CAR is in frame and the PERSON is also there
                if 'CAR' in keys and 'PERSON' in keys:
                    # checking if the person is intersecting with the tools or not
                    if self.do_overlap(self.RDict['TOOL'], self.RDict['PERSON']) and self.do_overlap(self.RDict['TOOL'], self.RDict['CAR']):
                        # if intersecting then saying 'someone is trying to breakin"
                        cv2.putText(img, "SOMEONE IS BREAKING IN THE CAR", (25, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255), 3, cv2.LINE_4)

            keys = self.RDict.keys()

            # Checking if the car is in frame + person is also present + if car door is open or not + is today the checkin date or not
            if 'CAR' in keys and 'PERSON' in keys and CarDoorOpen and not self.verifyDate("4/2/2023"):
                # if car and person is overlaping then saying its 'manual robbery'
                if self.do_overlap(self.RDict['CAR'], self.RDict['PERSON']):
                    cv2.putText(img, "MANUAL ROBBERY", (25, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)

            # if tool and person is intersecting then saying 'potential robbery'
            if 'PERSON' in keys and 'TOOL' in keys and self.do_overlap(self.RDict['TOOL'], self.RDict['PERSON']):
                cv2.putText(img, "POTENTIAL ROBBERY", (25, 230), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_4)

            # displaying the frame
            cv2.imshow('YOLO',self.image_resize(img,width=1000))


            if 'CAR' in keys and 'PERSON' in keys:
                pass





app = QApplication(sys.argv)
ex = Snake()
sys.exit(app.exec_())
