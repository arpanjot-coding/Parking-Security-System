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

    # Methods to perform task when window is destroyed
    def killWindow(self,event):
        self.master.destroy()  # destroying the window

    def __init__(self):

        # Getting the windows sizes
        winHeight = self.master.winfo_screenheight()
        winWidth = self.master.winfo_screenwidth()
        # Getting the size of the screen and removing 100 pixels from it to make a bit smaller
        self.master.geometry("{1}x{0}+2+5".format(winHeight - 100, winWidth - 100))
        self.master.resizable(0, 0)
        self.master.configure(bg=self.BackgroundColor)
        # destroy the window if "Escape key is pressed"
        self.master.bind("<Escape>", self.killWindow)

        self.master.mainloop()


# Calling the Main class that contain the GUI and DBS commands
m = Main()
