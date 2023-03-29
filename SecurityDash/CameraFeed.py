from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Worker import Worker

class CameraFeed(QWidget):
    def __init__(self, video, name, msg):
        super(CameraFeed, self).__init__()

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)

        self.Worker1 = Worker()
        if int(name) <= 10:
            filename, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "",
                                                          "All Files (*);;Text Files (*.mp4)")
            if filename != "":
                self.Worker1.setVideoMask(video, filename, msg)
        else:
            self.Worker1.setVideoMask(video, 0, msg)

        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()
