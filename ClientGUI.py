from tkinter import *
from PIL import Image, ImageTk
import psycopg2
import json
from tkinter import messagebox
import random
from tkcalendar import Calendar


class Main:
    BackgroundColor = "#A49B96"
    ForegroundColor = "#D3D0CF"
    textColor = "#ffffff"

    def __init__(self):
        # Creating the window
        master = Tk()
        # Getting the size of the screen and removing 100 pixles from it to make a bit smaller
        master.geometry("{1}x{0}+2+5".format(master.winfo_screenheight() - 100, master.winfo_screenwidth() - 100))
        master.resizable(0, 0)
        master.configure(bg=self.BackgroundColor)
        winHeight = master.winfo_screenheight()
        winWidth = master.winfo_screenwidth()

        master.mainloop()


# Calling the Main class that contain the GUI and DBS commands
m = Main()
