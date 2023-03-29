from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

class Worker(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def setVideoMask(self, video, n, msg):
        self.video = video
        self.op = n
        self.msg = msg

    def run(self):
        self.ThreadActive = True

        Capture = cv2.VideoCapture(self.op)

        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                FlippedImage = self.video.simulate(FlippedImage, self.msg)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0],
                                           QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False
        self.quit()
