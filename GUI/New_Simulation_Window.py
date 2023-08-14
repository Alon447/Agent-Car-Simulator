import tkinter as tk
from tkinter import ttk

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUI import Animate_Simulation as asim
import GUI.NSW_Controller as nswc
from matplotlib.figure import Figure
from tkinter import messagebox
from Utilities.Getters import hours, minutes, seconds, days, weeks, months

# TODO: add the functionality to insert every parameter for the simulation (that isn't already already here- all the optional parameters)

class New_Simulation_Window(tk.Tk):
    def __init__(self, controller):
        self.nswc = nswc.NSW_Controller(self, controller)
        super().__init__()
        self.title("New Simulation")
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.grid(row=0, column=0, padx=100, pady=100)  # Set the dimensions of the new window (width x height)

        # self.figure = fig
        # self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        # self.canvas.get_tk_widget().pack()

        # self.animation = animation
        # self.canvas,self.animation,self.ax,self.fig = controller.get_canvas_test(self)
        # self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        # self.toolbar.update()

        # Add a spacer frame above the title label
        spacer_frame = ttk.Frame(self.main_frame)
        spacer_frame.pack(pady=50)

        self.title_label = ttk.Label(self.main_frame, text="Car Navigation System", font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        ##########################################
        # prepare the simulation parameters
        ##########################################


        # load city map

        self.city_map_label = tk.Label(self.main_frame, text="Enter city map:")
        self.city_map_label.pack(pady=10)

        self.city_map_entry = tk.Text(self.main_frame, width=15, height=1)
        self.city_map_entry.pack(pady=10)

        self.load_status_label = ttk.Label(self.main_frame, text="City map not loaded")
        self.load_status_label.pack(pady=10)

        self.city_map_button = ttk.Button(self.main_frame, text="Load City Map", command=self.nswc.load_city_map)
        self.city_map_button.pack(pady=10)

        # choose simulation time

        self.simulation_duration_label = ttk.Label(self.main_frame, text="Enter simulation duration:")
        self.simulation_duration_label.pack(pady=10)

        self.hour_menu_label = ttk.Label(self.main_frame, text="Hours")
        self.hour_menu_label.pack()

        self.drop_hours = ttk.Combobox(self.main_frame, values=hours)
        self.drop_hours.current(8)
        self.drop_hours.pack()

        self.min_menu_label = ttk.Label(self.main_frame, text="Days")
        self.min_menu_label.pack()

        self.drop_minutes = ttk.Combobox(self.main_frame, values=days)
        self.drop_minutes.current(0)
        self.drop_minutes.pack()

        self.sec_menu_label = ttk.Label(self.main_frame, text="Weeks")
        self.sec_menu_label.pack()

        self.drop_seconds = ttk.Combobox(self.main_frame, values=weeks)
        self.drop_seconds.current(0)
        self.drop_seconds.pack()


        # block and unblock roads

        self.block_road_button = ttk.Button(self.main_frame, text="Block Road", command=self.nswc.block_road)
        self.block_road_button.pack(pady=10)

        self.unblock_all_roads_button = ttk.Button(self.main_frame, text="Unblock All Roads",
                                                   command=self.nswc.unblock_all_roads)
        self.unblock_all_roads_button.pack(pady=10)

        # car parameters



        self.add_car_button = ttk.Button(self.main_frame, text="Add New Car", command=self.nswc.add_new_car)
        self.add_car_button.pack(pady=10)

        ##########################################
        # all set and done
        ##########################################

        # start simulation

        self.start_simulation_button = ttk.Button(self.main_frame, text="Start Simulation",
                                                  command=self.nswc.start_simulation)
        self.start_simulation_button.pack(pady=10)

        # back to main menu

        self.back_to_main_menu_button = ttk.Button(self.main_frame, text="Back to Main Menu",
                                                   command=self.nswc.back_to_main_menu)
        self.back_to_main_menu_button.pack(pady=10)

    def add_canvas(self,canvas):
        self.canvas = canvas
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()

    def set_load_status_label(self, text):
        self.load_status_label.config(text=text)

    def get_city_name(self):
        return self.city_map_entry.get("1.0", 'end').replace('\n', '')

    # errors
    def no_map_loaded_error(self):
        messagebox.showerror("Error", "Please load a map before adding cars or starting the simulation")

    def add_cars_error(self):
        messagebox.showerror("Error", "Please add cars before starting the simulation")

    # main loop

    def main(self):
        self.mainloop()


