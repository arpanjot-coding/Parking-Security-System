from PyQt5.QtWidgets import *
from dashboard import MyTableWidget
from SignupPage import CreateAccScreen

class WelcomeScreen(QDialog):
    def __init__(self, goto_create_callback, widget, model1, model2, model3, userData):
        super(WelcomeScreen, self).__init__()
        self.setWindowTitle("Login")
        self.widget = widget

        self.u = 'admin'
        self.p = 'admin'


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

        self.LOGIN = QPushButton("Login")
        self.LOGIN.clicked.connect(self.loginfunction)
        layout.addWidget(self.LOGIN)

        self.SIGNUP = QPushButton("Sign up")
        self.SIGNUP.clicked.connect(goto_create_callback)
        layout.addWidget(self.SIGNUP)

        self.error = QLabel("")
        layout.addWidget(self.error)

        self.setLayout(layout)

    def loginfunction(self):
        user = self.usern.text()
        password = self.passw.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all fields.")
        else:
            if user == self.u and self.p == password:
                print("Successfully logged in.")
                dashboard = MyTableWidget(self.widget, self.model1, self.model2, self.model3, self.userData)
                self.widget.addWidget(dashboard)
                self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
            else:
                self.error.setText("Invalid username or password")



