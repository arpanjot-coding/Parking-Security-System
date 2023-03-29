from PyQt5.QtWidgets import *
from SignupPage import CreateAccScreen

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
