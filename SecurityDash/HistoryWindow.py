from tkinter import *
import customtkinter as ct
import os


class MyFrame2(ct.CTkFrame):
    def __init__(self, master, x, i, data, **kwargs):
        super().__init__(master, **kwargs)
        # add widgets onto the frame...
        self.x = x

        label = ct.CTkLabel(self, text=x, anchor=W, font=("Ariel", 15))
        button = ct.CTkButton(self, text="Open Location", font=("Ariel", 12),
                              command=lambda: [os.startfile(data[x]["path"])])

        label.place(relx=0.05, rely=0, relwidth=1, relheight=1)
        button.place(relx=0.8, rely=0.2, relwidth=0.15, relheight=0.6)

    def getX(self):
        return self.x


class MyFrame(ct.CTkScrollableFrame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, **kwargs)

        self.data = data
        self.scrols = []
        self.placeFrames()

    def placeFrames(self):
        for i, x in enumerate(self.data):
            f = MyFrame2(self, x, i, self.data, height=50, width=850)
            f.grid(row=i, column=0, padx=0)
            self.scrols.append(f)

    def query(self, cat, plate,name, id):
        print(cat, name, plate, id)
        self.placeFrames()

        for i in range(len(self.scrols)):
            if cat != "Select Category" and cat != "All" and cat not in self.data[self.scrols[i].getX()]["categories"]:
                self.scrols[i].grid_remove()

            if plate != "" and plate != self.data[self.scrols[i].getX()]["number"]:
                self.scrols[i].grid_remove()

            if name != "" and name != self.data[self.scrols[i].getX()]["User Name"]:
                self.scrols[i].grid_remove()

            if id != "" and id != self.data[self.scrols[i].getX()]["User ID"]:
                self.scrols[i].grid_remove()


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

        self.combobox = ct.CTkOptionMenu(master, values=["DOOR OPEN", "POTENTIAL", "BREAK IN", "MANUAL", "All"],
                                         font=("Ariel", 12), fg_color="grey", variable=self.var)
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

        self.button = ct.CTkButton(master, text="F I N D", font=("Ariel", 12), command=self.button_function)

        self.my_frame.place(relx=0.01, rely=0.15, relwidth=1 - 2 * 0.01, relheight=1 - 0.18)
        self.combobox.place(relx=0.05, rely=0.03, relwidth=0.15, relheight=0.075)
        self.entry1.place(relx=0.23, rely=0.03, relwidth=0.15, relheight=0.075)
        self.entry2.place(relx=0.41, rely=0.03, relwidth=0.15, relheight=0.075)
        self.entry3.place(relx=0.59, rely=0.03, relwidth=0.15, relheight=0.075)
        self.button.place(relx=1 - 0.15 - 0.05, rely=0.03, relwidth=0.15, relheight=0.075)

        master.mainloop()

    def button_function(self):
        self.my_frame.query(self.var.get(), self.entry1.get(), self.entry3.get(), self.entry2.get())


