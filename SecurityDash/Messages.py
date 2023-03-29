from PyQt5.QtWidgets import *

class ErrorWidget(QWidget):
    def __init__(self):
        super(ErrorWidget, self).__init__()
        self.setFixedHeight(200)
        self.setStyleSheet("background-color:rgb(255, 255, 255);")
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
            self.tabs[self.tabCount].setStyleSheet("color: " + color)
            self.tabs[self.tabCount].setText(str(y + x))
            self.tabCount = (self.tabCount + 1) % 8

    def verifyInput(self, msg):
        for i in range(len(self.tabs)):
            if msg == self.tabs[i].text():
                return False
        return True
