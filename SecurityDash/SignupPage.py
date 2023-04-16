from PyQt5.QtWidgets import *

class CreateAccScreen(QDialog):
    def __init__(self, back_to_login_callback, widget, model1, model2, model3, userData):
        super(CreateAccScreen, self).__init__()
        self.setWindowTitle("Sign up")
        self.widget = widget

        # Add these lines to store the additional parameters
        self.model1 = model1
        self.model2 = model2
        self.model3 = model3
        self.userData = userData

        layout = QVBoxLayout()

        self.usern = QLineEdit()
        self.usern.setPlaceholderText("Username")
        layout.addWidget(self.usern)

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Password")
        self.passw.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passw)

        self.passw2 = QLineEdit()
        self.passw2.setPlaceholderText("Confirm Password")
        self.passw2.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passw2)

        self.SIGNUP = QPushButton("Sign up")
        self.SIGNUP.clicked.connect(self.signupfunction)  # Change this line
        layout.addWidget(self.SIGNUP)

        self.BACK = QPushButton("Back to login")
        self.BACK.clicked.connect(back_to_login_callback)
        layout.addWidget(self.BACK)

        self.error = QLabel("")
        layout.addWidget(self.error)

        self.setLayout(layout)

    def back_to_login(self):
        login_page = WelcomeScreen(goto_create, widget, self.model1, self.model2, self.model3, self.userData)
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def signupfunction(self):
        user = self.usern.text()
        password = self.passw.text()
        confirmpassword = self.passw2.text()

        if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0:
            self.error.setText("Please fill in all inputs.")
        else:
            # Call the back_to_login_callback function instead of self.back_to_login()
            self.back_to_login_callback()

