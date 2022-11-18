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

    def __init__(self):
        # Getting the size of the screen and removing 100 pixels from it to make a bit smaller
        self.master.geometry("{1}x{0}+2+5".format(self.winHeight - 100, self.winWidth - 100))
        self.master.resizable(0, 0)
        self.master.configure(bg=self.backgroundColor)
        # destroy the window if "Escape key is pressed"
        self.master.bind("<Escape>", self.killWindow)

        # Loading images for the GUI
        coverImg = Image.open("images/Cover-pic.png").resize((int(self.winWidth * 0.8), int(self.winHeight * 0.8)))
        renderCover = ImageTk.PhotoImage(coverImg)
        perImg = Image.open("images/per.png").resize((int(self.winHeight * 0.06), int(self.winHeight * 0.064)))
        renderPerson = ImageTk.PhotoImage(perImg)
        perLogout = Image.open("images/log.png").resize((int(self.winHeight * 0.06), int(self.winHeight * 0.06)))
        renderLogout = ImageTk.PhotoImage(perLogout)
        perBook = Image.open("images/book.png").resize((int(self.winHeight * 0.06), int(self.winHeight * 0.06)))
        renderBook = ImageTk.PhotoImage(perBook)

        # Creating labels font
        headerFont = ("Calibre", int(self.winHeight / 15), "bold")
        buttonFont = ("Calibre", int(self.winHeight / 50))
        simpleTextFont = ("Calibre", int(self.winHeight / 45), "bold")
        simpleTextFont2 = ("Calibre", int(self.winHeight / 50))
        textEntryFont = ("Calibre", int(self.winHeight / 60))

        #
        labelInterfaceOne = Label(self.master, image=renderCover)
        #
        labelOne = Label(self.master, bg=self.foregroundColor, fg=self.textColor, text="Login", font=headerFont)
        labelTwo = Label(self.master, bg=self.foregroundColor, fg=self.textColor, text="USERNAME", font=simpleTextFont)
        labelThree = Label(self.master, bg=self.foregroundColor, fg=self.textColor, text="PASSWORD",
                           font=simpleTextFont)
        labelFour = Label(self.master, bg=self.foregroundColor, fg=self.textColor, text="FIRST NAME",
                          font=simpleTextFont)
        labelFive = Label(self.master, bg=self.foregroundColor, fg=self.textColor, text="LAST NAME",
                          font=simpleTextFont)
        #
        textEntryOne = Text(self.master, font=textEntryFont, bg="white", bd=0)
        textEntryTwo = Text(self.master, font=textEntryFont, bg="white", bd=0)
        textEntryThree = Text(self.master, font=textEntryFont, bg="white", bd=0)
        textEntryFour = Text(self.master, font=textEntryFont, bg="white", bd=0)
        password = Entry(self.master, font=textEntryFont, bg="white", bd=0, show="*")

        # Creating the front Calendar
        calender = Calendar(self.master, selectmode='day', year=2020, month=5, day=22)

        # ///// Creating Buttons
        buttonOne = Button(self.master, bg=self.backgroundColor, fg=self.textColor, text="Login", borderwidth=0, font=self.buttonFont)
        buttonTwo = Button(self.master, bg=self.backgroundColor, fg=self.textColor, text="Register", borderwidth=0, font=self.buttonFont,)
        buttonThree = Button(self.master, image=renderLogout, borderwidth=0, font=self.buttonFont, bd=0, highlightthickness=0,)
        buttonFour = Button(self.master, image=renderBook, borderwidth=0, font=self.buttonFont, bd=0, highlightthickness=0)
        buttonFive = Button(self.master, image=renderPerson, borderwidth=0, font=buttonFont, bd=0, highlightthickness=0,)
        buttonSix = Button(self.master, bg=self.backgroundColor, fg=self.textColor, text="Select", borderwidth=0, font=buttonFont,)
        buttonSeven = Button(self.master, bg=self.backgroundColor, fg=self.textColor, text="Select", borderwidth=0, font=buttonFont,)

        self.master.mainloop()

    # Methods to perform task when window is destroyed
    def killWindow(self, event):
        self.master.destroy()  # destroying the window


# Calling the Main class that contain the GUI and DBS commands
m = Main()
