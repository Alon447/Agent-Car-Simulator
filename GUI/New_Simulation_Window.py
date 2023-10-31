import tkinter as tk
from tkinter import ttk

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GUI import Animate_Simulation as asim
import GUI.NSW_Controller as nswc
from matplotlib.figure import Figure
from tkinter import messagebox
from Utilities.Getters import hours, minutes, seconds, days, weeks, months, rain_intensity_values, rain_intensity_dict



class New_Simulation_Window(tk.Tk):
    def __init__(self, controller):
        self.nswc = nswc.NSW_Controller(self, controller)
        super().__init__()
        self.title("New Simulation")
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.grid(row=0, column=0, padx=100, pady=100)  # Set the dimensions of the new window (width x height)

        # Add a spacer frame above the title label
        spacer_frame = ttk.Frame(self.main_frame)
        spacer_frame.pack()

        self.title_label = ttk.Label(self.main_frame, text="Car Navigation System", font=("Helvetica", 20))
        self.title_label.pack()

        ##########################################
        # prepare the simulation parameters
        ##########################################

        # load city map
        self.city_map_label = tk.Label(self.main_frame, text="Enter City Name:")
        self.city_map_label.pack(pady=10)

        self.city_map_entry = tk.Text(self.main_frame, width=15, height=1)
        self.city_map_entry.pack(pady=10)

        self.city_map_entry.insert(tk.END,"")

        self.load_status_label = ttk.Label(self.main_frame, text="City Map Not Loaded")
        self.load_status_label.pack(pady=10)

        self.city_map_button = ttk.Button(self.main_frame, text="Load City Map", command=self.nswc.load_city_map)
        self.city_map_button.pack(pady=10)

        # indicate weather to add traffic white noise
        self.traffic_white_noise = tk.BooleanVar()
        self.check_traffic_white_noise = ttk.Checkbutton(self.main_frame, text="Add Traffic White Noise",
                                                           variable=self.traffic_white_noise,
                                                           onvalue=True, offvalue=False)
        self.check_traffic_white_noise.pack(pady=10)

        # indicate weather to plot results
        self.plot_results = tk.BooleanVar()
        self.check_plot_results = ttk.Checkbutton(self.main_frame, text="Plot Q Learning Training Results",
                                                           variable=self.plot_results,
                                                           onvalue=True, offvalue=False)
        self.check_plot_results.pack(pady=10)

        # indicate weather to activate traffic lights
        self.traffic_lights = tk.BooleanVar()
        self.check_traffic_lights = ttk.Checkbutton(self.main_frame, text="Activate Traffic Lights",
                                                           variable=self.traffic_lights,
                                                           onvalue=True, offvalue=False)
        self.check_traffic_lights.pack(pady=10)

        # choose rain intensity
        self.rain_intensity_label = ttk.Label(self.main_frame, text = "Rain Intensity")
        self.rain_intensity_label.pack()

        self.drop_rain_intensity = ttk.Combobox(self.main_frame, values = rain_intensity_values)
        self.drop_rain_intensity.current(0)
        self.drop_rain_intensity.pack()

        # add car button
        self.add_car_button = ttk.Button(self.main_frame, text="Add New Car", command=self.nswc.add_new_car)
        self.add_car_button.pack(pady=10)

        # block and unblock roads
        self.block_road_button = ttk.Button(self.main_frame, text="Block/Unblock Road", command=self.nswc.block_road)
        self.block_road_button.pack(pady=10)

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

    # getters for NSW Controller
    def get_rain_intensity(self):
        rain_val = self.drop_rain_intensity.get()
        return rain_intensity_dict[rain_val]

    def get_plot_results(self):
        return self.plot_results.get()

    def get_traffic_white_noise(self):
        return self.traffic_white_noise.get()

    def get_traffic_lights(self):
        return self.traffic_lights.get()

    # main loop
    def main(self):
        self.mainloop()