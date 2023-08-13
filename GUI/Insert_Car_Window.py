import tkinter as tk
from tkinter import ttk
from GUI import ICW_Controller as icwc

hours = [i for i in range(0, 24)]
minutes = [i for i in range(0, 60)]
seconds = [i for i in range(0, 60)]

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


class Insert_Car_Window(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.icwc = icwc.ICW_Controller(self, master)
        self.title("Insert Car")
        self.geometry("500x500")

        ###############################
        # car's starting time
        ###############################

        self.settings_label = ttk.Label(self, text="Insert Car Settings")
        self.settings_label.pack()

        self.time_title_label = ttk.Label(self, text="Car's Starting Time")
        self.time_title_label.pack()

        self.hour_menu_label = ttk.Label(self, text="Hour")
        self.hour_menu_label.pack()

        self.drop_hours = ttk.Combobox(self, values=hours)
        self.drop_hours.current(0)
        self.drop_hours.pack()

        self.min_menu_label = ttk.Label(self, text="Minute")
        self.min_menu_label.pack()

        self.drop_minutes = ttk.Combobox(self, values=minutes)
        self.drop_minutes.current(0)
        self.drop_minutes.pack()

        self.sec_menu_label = ttk.Label(self, text="Second")
        self.sec_menu_label.pack()

        self.drop_seconds = ttk.Combobox(self, values=seconds)
        self.drop_seconds.current(0)
        self.drop_seconds.pack()

        self.day_menu_label = ttk.Label(self, text="Car's Starting Day")
        self.day_menu_label.pack()

        self.drop_days = ttk.Combobox(self, values=days)
        self.drop_days.current(0)
        self.drop_days.pack()

        ###############################
        # car's source
        ###############################

        ###############################
        # car's destination
        ###############################

        ###############################
        # confirm choice button
        ###############################

        self.confirm_button = ttk.Button(self, text="Confirm", command=self.icwc.confirm_choice())