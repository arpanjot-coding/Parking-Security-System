from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from firebase_admin import db,storage
import os
import easyocr
import cv2
from Points import Point
import numpy as np
import time

class MainSimulation(QWidget):
    def __init__(self, m1, m2, m3, msg, name, d):
        super(MainSimulation, self).__init__()
        self.RDict = {}
        self.setFixedSize(550, 400)
        # Loding the modelling files
        try:
            os.mkdir('test')
        except:
            pass

        self.userData = d
        self.model1 = m1
        self.model2 = m2
        self.model3 = m3
        self.msg = msg
        self.reader = easyocr.Reader(['en'])
        self.name = name
        self.n2d = True
        self.videoSet = False
        self.MsgSent = False
        self.MsgSent2 = False
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
        self.drawHomograph(qp)
        qp.end()

    def setRdict(self, r):
        self.RDict = r

    # Not default method.
    def newGame(self):
        self.timer = QBasicTimer()
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
    def drawHomograph(self, qp):
        # for car
        qp.setPen(Qt.NoPen)
        qp.setBrush(QColor(255, 80, 0, 255))
        qp.drawRect(self.CP1x, self.CP1y, self.CP2x, self.CP2y)
        # for person
        qp.setBrush(QColor(50, 255, 0, 255))
        qp.drawRect(self.PP1x, self.PP1y, self.PP2x, self.PP2y)

    # Default method name
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            # The code bellow is used to
            self.update()
            self.repaint()
        else:
            QFrame.timerEvent(self, event)

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

        cv2.imwrite("test/n.jpg", cv2.flip(frame, 1))
        output = ""#self.reader.readtext("test/n.jpg")

        print(output)
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

    def simulate(self, frame, msg, ret=True):
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
            WarningFrame = False
            numberPlate = ""
            # count the number of cars available or person etc...
            carCount = 1
            personCount = 1
            numberPlateCount = 1
            toolCount = 1
            securityCount = 1
            warns = []

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
                        # cv2.putText(img, "CAR DOOR OPEN", (25, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_4)
                        self.MsgSent = True
                        WarningFrame = True
                        warns.append("DOOR OPEN")
                        msg.addMessage("Tab " + self.name + " : CAR DOOR OPEN", "red")

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
                        self.MsgSent = True
                        WarningFrame = True
                        warns.append("DOOR OPEN")
                        msg.addMessage(f"Tab {self.name} : CAR DOOR OPEN", "red")

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
                        self.MsgSent = True
                        WarningFrame = True
                        warns.append("BREAK IN")
                        msg.addMessage("Tab " + self.name + " : SOMEONE IS BREAKING IN THE CAR", "red")

            keys = self.RDict.keys()

            # Checking if the car is in frame + person is also present + if car door is open or not + is today the checkin date or not
            if 'CAR' in keys and 'PERSON' in keys and CarDoorOpen and not self.verifyDate("4/2/2023"):
                # if car and person is overlaping then saying its 'manual robbery'
                if self.do_overlap(self.RDict['CAR'], self.RDict['PERSON']):
                    self.MsgSent = True
                    WarningFrame = True
                    warns.append("MANUAL")
                    msg.addMessage("Tab " + self.name + " : MANUAL ROBBERY", "red")

            # if tool and person is intersecting then saying 'potential robbery'
            if 'PERSON' in keys and 'TOOL' in keys and self.do_overlap(self.RDict['TOOL'], self.RDict['PERSON']):
                self.MsgSent = True
                WarningFrame = True
                warns.append("POTENTIAL")
                msg.addMessage("Tab " + self.name + " : POTENTIAL ROBBERY", "blue")

            # displaying the frame
            # cv2.imshow('YOLO',self.image_resize(img,width=1000))

            # if number plate is in frame then geting the number from number plate
            if 'PLATE' in keys:
                numberPlate = self.getNumberPlate(frame, self.RDict['PLATE'])
                # numberPlate = "EA11 URS"

            if self.MsgSent and not self.MsgSent2:
                cv2.imwrite("test/not.jpg", frame)
                fileName = r"test/not.jpg"
                bucket = storage.bucket()
                blob = bucket.blob(fileName)
                blob.upload_from_filename(fileName)
                blob.make_public()
                self.MsgSent2 = True

                for i in self.userData:
                    if numberPlate == self.userData[i]['NP']:
                        msg.addMessage("Tab " + self.name + " : Sending Message to user: " + i, "blue")
                        data = {
                            "uId": i,
                            "message": "Your car is being stolen",
                            "numPlate": self.userData[i]['NP'],
                            "image": blob.public_url,
                            "time": 1675538430872,
                            "read": False
                        }
                        alertRef = db.reference('Alerts').child('for users').child(i)
                        alertRef.set(data)
                        break

            # self.msg.resetMessages()
            return img,list(warns),WarningFrame

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
