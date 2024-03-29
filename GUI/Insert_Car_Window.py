# external imports
import datetime
import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk

# internal imports
from GUI import ICW_Controller as icwc
from Utilities.Getters import hours, minutes, seconds, routing_algorithms



class Insert_Car_Window(tk.Toplevel):
    """
    This class is used to create the insert a new car into the simulation window
    """
    def __init__(self, master=None, controller=None):
        super().__init__(master=master)
        self.existing_cars_treeview = None
        self.icwc = icwc.ICW_Controller(self, master, controller)
        self.title("Insert Car")
        self.geometry("1000x1000")


        # titles
        self.settings_label = ttk.Label(self, text="Insert Car Settings")
        self.settings_label.pack()

        self.time_title_label = ttk.Label(self, text="Car's Starting Time")
        self.time_title_label.pack()


        # car's starting time

        # choose hour
        self.hour_menu_label = ttk.Label(self, text="Hour")
        self.hour_menu_label.pack()

        self.drop_hours = ttk.Combobox(self, values=hours)
        self.drop_hours.current(8)
        self.drop_hours.pack()

        # choose minute
        self.min_menu_label = ttk.Label(self, text="Minute")
        self.min_menu_label.pack()

        self.drop_minutes = ttk.Combobox(self, values=minutes)
        self.drop_minutes.current(0)
        self.drop_minutes.pack()

        # choose second
        self.sec_menu_label = ttk.Label(self, text="Second")
        self.sec_menu_label.pack()

        self.drop_seconds = ttk.Combobox(self, values=seconds)
        self.drop_seconds.current(0)
        self.drop_seconds.pack()

        ####################################
        # car's starting day using calendar
        ####################################
        cur_year = int(datetime.datetime.now().year)
        cur_month = int(datetime.datetime.now().month)
        cur_day = int(datetime.datetime.now().day)

        self.cal = Calendar(self, selectmode='day',
                            year=cur_year, month=cur_month,
                            day=cur_day, date_pattern='dd/mm/yyyy')

        self.cal.pack(pady=20)

        ###############################
        # car's source and destination
        ###############################


        self.choose_source_button = ttk.Button(self, text="Choose Source and destination",
                                               command=self.icwc.choose_src_dst)
        self.choose_source_button.pack()

        ###############################
        # car's routing algorithm
        ###############################

        self.routing_algorithm_label = ttk.Label(self, text="Routing Algorithm:")
        self.routing_algorithm_label.pack()

        self.routing_algorithm_menu = ttk.Combobox(self, values=routing_algorithms)
        self.routing_algorithm_menu.current(0)
        self.routing_algorithm_menu.pack()

        ###############################
        # car's use existing q tables
        ###############################
        self.use_existing_q_tables = tk.BooleanVar()
        self.check_use_existing_q_tables = ttk.Checkbutton(self, text="Use Existing Tables",
                                                           variable=self.use_existing_q_tables,
                                                           onvalue=True, offvalue=False)
        self.check_use_existing_q_tables.pack()

        ###############################
        # confirm choice button
        ###############################
        self.confirm_button = ttk.Button(self, text="Confirm", command=self.icwc.confirm_choice)
        self.confirm_button.pack()

        ###############################
        #   existing cars
        ###############################
        self.existing_cars_label = ttk.Label(self, text="Existing Cars:")
        self.existing_cars_label.pack()

        # create the treeview and load existing cars
        self.create_treeview()
        self.icwc.load_existing_cars()

        ###############################
        #   delete cars button
        ###############################
        self.delete_cars_button = ttk.Button(self, text="Delete Cars", command=lambda: self.icwc.delete_cars(self.existing_cars_treeview.selection()))
        self.delete_cars_button.pack()

    def create_treeview(self):
        self.existing_cars_treeview = ttk.Treeview(self, column = ("c1", "c2", "c3", "c4", "c5", "c6"),
                                                   show = 'headings', height = 5, selectmode = "extended")

        self.existing_cars_treeview.column("#1", width = 50, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#1", text = "ID")

        self.existing_cars_treeview.column("#2", width = 100, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#2", text = "Source")

        self.existing_cars_treeview.column("#3", width = 100, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#3", text = "Destination")

        self.existing_cars_treeview.column("#4", width = 150, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#4", text = "Starting Time")

        self.existing_cars_treeview.column("#5", width = 120, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#5", text = "Routing Algorithm")

        self.existing_cars_treeview.column("#6", width = 130, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#6", text = "Use Existing Q Tables")

        self.existing_cars_treeview.pack()

    # get functions to be used in ICW_Controller
    def get_hour(self):
        return int(self.drop_hours.get())

    def get_minute(self):
        return int(self.drop_minutes.get())

    def get_second(self):
        return int(self.drop_seconds.get())

    def get_routing_algorithm(self):
        return self.routing_algorithm_menu.get()

    def get_date(self):
        raw_date = self.cal.get_date()
        date = raw_date.split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        return day, month, year

    def get_raw_date(self):
        return self.cal.get_date()

    def get_use_existing_q_tables(self):
        return self.use_existing_q_tables.get()

    def get_existing_cars_treeview(self):
        return self.existing_cars_treeview

    # functions for the treeview
    def add_car(self, car):
        self.existing_cars_treeview.insert("", tk.END, values=car)

    def car_id_from_treeview(self, car_id):
        return self.existing_cars_treeview.item(car_id)['values'][0]