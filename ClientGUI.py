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
    BackgroundColor = "#A49B96"
    ForegroundColor = "#D3D0CF"
    textColor = "#ffffff"
    # Getting the windows sizes
    winHeight = master.winfo_screenheight()
    winWidth = master.winfo_screenwidth()

    def __init__(self):
        # Getting the size of the screen and removing 100 pixels from it to make a bit smaller
        self.master.geometry("{1}x{0}+2+5".format(self.winHeight - 100, self.winWidth - 100))
        self.master.resizable(0, 0)
        self.master.configure(bg=self.BackgroundColor)
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

        self.master.mainloop()

    # Methods to perform task when window is destroyed
    def killWindow(self, event):
        self.master.destroy()  # destroying the window


# Calling the Main class that contain the GUI and DBS commands
m = Main()
