from PyQt5.QtWidgets import *

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

