from tkinter import *
import psycopg2
import json
import random
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




    class Table:
        def __init__(self, root, lst):
            totalRows = len(lst)
            totalColumns = len(lst[0])
            # code for creating table
            for i in range(totalRows):
                for j in range(totalColumns):
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

    def addBookings(self, entryOne, entryTwo, entryThree):
        if entryOne.get("1.0", "end-1c") != "" and entryTwo.get("1.0", "end-1c") != "" and entryThree.get("1.0", "end-1c") != "":
            try:
                self.cur.execute("INSERT INTO BOOKING (BID,NUMBER,CHECKIN,CHECKOUT,USERNAME) \
                      VALUES (" + str(random.randint(1, 1000)) + ",'" + entryOne.get("1.0", "end-1c") + "', '" + entryTwo.get("1.0",
                                                                                                                  "end-1c") + "' , '" + entryThree.get(
                    "1.0", "end-1c") + "', '" + username + "' );")
                messagebox.showinfo("showinfo", "Booking Complete!")
                # Removing the text from Text widgets
                entryOne.delete("1.0", "end")
                entryTwo.delete("1.0", "end")
                entryThree.delete("1.0", "end")
            except:
                # showing error because of any possible error and Booking failed.
                messagebox.showinfo("showinfo", "Booking failed!")
        else:
            # showing error message in case any field is empty
            messagebox.showinfo("showinfo", "Fields are empty! All fields must be filled.")
        return

    def addProfile(self, entryOne, entryTwo, entryThree, entryFour):
        if entryOne.get("1.0", "end-1c") != "" and entryTwo.get("1.0", "end-1c") != "" and entryThree.get("1.0", "end-1c") != "" and entryFour.get(
                "1.0", "end-1c") != "":
            # Query for getting if username exists
            self.cur.execute("SELECT username,pass FROM PERSON WHERE (USERNAME ='" + str(entryThree.get("1.0", "end-1c")) + "');")
            if len(self.cur.fetchall()) == 0:
                # Registering the profile
                self.cur.execute("INSERT INTO PERSON (FNAME,LNAME,PASS,USERNAME) \
                      VALUES ('" + entryOne.get("1.0", "end-1c") + "', '" + entryTwo.get("1.0", "end-1c") + "' , '" + entryFour.get("1.0",
                                                                                                                 "end-1c") + "', '" + entryThree.get(
                    "1.0", "end-1c") + "' );")
                # Moving to the Login page if registration is successful
                removeSignupPage()
                placeLoginPage()
            else:
                # showing error message if primary key "Username already exists in the person table"
                messagebox.showinfo("showinfo", "Username already exists!")
        else:
            # showing error message in case any field is empty
            messagebox.showinfo("showinfo", "Fields are empty! All fields must be filled.")