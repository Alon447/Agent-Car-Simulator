import tkinter as tk
from tkinter import ttk

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUI import Animate_Simulation as asim
import GUI.NLSW_Controller as nlswc
from matplotlib.figure import Figure
from tkinter import messagebox
from Utilities.Getters import hours, minutes, seconds, days, weeks, months,rain_intensity_values
class New_Load_Simulation_Window(tk.Tk):
    """
    This class is used to create the load simulation window
    """
    def __init__(self, controller):

        super().__init__()
        self.existing_simulations_treeview = None
        self.nlswc = nlswc.NLSW_Controller(self, controller)

        self.title("Load Simulation")
        self.main_frame = ttk.Frame(self, padding = 20)
        self.main_frame.grid(row=0, column=0,padx = 150, pady = 150)  # Set the dimensions of the new window (width x height)


        self.settings_label = ttk.Label(self, text = "Load Saved Simulation", font = ("Ariel", 16))
        self.settings_label.grid(row = 1, column = 0, padx = 10, pady = 10)


        height = self.nlswc.get_number_of_saves()
        # create past simulations treeview
        self.create_treeview(height)

        # load exisitng simulations into the table
        self.nlswc.load_existing_simulations()

        # confirm button
        self.confirm_button = ttk.Button(self.main_frame, text = "Confirm",
                                         command=lambda: self.nlswc.confirm(self.existing_simulations_treeview.selection()))
        self.confirm_button.grid(row = 2, column = 0, padx = 10, pady = 10)
        # back to menu button
        self.back_button = ttk.Button(self.main_frame, text = "Back To Main Menu", command = self.nlswc.back_to_menu)
        self.back_button.grid(row = 3, column = 0, padx = 10, pady = 10)

    def create_treeview(self, height):
        self.existing_simulations_treeview = ttk.Treeview(self, column = ("c1", "c2", "c3"),
                                                   show = 'headings', height = height, selectmode = "browse")

        self.existing_simulations_treeview.column("#1", width = 200, anchor = tk.CENTER)
        self.existing_simulations_treeview.heading("#1", text = "Name")

        self.existing_simulations_treeview.column("#2", width = 150, anchor = tk.CENTER)
        self.existing_simulations_treeview.heading("#2", text = "Date")

        self.existing_simulations_treeview.column("#3", width = 100, anchor = tk.CENTER)
        self.existing_simulations_treeview.heading("#3", text = "Number of cars")
        self.existing_simulations_treeview.grid(row = 1, column = 0, padx = 50, pady = 50)


        # self.existing_simulations_treeview.column("#4", width = 150, anchor = tk.CENTER)
        # self.existing_simulations_treeview.heading("#4", text = "Start_time")


    # def get_city_name(self):
    #     return self.city_map_entry.get("1.0", 'end').replace('\n', '')

    def set_load_status_label(self, text):
        self.load_status_label.config(text=text)

    def add_existing_simulation(self, json_data, simulation_name, modification_datetime):
        """
        load existing simulation from json files to the table
        :param json_data:
        :param simulation_name:
        :return:
        """
        simulation_data = json_data[0]
        self.existing_simulations_treeview.insert("", tk.END, values = (simulation_name, modification_datetime, len(simulation_data)-1))
    # functions for the treeview
    def simulation_id_from_treeview(self, simulation_id):
        return self.existing_simulations_treeview.item(simulation_id)['values'][0]
    # main loop
    def main(self):
        self.mainloop()