from tkinter import *
import customtkinter as ct
import os


class MyFrame2(ct.CTkFrame):
    def __init__(self, master, x, i, data, **kwargs):
        super().__init__(master, **kwargs)
        # add widgets onto the frame...
        label = ct.CTkLabel(self, text=x, anchor=W, font=("Ariel", 15))
        button = ct.CTkButton(self, text="Open Location", font=("Ariel", 12),
                              command=lambda: [os.startfile(data[x]["path"])])

        label.place(relx=0.05, rely=0, relwidth=1, relheight=1)
        button.place(relx=0.8, rely=0.2, relwidth=0.15, relheight=0.6)


class MyFrame(ct.CTkScrollableFrame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, **kwargs)

        for i, x in enumerate(data):
            f = MyFrame2(self, x, i, data, height=50, width=850)
            f.grid(row=i, column=0, padx=0)

    def query(self,cat,name,plate,id):
        print(cat,name,plate,id)



class AnotherWindow:
    def __init__(self, dictionary):
        ct.set_appearance_mode("System")
        ct.set_default_color_theme("blue")

        master = ct.CTk()
        master.title("Data History")
        master.geometry("900x400")

        self.data = dictionary

        self.my_frame = MyFrame(master, dictionary)
        self.var = StringVar()
        self.var.set("")

        self.combobox = ct.CTkOptionMenu(master, values=["DOOR OPEN", "POTENTIAL","BREAK IN","MANUAL"], font=("Ariel", 12),fg_color="grey",variable=self.var)
        self.combobox.set("Select Category")

        self.entry1 = ct.CTkEntry(master=master,
                                  placeholder_text="Plate Number",
                                  width=120,
                                  height=25,
                                  border_width=2,
                                  corner_radius=10)

        self.entry2 = ct.CTkEntry(master=master,
                                  placeholder_text="Person ID",
                                  width=120,
                                  height=25,
                                  border_width=2,
                                  corner_radius=10)

        self.entry3 = ct.CTkEntry(master=master,
                                  placeholder_text="Person Name",
                                  width=120,
                                  height=25,
                                  border_width=2,
                                  corner_radius=10)

        self.button = ct.CTkButton(master, text="F I N D", font=("Ariel", 12),command=self.button_function)

        self.my_frame.place(relx=0.01, rely=0.15, relwidth=1 - 2 * 0.01, relheight=1 - 0.18)
        self.combobox.place(relx=0.05, rely=0.03, relwidth=0.15, relheight=0.075)
        self.entry1.place(relx=0.23, rely=0.03, relwidth=0.15, relheight=0.075)
        self.entry2.place(relx=0.41, rely=0.03, relwidth=0.15, relheight=0.075)
        self.entry3.place(relx=0.59, rely=0.03, relwidth=0.15, relheight=0.075)
        self.button.place(relx=1-0.15-0.05, rely=0.03, relwidth=0.15, relheight=0.075)

        master.mainloop()

    def button_function(self):
        self.my_frame.query(self.var.get(),"","","")


dist = {
    "video1": {
        "path": "C:/Users/Pc/PycharmProjects/CarDashboard/DataSet/video 1",
        "number": "",
        "categories": ["DOOR OPEN","BREAK IN"],
        "User Name": "",
        "User ID": ""
    },
    "video2": {
        "path": "C:/Users/Pc/PycharmProjects/CarDashboard/DataSet/video 1",
        "number": "",
        "categories": ["DOOR OPEN", "POTENTIAL","MANUAL"],
        "User Name": "",
        "User ID": ""
    },
    "video3": {
        "path": "C:/Users/Pc/PycharmProjects/CarDashboard/DataSet/video 1",
        "number": "",
        "categories": ["MANUAL"],
        "User Name": "",
        "User ID": ""
    },
    "video4": {
        "path": "C:/Users/Pc/PycharmProjects/CarDashboard/DataSet/video 1",
        "number": "",
        "categories": ["POTENTIAL"],
        "User Name": "",
        "User ID": ""
    },
    "video5": {
        "path": "C:/Users/Pc/PycharmProjects/CarDashboard/DataSet/video 1",
        "number": "",
        "categories": ["BREAK IN","MANUAL"],
        "User Name": "",
        "User ID": ""
    },
}

AnotherWindow(dist)
