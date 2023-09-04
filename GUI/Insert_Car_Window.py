import tkinter as tk
from tkinter import ttk
from GUI import ICW_Controller as icwc
from Utilities.Getters import hours, minutes, seconds, days_of_the_week


# TODO: add buttons with functionality to reset choices and cars,
#   also display current list of cars and their parameters
#   and most importantly fill in on inputting the rest of the car parameters
class Insert_Car_Window(tk.Toplevel):
    def __init__(self, master=None, controller=None):
        super().__init__(master=master)
        self.icwc = icwc.ICW_Controller(self, master, controller)
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
        self.drop_hours.current(8)
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

        self.drop_days = ttk.Combobox(self, values=days_of_the_week)
        self.drop_days.current(0)
        self.drop_days.pack()

        ###############################
        # car's source and destination
        ###############################
        self.source_title_label = ttk.Label(self, text="Car's Source:")
        self.source_title_label.pack()
        self.source_lable = ttk.Label(self, text="(no source selected)")
        self.source_lable.pack()

        self.destination_title_label = ttk.Label(self, text="Car's Destination:")
        self.destination_title_label.pack()
        self.destination_lable = ttk.Label(self, text="(no destination selected)")
        self.destination_lable.pack()

        self.choose_source_button = ttk.Button(self, text="Choose Source and destination",
                                               command=self.icwc.choose_src_dst)
        self.choose_source_button.pack()

        ###############################
        # confirm choice button
        ###############################

        self.confirm_button = ttk.Button(self, text="Confirm", command=self.icwc.confirm_choice)
        self.confirm_button.pack()

    # TODO: add more error functions as needed
    def no_map_loaded_error(self):
        tk.messagebox.showerror("Error", "No map loaded!")

    def no_source_selected_error(self):
        tk.messagebox.showerror("Error", "No source selected!")

    def no_destination_selected_error(self):
        tk.messagebox.showerror("Error", "No destination selected!")

    def get_day_of_the_week(self):
        return self.drop_days.get()

    def get_hour(self):
        return int(self.drop_hours.get())

    def get_minute(self):
        return int(self.drop_minutes.get())

    def get_second(self):
        return int(self.drop_seconds.get())

