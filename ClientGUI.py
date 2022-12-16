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
    winHeight = master.winfo_screenheight()-100
    winWidth = master.winfo_screenwidth()-100

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


    global username
    username = ""

    class Table:

        def __init__(self, root, lst):
            totalRows = len(lst)
            totalColumns = len(lst[0])
            # code for creating table
            for i in range(totalRows):
                for j in range(totalColumns):
                    if i == 0:
                        self.e = Entry(root, width=20, bg=Main.backgroundColor, fg=Main.textColor,
                                       font=Main.simpleTextFont2,
                                       justify=CENTER)
                        self.e.grid(row=i, column=j)
                    else:
                        self.e = Entry(root, width=20, fg=Main.backgroundColor, bg=Main.textColor,
                                       font=Main.simpleTextFont2,
                                       justify=CENTER)
                        self.e.grid(row=i, column=j)
                    self.e.insert(END, lst[i][j])

    def __init__(self):
        # Getting the size of the screen and removing 100 pixels from it to make a bit smaller
        self.master.geometry("{1}x{0}+2+5".format(self.winHeight, self.winWidth))
        self.master.resizable(0, 0)
        self.master.configure(bg=self.backgroundColor)
        # destroy the window if "Escape key is pressed"
        self.master.bind("<Escape>", self.killWindow)

        self.buttonOne = Button(self.master, bg=Main.backgroundColor, fg=Main.textColor, text="Login", borderwidth=0, font=Main.buttonFont)
        self.buttonTwo = Button(self.master, bg=Main.backgroundColor, fg=Main.textColor, text="Register", borderwidth=0, font=Main.buttonFont,
                           command=lambda: [self.removeLoginPage(), self.placeSignupPage()])
        self.buttonThree = Button(self.master, image=Main.renderLogout, borderwidth=0, font=Main.buttonFont, bd=0, highlightthickness=0,
                             command=lambda: [self.removeBookingPage(), self.placeLoginPage()])
        self.buttonSeven = Button(self.master, image=Main.renderBook, borderwidth=0, font=Main.buttonFont, bd=0, highlightthickness=0)
        self.buttonFour = Button(self.master, image=Main.renderPerson, borderwidth=0, font=Main.buttonFont, bd=0, highlightthickness=0,
                            command=lambda: [self.removeBookingPage(), self.placePersonalPage()])
        self.buttonFive = Button(self.master, bg=Main.backgroundColor, fg=Main.textColor, text="Select", borderwidth=0, font=Main.buttonFont,
                            command=lambda: [self.showCalender(self.textEntryTwo)])
        self.buttonSix = Button(self.master, bg=Main.backgroundColor, fg=Main.textColor, text="Select", borderwidth=0, font=Main.buttonFont,
                           command=lambda: [self.showCalender(self.textEntryThree)])

        # Opening the DB credential file
        with open("files/configSettings.json", 'r') as f:  # Opening the settings file
            configData = json.load(f)
            configJsonData = configData

        try:
            # opening the database
            self.conn = psycopg2.connect(database=configJsonData["database"], user=configJsonData["user"],
                                    password=configJsonData["password"], host=configJsonData["host"],
                                    port=configJsonData["port"])
            self.cur = self.conn.cursor()
        except:
            messagebox.showinfo("showinfo",
                                "Database connection failed!\nCheck \"IP,Database name, User, password\" From settings")
        try:
            self.createDB()
        except:
            pass

        self.placeLoginPage()
        self.conn.commit()
        self.master.mainloop()

    # Methods to perform task when window is destroyed
    def killWindow(self, event):
        self.conn.commit()
        self.conn.close()
        self.master.destroy()  # destroying the window
        # Creating Buttons


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

    def removeSignupPage(self):
        self.textEntryOne.delete("1.0", "end")
        self.textEntryTwo.delete("1.0", "end")
        self.textEntryThree.delete("1.0", "end")
        self.textEntryFour.delete("1.0", "end")

        self.labelInterfaceOne.place_forget()
        self.labelOne.place_forget()
        self.labelTwo.place_forget()
        self.labelThree.place_forget()
        self.labelFive.place_forget()
        self.labelFour.place_forget()
        self.buttonTwo.place_forget()
        self.buttonOne.place_forget()
        self.textEntryOne.place_forget()
        self.textEntryTwo.place_forget()
        self.textEntryThree.place_forget()
        self.textEntryFour.place_forget()

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
            self.cur.execute("SELECT USERNAME, PASS FROM PERSON WHERE (USERNAME ='" + str(entryOne.get("1.0", "end-1c")) + "' and PASS= '" + str(entryTwo.get()) +"');")
            if len(self.cur.fetchall()) > 0:
                ...
                self.removeLoginPage()
                self.placeBookingPage()
            else:
                # showing error message if user not found
                messagebox.showinfo("showinfo", "No User Found! New user?")
        else:
            # showing error message in case any field is empty
            messagebox.showinfo("showinfo", "Fields are Empty! Password and username required.")

    def getPersonalInfo(self):
        # Query to get all the user personal data
        self.cur.execute(
            "SELECT * FROM PERSON WHERE (USERNAME ='" + username + "');")
        return self.cur.fetchall()[0]

    def getBookingDetails(self):
        # Returning the User's booking data in form of string
        self.cur.execute("SELECT * FROM BOOKING WHERE (USERNAME ='" + username + "');")
        x = [("ID", "Number", "Checkin date", "Checkout date", "Username")]
        x.extend(self.cur.fetchall())
        return x


    def UpdatePersonalInfo(self,E1,E2,E4):
        E1 = E1.get("1.0", "end-1c")
        E2 = E2.get("1.0", "end-1c")
        E4 = E4.get("1.0", "end-1c")

        root = Tk()
        root.geometry("300x100+2+5")
        root.title("Verify Old password to save for " + username)

        oldPas = Entry(root,show="*")
        oldPas.place(relx=0.1,rely=0.2,relwidth=0.8,relheight=0.2)
        ppb = Button(root,text="Enter Password",command=lambda:[self.saveProfile(E1,E2,oldPas,E4),root.destroy()])
        ppb.place(relx=0.1,rely=0.6,relwidth=0.8,relheight=0.2)
        root.mainloop()

    def placeBookingPage(self):
        self.labelOne.config(text="Booking")
        self.labelFour.config(text="Number")
        self.labelFive.config(text="Checkin Date")
        self.labelTwo.config(text="Checkout Date")
        self.buttonSeven.config(command=lambda: [self.showBookings(self.getBookingDetails())])
        self.buttonOne.config(text="Book", command=lambda: [self.addBookings(self.textEntryOne, self.textEntryTwo, self.textEntryThree)])

        # Placing the Labels,Buttons,Text boxes of Booking page
        self.labelInterfaceOne.place(relx=0.1, rely=0.1)
        self.buttonThree.place(relx=0.86, rely=0.109)
        self.buttonFour.place(relx=0.82, rely=0.109)
        self.buttonSeven.place(relx=0.77, rely=0.109)
        self.labelOne.place(relx=0.63, rely=0.22, relheight=0.1, relwidth=0.2)
        self.labelFour.place(relx=0.63, rely=0.345, relheight=0.03, relwidth=0.2)
        self.labelFive.place(relx=0.63, rely=0.467, relheight=0.03, relwidth=0.2)
        self.labelTwo.place(relx=0.63, rely=0.585, relheight=0.03, relwidth=0.2)
        self.buttonOne.place(relx=0.8, rely=0.8, relheight=0.05, relwidth=0.08)
        self.textEntryOne.place(relx=0.58, rely=0.39, relheight=0.04, relwidth=0.3)
        self.textEntryTwo.place(relx=0.58, rely=0.51, relheight=0.04, relwidth=0.22)
        self.buttonFive.place(relx=0.8, rely=0.51, relheight=0.04, relwidth=0.08)
        self.textEntryThree.place(relx=0.58, rely=0.63, relheight=0.04, relwidth=0.3)
        self.buttonSix.place(relx=0.8, rely=0.63, relheight=0.04, relwidth=0.08)

    def saveProfile(self,E1, E2, E3, E4):
        E3 = E3.get()
        self.cur.execute("SELECT PASS FROM PERSON WHERE (USERNAME ='" + str(username) + "');")
        pas = list(self.cur.fetchall()[0])[0]

        if E3 != "" and E4 != "" and E3 == str(pas) and E3 != E4:
            self.cur.execute("UPDATE PERSON SET PASS = '" + str(E4) + "' WHERE USERNAME = '" + username + "';")

        if E1 != "" and E2 != "":
            self.cur.execute("UPDATE PERSON SET FNAME = '" + str(E1) + "' WHERE USERNAME = '" + username + "';")
            self.cur.execute("UPDATE PERSON SET LNAME = '" + str(E2) + "' WHERE USERNAME = '" + username + "';")

        self.removePersonalPage()
        self.placeBookingPage()

    def placePersonalPage(self):
        b, c, d, e = self.getPersonalInfo()

        self.labelOne.config(text="Personal Info.")
        self.labelFive.config(text="First Name")
        self.labelTwo.config(text="Last Name")
        self.labelFour.config(text=str(e), font=("Calibre", int(self.winHeight / 30), "bold"), fg="#A49B96")
        self.labelThree.config(text="Password")

        self.textEntryOne.insert(END, b)
        self.textEntryTwo.insert(END, c)
        self.textEntryThree.insert(END, "")

        self.buttonOne.config(text="Save", command=lambda: [self.UpdatePersonalInfo(self.textEntryOne, self.textEntryTwo, self.textEntryThree)])

        # Placing the Labels,Buttons,Text boxes of personal Info page
        self.labelInterfaceOne.place(relx=0.1, rely=0.1)
        self.labelOne.place(relx=0.5, rely=0.2, relheight=0.1, relwidth=0.4)
        self.labelFour.place(relx=0.525, rely=0.32, relheight=0.06, relwidth=0.35)
        self.labelFive.place(relx=0.525, rely=0.4, relheight=0.06, relwidth=0.35)
        self.labelTwo.place(relx=0.525, rely=0.5, relheight=0.06, relwidth=0.35)
        self.labelThree.place(relx=0.525, rely=0.6, relheight=0.07, relwidth=0.35)

        self.textEntryOne.place(relx=0.525, rely=0.45, relheight=0.04, relwidth=0.35)
        self.textEntryTwo.place(relx=0.525, rely=0.55, relheight=0.04, relwidth=0.35)
        self.textEntryThree.place(relx=0.525, rely=0.657, relheight=0.04, relwidth=0.35)

        self.buttonOne.place(relx=0.79, rely=0.845, relheight=0.05, relwidth=0.08)

    def removePersonalPage(self):
        self.textEntryOne.delete("1.0", "end")
        self.textEntryTwo.delete("1.0", "end")
        self.textEntryThree.delete("1.0", "end")
        self.textEntryFour.delete("1.0", "end")
        self.labelFour.config(font=Main.simpleTextFont, fg=Main.textColor)
        self.buttonTwo.place_forget()
        self.labelThree.config(bg="#D3D0CF", fg=Main.textColor, anchor=CENTER)
        self.labelInterfaceOne.place_forget()
        self.labelOne.place_forget()
        self.buttonThree.place_forget()
        self.labelFour.place_forget()
        self.labelFive.place_forget()
        self.labelTwo.place_forget()
        self.labelThree.place_forget()
        self.textEntryFour.place_forget()
        self.buttonOne.place_forget()

    def showBookings(self,lst):
        root = Tk()
        root.title("Bookings of " + username)
        self.Table(root, lst)
        root.mainloop()

    def removeBookingPage(self):

        self.textEntryOne.delete("1.0", "end")
        self.textEntryTwo.delete("1.0", "end")
        self.textEntryThree.delete("1.0", "end")
        self.textEntryFour.delete("1.0", "end")

        self.labelInterfaceOne.place_forget()
        self.labelOne.place_forget()
        self.labelFour.place_forget()
        self.labelFive.place_forget()
        self.labelTwo.place_forget()
        self.buttonOne.place_forget()
        self.buttonThree.place_forget()
        self.buttonSeven.place_forget()
        self.buttonFour.place_forget()
        self.textEntryOne.place_forget()
        self.buttonFive.place_forget()
        self.buttonSix.place_forget()
        self.textEntryTwo.place_forget()
        self.textEntryThree.place_forget()
        self.textEntryFour.place_forget()

    def Setdate(self,E):
        E.insert(END, str(self.calender.get_date()))
        self.calender.place_forget()
        self.buttonOne.place_forget()
        self.buttonOne.config(text="Book", command=lambda: [self.addBookings(self.textEntryOne, self.textEntryTwo, self.textEntryThree)])
        self.buttonOne.place(relx=0.8, rely=0.8, relheight=0.05, relwidth=0.08)

    def showCalender(self,E):
        self.buttonOne.config(text="Save date!", command=lambda: [self.Setdate(E)])
        self.calender.place(relx=0.13, rely=0.3, relheight=0.4, relwidth=0.3)
        self.buttonOne.place(relx=0.13, rely=0.7, relheight=0.05, relwidth=0.08)

    def addBookings(self,E1, E2, E3):
        if not (E1.get("1.0", "end-1c").isnumeric()):
            messagebox.showinfo("showinfo", "Database connection failed!\nAlphanumeric not allowed in number field!")

        elif E1.get("1.0", "end-1c") != "" and E2.get("1.0", "end-1c") != "" and E3.get("1.0", "end-1c") != "":
            try:
                self.cur.execute("INSERT INTO BOOKING (BID,NUMBER,CHECKIN,CHECKOUT,USERNAME) \
                      VALUES (" + str(random.randint(1, 1000)) + ",'" + E1.get("1.0", "end-1c") + "', '" + E2.get("1.0",
                                                                                                                  "end-1c") + "' , '" + E3.get(
                    "1.0", "end-1c") + "', '" + username + "' );")
                messagebox.showinfo("showinfo", "Booking Complete!")
                # Removing the text from Text widgets
                E1.delete("1.0", "end")
                E2.delete("1.0", "end")
                E3.delete("1.0", "end")
            except:
                # showing error because of any possible error and Booking failed.
                messagebox.showinfo("showinfo", "Booking failed!")
        else:
            # showing error message in case any field is empty
            messagebox.showinfo("showinfo", "Fields are empty! All fields must be filled.")
        return


# Calling the Main class that contain the GUI and DBS commands
m = Main()
