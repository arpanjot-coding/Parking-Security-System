from tkinter import *
import psycopg2
import json
from tkinter import messagebox



class main:
    winHeight = None
    winWidth = None

    BackgroundColor = "#A49B96"
    ForegroundColor = "#D3D0CF"
    textColor = "#ffffff"

    HeaderFont = ("Calibre", int(winHeight / 15), "bold")
    ButtonFont = ("Calibre", int(winHeight / 50))
    simpleTextFont = ("Calibre", int(winHeight / 45), "bold")
    simpleTextFont2 = ("Calibre", int(winHeight / 50))
    TextEntryFont = ("Calibre", int(winHeight / 60))

    cur = None


    def __init__(self,winHeight,winWidth):
        self.winHeight = winHeight
        self.winWidth = winWidth

        # Opening the DB credential file
        with open("files/configSettings.json", 'r') as f:  # Opening the settings file
            configData = json.load(f)
            configJsonData = configData

        try:
            # opening the database
            conn = psycopg2.connect(database=configJsonData["database"], user=configJsonData["user"],
                                    password=configJsonData["password"], host=configJsonData["host"],
                                    port=configJsonData["port"])
            self.cur = conn.cursor()
        except:
            messagebox.showinfo("showinfo",
                                "Database connection failed!\nCheck \"IP,Database name, User, password\" From settings")

        global username
        username = ""

        try:
            self.createDB()
        except:
            pass


    class Table:
        def __init__(self, root, lst):
            total_rows = len(lst)
            total_columns = len(lst[0])
            # code for creating table
            for i in range(total_rows):
                for j in range(total_columns):
                    if i == 0:
                        self.e = Entry(root, width=20, bg=self.backgroundColor, fg=self.textColor, font=self.simpleTextFont2,
                                       justify=CENTER)
                        self.e.grid(row=i, column=j)
                    else:
                        self.e = Entry(root, width=20, fg=self.backgroundColor, bg=self.textColor, font=self.simpleTextFont2,
                                       justify=CENTER)
                        self.e.grid(row=i, column=j)
                    self.e.insert(END, lst[i][j])

    def createDB(self):
        # Creating the tables in database
        self.cur.execute('''CREATE TABLE PERSON
              (FNAME           VARCHAR(30)    NOT NULL,
              LNAME           VARCHAR(30)    NOT NULL,
              PASS            VARCHAR(30)     NOT NULL,
              USERNAME        VARCHAR(30)  PRIMARY KEY   NOT NULL
              );
              ''')
        self.cur.execute('''CREATE TABLE BOOKING
                  (BID INT PRIMARY KEY  NOT NULL,
                  NUMBER INT NOT NULL,
                  CHECKIN VARCHAR(30) NOT NULL,
                  CHECKOUT VARCHAR(30) NOT NULL,
                  USERNAME VARCHAR(30) NOT NULL,
                  CONSTRAINT FK_PERSON FOREIGN KEY(USERNAME) REFERENCES PERSON(USERNAME)
                  );
                  ''')