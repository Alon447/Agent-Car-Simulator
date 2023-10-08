import datetime
import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk

from GUI import IBR_Controller as ibrc
from Utilities.Getters import hours, minutes, seconds


class Insert_Block_Road(tk.Toplevel):
    """
    This class is used to insert a new blocked road into the simulation
    """
    def __init__(self, master=None, controller=None):
        super().__init__(master=master)
        self.ibrc = ibrc.IBR_Controller(self, master, controller)
        # Window title and size
        self.title("Insert Blocked Road")
        self.geometry("1000x1000")

        ###############################
        # road's blockage starting time
        ###############################

        self.settings_label = ttk.Label(self, text = "Insert Car Settings")
        self.settings_label.pack()

        self.time_title_label = ttk.Label(self, text = "Road's blockage Starting Time")
        self.time_title_label.pack()

        self.hour_menu_label1 = ttk.Label(self, text = "Hour")
        self.hour_menu_label1.pack()

        self.start_hour = ttk.Combobox(self, values = hours)
        self.start_hour.current(8)
        self.start_hour.pack()

        self.min_menu_label1 = ttk.Label(self, text = "Minute")
        self.min_menu_label1.pack()

        self.start_minute = ttk.Combobox(self, values = minutes)
        self.start_minute.current(0)
        self.start_minute.pack()

        self.sec_menu_label1 = ttk.Label(self, text = "Second")
        self.sec_menu_label1.pack()

        self.start_second = ttk.Combobox(self, values = seconds)
        self.start_second.current(0)
        self.start_second.pack()

        ###############################
        # Road's blockage starting day using calendar
        ###############################
        cur_year = int(datetime.datetime.now().year)
        cur_month = int(datetime.datetime.now().month)
        cur_day = int(datetime.datetime.now().day)

        self.cal_start = Calendar(self, selectmode = 'day', year = cur_year, month = cur_month, day = cur_day,
                            date_pattern = 'dd/mm/yyyy')

        self.cal_start.pack(pady = 20)

        ###############################
        # road's blockage ending time
        ###############################

        self.settings_label = ttk.Label(self, text = "Insert Car Settings")
        self.settings_label.pack()

        self.time_title_label = ttk.Label(self, text = "Road's blockage Ending Time")
        self.time_title_label.pack()

        self.hour_menu_label2 = ttk.Label(self, text = "Hour")
        self.hour_menu_label2.pack()

        self.end_hour = ttk.Combobox(self, values = hours)
        self.end_hour.current(8)
        self.end_hour.pack()

        self.min_menu_label2 = ttk.Label(self, text = "Minute")
        self.min_menu_label2.pack()

        self.end_minute = ttk.Combobox(self, values = minutes)
        self.end_minute.current(0)
        self.end_minute.pack()

        self.sec_menu_label2 = ttk.Label(self, text = "Second")
        self.sec_menu_label2.pack()

        self.end_second = ttk.Combobox(self, values = seconds)
        self.end_second.current(0)
        self.end_second.pack()

        ###############################
        # Road's blockage ending day using calendar
        ###############################
        end_year = int(datetime.datetime.now().year)
        end_month = int(datetime.datetime.now().month)
        end_day = int(datetime.datetime.now().day)

        self.cal_end = Calendar(self, selectmode = 'day', year = end_year, month = end_month, day = end_day,
                            date_pattern = 'dd/mm/yyyy')

        self.cal_end.pack(pady = 20)

        ###############################
        # choose which road to block
        ###############################

        self.choose_road_button = ttk.Button(self, text = "Choose Source and destination",
                                               command = self.ibrc.choose_road)
        self.choose_road_button.pack()


        ###############################
        # confirm choice button
        ###############################

        self.confirm_button = ttk.Button(self, text = "Confirm", command = self.ibrc.confirm_choice)
        self.confirm_button.pack()

        ###############################
        #   existing roads blockages
        ###############################
        self.existing_roads_label = ttk.Label(self, text = "Existing roads blockages:")
        self.existing_roads_label.pack()

        self.existing_blockages_treeview = ttk.Treeview(self, column=("c1", "c2", "c3", "c4", "c5"), show = 'headings', height = 5, selectmode = "extended")

        self.existing_blockages_treeview.column("#1", width = 50, anchor = tk.CENTER)
        self.existing_blockages_treeview.heading("#1", text = "ID")

        self.existing_blockages_treeview.column("#2", width = 100, anchor = tk.CENTER)
        self.existing_blockages_treeview.heading("#2", text = "Source")

        self.existing_blockages_treeview.column("#3", width = 100, anchor = tk.CENTER)
        self.existing_blockages_treeview.heading("#3", text = "Destination")

        self.existing_blockages_treeview.column("#4", width = 150, anchor = tk.CENTER)
        self.existing_blockages_treeview.heading("#4", text = "Starting Time")

        self.existing_blockages_treeview.column("#5", width = 120, anchor = tk.CENTER)
        self.existing_blockages_treeview.heading("#5", text = "Ending Time")

        self.existing_blockages_treeview.pack()

        self.ibrc.load_existing_blockages()

        self.delete_blockage_button = ttk.Button(self, text = "Delete Road Blockage", command = lambda: self.ibrc.delete_blockage(
            self.existing_blockages_treeview.selection()))
        self.delete_blockage_button.pack()

    def get_start_date(self):
        raw_date = self.cal_start.get_date()
        date = raw_date.split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        return day, month, year

    def get_start_hour(self):
        return int(self.start_hour.get())

    def get_start_minute(self):
        return int(self.start_minute.get())

    def get_start_second(self):
        return int(self.start_second.get())

    def get_end_date(self):
        raw_date = self.cal_end.get_date()
        date = raw_date.split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        return day, month, year
    def get_end_hour(self):
        return int(self.end_hour.get())

    def get_end_minute(self):
        return int(self.end_minute.get())

    def get_end_second(self):
        return int(self.end_second.get())

    def add_road(self, road):
        self.existing_blockages_treeview.insert("", tk.END, values=road)
    # Gets
    def road_id_from_treeview(self, road_id):
        id = self.existing_blockages_treeview.item(road_id)['values'][0]
        start_time = self.existing_blockages_treeview.item(road_id)['values'][3]
        end_time = self.existing_blockages_treeview.item(road_id)['values'][4]
        return id, start_time, end_time

    def get_existing_blockages_treeview(self):
        return self.existing_blockages_treeview
    # Exception handling
    def no_map_loaded_error(self):
        tk.messagebox.showerror("Error", "No map loaded!")
    def no_road_selected_error(self):
        tk.messagebox.showerror("Error", "No road selected!")
    def general_error(self):
        tk.messagebox.showerror("Error", "Something went wrong!")