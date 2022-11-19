from tkinter import *
from PIL import Image, ImageTk
import psycopg2
import json
from tkinter import messagebox
import random
from tkcalendar import Calendar


class Main:
    # Creating the window
    master = Tk()
    backgroundColor = "#A49B96"
    foregroundColor = "#D3D0CF"
    textColor = "#ffffff"
    # Getting the windows sizes
    winHeight = master.winfo_screenheight()
    winWidth = master.winfo_screenwidth()

    # Loading images for the GUI
    coverImg = Image.open("images/Cover-pic.png").resize((int(winWidth * 0.8), int(winHeight * 0.8)))
    renderCover = ImageTk.PhotoImage(coverImg)
    perImg = Image.open("images/per.png").resize((int(winHeight * 0.06), int(winHeight * 0.064)))
    renderPerson = ImageTk.PhotoImage(perImg)
    perLogout = Image.open("images/log.png").resize((int(winHeight * 0.06), int(winHeight * 0.06)))
    renderLogout = ImageTk.PhotoImage(perLogout)
    perBook = Image.open("images/book.png").resize((int(winHeight * 0.06), int(winHeight * 0.06)))
    renderBook = ImageTk.PhotoImage(perBook)

    # Creating labels font
    headerFont = ("Calibre", int(winHeight / 15), "bold")
    buttonFont = ("Calibre", int(winHeight / 50))
    simpleTextFont = ("Calibre", int(winHeight / 45), "bold")
    simpleTextFont2 = ("Calibre", int(winHeight / 50))
    textEntryFont = ("Calibre", int(winHeight / 60))

    #
    labelInterfaceOne = Label(master, image=renderCover)
    #
    labelOne = Label(master, bg=foregroundColor, fg=textColor, text="Login", font=headerFont)
    labelTwo = Label(master, bg=foregroundColor, fg=textColor, text="USERNAME", font=simpleTextFont)
    labelThree = Label(master, bg=foregroundColor, fg=textColor, text="PASSWORD",
                       font=simpleTextFont)
    labelFour = Label(master, bg=foregroundColor, fg=textColor, text="FIRST NAME",
                      font=simpleTextFont)
    labelFive = Label(master, bg=foregroundColor, fg=textColor, text="LAST NAME",
                      font=simpleTextFont)
    #
    textEntryOne = Text(master, font=textEntryFont, bg="white", bd=0)
    textEntryTwo = Text(master, font=textEntryFont, bg="white", bd=0)
    textEntryThree = Text(master, font=textEntryFont, bg="white", bd=0)
    textEntryFour = Text(master, font=textEntryFont, bg="white", bd=0)
    password = Entry(master, font=textEntryFont, bg="white", bd=0, show="*")

    # Creating the front Calendar
    calender = Calendar(master, selectmode='day', year=2020, month=5, day=22)

    # Creating Buttons
    buttonOne = Button(master, bg=backgroundColor, fg=textColor, text="Login", borderwidth=0,
                       font=buttonFont)
    buttonTwo = Button(master, bg=backgroundColor, fg=textColor, text="Register", borderwidth=0,
                       font=buttonFont, )
    buttonThree = Button(master, image=renderLogout, borderwidth=0, font=buttonFont, bd=0,
                         highlightthickness=0, )
    buttonFour = Button(master, image=renderBook, borderwidth=0, font=buttonFont, bd=0, highlightthickness=0)
    buttonFive = Button(master, image=renderPerson, borderwidth=0, font=buttonFont, bd=0, highlightthickness=0, )
    buttonSix = Button(master, bg=backgroundColor, fg=textColor, text="Select", borderwidth=0,
                       font=buttonFont, )
    buttonSeven = Button(master, bg=backgroundColor, fg=textColor, text="Select", borderwidth=0,
                         font=buttonFont, )

    cur = None

    global username
    username = ""









    def __init__(self):
        # Getting the size of the screen and removing 100 pixels from it to make a bit smaller
        self.master.geometry("{1}x{0}+2+5".format(self.winHeight - 100, self.winWidth - 100))
        self.master.resizable(0, 0)
        self.master.configure(bg=self.backgroundColor)
        # destroy the window if "Escape key is pressed"
        self.master.bind("<Escape>", self.killWindow)

        self.placeLoginPage()

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


        try:
            self.createDB()
        except:
            pass

        self.master.mainloop()

    # Methods to perform task when window is destroyed
    def killWindow(self, event):
        self.master.destroy()  # destroying the window

    # Creating the login page
    def placeLoginPage(self):
        self.labelOne.config(text="Login")
        self.labelTwo.config(text="USERNAME")
        self.labelThree.config(text="PASSWORD")

        self.buttonOne.config(text="Login", command=lambda: [self.verifyLogin(self.textEntryTwo, self.password)])
        self.buttonTwo.config(text="Register", command=lambda: [self.removeLoginPage(), self.placeSignupPage()])
        # Placing the Labels,Buttons,Text boxes of login page
        self.labelInterfaceOne.place(relx=0.1, rely=0.1)
        self.labelOne.place(relx=0.63, rely=0.22, relheight=0.1, relwidth=0.2)
        self.labelTwo.place(relx=0.63, rely=0.41, relheight=0.03, relwidth=0.2)
        self.labelThree.place(relx=0.63, rely=0.55, relheight=0.03, relwidth=0.2)
        self.buttonTwo.place(relx=0.7, rely=0.8, relheight=0.05, relwidth=0.08)
        self.buttonOne.place(relx=0.8, rely=0.8, relheight=0.05, relwidth=0.08)
        self.textEntryTwo.place(relx=0.58, rely=0.46, relheight=0.04, relwidth=0.3)
        self.password.place(relx=0.58, rely=0.61, relheight=0.04, relwidth=0.3)

    # Creating the method to remove the elements before moving to the next "page"
    def removeLoginPage(self):
        self.password.delete(0, "end")
        self.textEntryOne.delete("1.0", "end")
        self.textEntryTwo.delete("1.0", "end")
        self.textEntryThree.delete("1.0", "end")
        self.textEntryFour.delete("1.0", "end")

        self.password.place_forget()
        self.labelInterfaceOne.place_forget()
        self.labelOne.place_forget()
        self.labelTwo.place_forget()
        self.labelThree.place_forget()
        self.buttonTwo.place_forget()
        self.buttonOne.place_forget()
        self.textEntryTwo.place_forget()
        self.textEntryOne.place_forget()

    def placeSignupPage(self):
        self.labelOne.config(text="Signup")
        self.labelTwo.config(text="USERNAME")
        self.labelThree.config(text="PASSWORD")
        self.labelFour.config(text="FIRST NAME")
        self.labelFive.config(text="LAST NAME")
        self.buttonOne.config(text="Save Info",command=lambda :[self.addProfile(self.textEntryOne,self.textEntryTwo,self.textEntryThree,self.textEntryFour)])

        # Placing the Labels,Buttons,Text boxes of Signup page
        self.labelInterfaceOne.place(relx=0.1, rely=0.1)
        self.labelOne.place(relx=0.63, rely=0.12, relheight=0.1, relwidth=0.2)
        self.labelFour.place(relx=0.63, rely=0.29, relheight=0.03, relwidth=0.2)
        self.labelFive.place(relx=0.63, rely=0.4, relheight=0.03, relwidth=0.2)
        self.labelTwo.place(relx=0.63, rely=0.51, relheight=0.03, relwidth=0.2)
        self.labelThree.place(relx=0.63, rely=0.62, relheight=0.03, relwidth=0.2)
        self.buttonOne.place(relx=0.8, rely=0.8, relheight=0.05, relwidth=0.08)
        self.textEntryOne.place(relx=0.58, rely=0.338, relheight=0.04, relwidth=0.3)
        self.textEntryTwo.place(relx=0.58, rely=0.448, relheight=0.04, relwidth=0.3)
        self.textEntryThree.place(relx=0.58, rely=0.558, relheight=0.04, relwidth=0.3)
        self.textEntryFour.place(relx=0.58, rely=0.668, relheight=0.04, relwidth=0.3)


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
                self.removeSignupPage()
                self.placeLoginPage()
            else:
                # showing error message if primary key "Username already exists in the person table"
                messagebox.showinfo("showinfo", "Username already exists!")
        else:
            # showing error message in case any field is empty
            messagebox.showinfo("showinfo", "Fields are empty! All fields must be filled.")

    def verifyLogin(self, entryOne, entryTwo):
        global username
        if entryOne.get("1.0", "end-1c") != "" and entryTwo.get() != "":
            username = str(entryOne.get("1.0", "end-1c"))
            # Query to check if user exist
            self.cur.execute("SELECT username,pass FROM PERSON WHERE (USERNAME ='" + str(
                entryOne.get("1.0", "end-1c")) + "' and PASS= '" + str(entryTwo.get()) + "');")
            if len(self.cur.fetchall()) > 0:
                self.removeLoginPage()
                self.placeBookingPage()
            else:
                # showing error message if user not found
                messagebox.showinfo("showinfo", "No User Found! New user?")
        else:
            # showing error message in case any field is empty
            messagebox.showinfo("showinfo", "Fields are Empty! Password and username required.")





# Calling the Main class that contain the GUI and DBS commands
m = Main()
