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
    def __init__(self, controller):
        self.nlswc = nlswc.NLSW_Controller(self, controller)
        super().__init__()
        self.title("Load Simulation")
        self.main_frame = ttk.Frame(self, padding = 20)
        self.main_frame.grid(padx = 100, pady = 100)  # Set the dimensions of the new window (width x height)

        # load city map
        self.city_map_label = tk.Label(self.main_frame, text = "Enter The City's Simulation You Wish To Load:")
        self.city_map_label.pack(pady = 10)

        self.city_map_entry = tk.Text(self.main_frame, width = 15, height = 1)
        self.city_map_entry.pack(pady = 10)

        self.city_map_entry.insert(tk.END, "TLV")  # TODO: remove this line after testing

        self.load_status_label = ttk.Label(self.main_frame, text = "City Map Not Loaded")
        self.load_status_label.pack(pady = 10)

        self.city_map_button = ttk.Button(self.main_frame, text = "Load City", command = self.nlswc.load_city_map)
        self.city_map_button.pack(pady = 0)

        # choose past simulation
        self.existing_cars_treeview = ttk.Treeview(self, column = ("c1", "c2", "c3", "c4", "c5", "c6","c7", "c8"),
                                                   show = 'headings', height = 5, selectmode = "extended")

        self.existing_cars_treeview.column("#1", width = 50, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#1", text = "ID")

        self.existing_cars_treeview.column("#2", width = 100, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#2", text = "Source")

        self.existing_cars_treeview.column("#3", width = 100, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#3", text = "Destination")

        self.existing_cars_treeview.column("#4", width = 150, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#4", text = "Start_time")

        self.existing_cars_treeview.column("#5", width = 120, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#5", text = "End_time")

        self.existing_cars_treeview.column("#6", width = 130, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#6", text = "Routing_algorithm")

        self.existing_cars_treeview.column("#7", width = 130, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#7", text = "City Name")

        self.existing_cars_treeview.column("#8", width = 130, anchor = tk.CENTER)
        self.existing_cars_treeview.heading("#8", text = "Reached_destination")

        self.existing_cars_treeview.grid(row = 1, column = 0, padx = 50, pady = 50)

        # load exisitng simulations into the table
        self.nlswc.load_existing_simulations()

    def get_city_name(self):
        return self.city_map_entry.get("1.0", 'end').replace('\n', '')

    def set_load_status_label(self, text):
        self.load_status_label.config(text=text)

    def add_existing_simulation(self, json_data, simulation_name):
        """
        load existing simulation from json files to the table
        :param json_data:
        :param simulation_name:
        :return:
        """
        simulation_data = json_data[0]
        self.existing_cars_treeview.insert("", tk.END, values = (json_data["simulation id"],
                                                                  json_data["Source"],
                                                                  json_data["Destination"],
                                                                  json_data["Start_time"],
                                                                  json_data["End_time"],
                                                                  json_data["Routing_algorithm"],
                                                                  simulation_name,
                                                                  json_data["Reached_destination"],
                                                                  ))
    # main loop
    def main(self):
        self.mainloop()