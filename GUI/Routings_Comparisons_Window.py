import datetime
import tkinter as tk
from tkinter import ttk, Scrollbar
from tkcalendar import Calendar, DateEntry
import GUI.RCW_Controller as rcwc
from Utilities.Getters import *

import GUI.Main_Window_Controller as mwc


class Routing_Comparisons_Window(tk.Tk):
    def __init__(self, controller):
        row = 0
        super().__init__()
        self.rcwc = rcwc.RCW_Controller(self, controller)
        self.controller = controller
        self.title("Car Navigation")

        # Create a Canvas widget with a scrollbar
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Add a vertical scrollbar for the canvas
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=3, sticky=(tk.N, tk.S))

        # Configure the canvas to work with the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set, width=700, height=1000)

        # Create a frame inside the canvas to hold your buttons
        self.main_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor=tk.NW)

        self.title_label = ttk.Label(self.main_frame, text="Car Routing Comparisons \n \t and Statistic",
                                     font=("Helvetica", 14))
        row += 1
        self.title_label.grid(row=row, column=1, padx=0, pady=10)

        button_style = ttk.Style()
        button_style.configure("TButton", font=("Ariel", 14))

        # start new simulation button
        button_style = ttk.Style()
        button_style.configure("TButton", font=("Helvetica", 14))

        # load city map

        self.city_map_label = tk.Label(self.main_frame, text="Enter city map:")
        row += 1
        self.city_map_label.grid(row=row, column=1, padx=0, pady=10)

        self.city_map_entry = tk.Text(self.main_frame, width=15, height=1)
        row += 1
        self.city_map_entry.grid(row=row, column=1, padx=0, pady=10)

        self.load_status_label = ttk.Label(self.main_frame, text="City map not loaded")
        row += 1
        self.load_status_label.grid(row=row, column=1, padx=0, pady=10)

        self.city_map_button = ttk.Button(self.main_frame, text="Load City Map", command=self.rcwc.load_city_map)
        row += 1
        self.city_map_button.grid(row=row, column=1, padx=0, pady=10)

        # choose sources and destinations

        self.choose_source_button = ttk.Button(self.main_frame, text="Choose Source and destination",
                                               command=self.rcwc.choose_src_dst)
        row += 1
        self.choose_source_button.grid(row=row, column=1, padx=0, pady=10)

        # choose routing algorithms

        self.algorithms_label = tk.Label(self.main_frame, text="Choose routing algorithms:")
        row += 1
        self.algorithms_label.grid(row=row, column=1, padx=0, pady=10)

        self.algorithms_boolean_dict = {}
        i = 0
        row += 1
        for algorithm in routing_algorithms:

            self.algorithms_boolean_dict[algorithm] = tk.BooleanVar()
            self.algorithms_boolean_dict[algorithm].set(False)
            self.algorithm_checkbutton = tk.Checkbutton(self.main_frame, text=algorithm,
                                                        command=self.rcwc.toggle_algorithm(algorithm,
                                                                                           self.algorithms_boolean_dict[
                                                                                               algorithm]),
                                                        variable=self.algorithms_boolean_dict[algorithm],
                                                        onvalue=True, offvalue=False)

            self.algorithm_checkbutton.grid(row=row, column=i, padx=0, pady=10)
            i += 1
            if i % 3 == 0:
                row += 1
                i = 0

        # choose cars amount

        self.cars_amount_label = tk.Label(self.main_frame, text="Enter amount of cars:")
        row += 1
        self.cars_amount_label.grid(row=row, column=1, padx=10, pady=10)

        self.cars_amount_entry = tk.Text(self.main_frame, width=15, height=1)
        row += 1
        self.cars_amount_entry.grid(row=row, column=1, padx=10, pady=10)

        # choose simulations amount

        self.simulations_amount_label = tk.Label(self.main_frame, text="Enter amount of simulations:")
        row += 1
        self.simulations_amount_label.grid(row=row, column=1, padx=0, pady=10)

        self.simulations_amount_entry = tk.Text(self.main_frame, width=15, height=1)
        row += 1
        self.simulations_amount_entry.grid(row=row, column=1, padx=0, pady=10)

        # choose simulation times

        self.times_titles = {Start_key: Starting_time_title, End_key: Ending_time_title}
        self.time_entries = {Hours_key: hours, Minutes_key: minutes, Seconds_key: seconds}
        self.time_entries_lables = {}
        self.drop_time_entries = {}
        self.cal = {}
        for title in self.times_titles.keys():
            self.simulation_starting_time_label = tk.Label(self.main_frame, text=self.times_titles[title])
            row += 1
            self.simulation_starting_time_label.grid(row=row, column=1, padx=0, pady=10)

            col = 0
            row += 1
            for time_entry in self.time_entries.keys():
                self.time_entries_lables[title] = {}
                self.time_entries_lables[title][time_entry] = ttk.Label(self.main_frame, text=time_entry)
                self.time_entries_lables[title][time_entry].grid(row=row, column=col, padx=0, pady=10)

                self.drop_time_entries[title] = {}
                self.drop_time_entries[title][time_entry] = ttk.Combobox(self.main_frame,
                                                                         values=self.time_entries[time_entry])
                self.drop_time_entries[title][time_entry].current(0)
                self.drop_time_entries[title][time_entry].grid(row=row + 1, column=col, padx=0, pady=10)
                col += 1

            self.day_menu_label = ttk.Label(self.main_frame, text=Days_lable_text)
            row += 2
            self.day_menu_label.grid(row=row, column=1, padx=1, pady=10)

            cur_year = int(datetime.datetime.now().year)
            cur_month = int(datetime.datetime.now().month)
            cur_day = int(datetime.datetime.now().day)

            self.cal[title] = Calendar(self.main_frame, selectmode='day',
                                       year=cur_year, month=cur_month,
                                       day=cur_day, date_pattern='dd/mm/yyyy')

            row += 1
            self.cal[title].grid(row=row, column=1, padx=1, pady=10)

        # general settings

        # q learning settings
        self.q_learning_label = tk.Label(self.main_frame, text="Q-Learning Settings")
        row += 1
        self.q_learning_label.grid(row=row, column=1, padx=0, pady=10)

        self.q_learning_parameters = {Number_of_episodes: "Number of episodes:",
                                      Max_steps_per_episode: "Max steps per episode:"}
        self.q_learning_parameters_lable = {}
        self.q_learning_parameters_entry = {}
        for parameter in self.q_learning_parameters.keys():
            self.q_learning_parameters_lable[parameter] = tk.Label(self.main_frame,
                                                                   text=self.q_learning_parameters[parameter])
            row += 1
            self.q_learning_parameters_lable[parameter].grid(row=row, column=1, padx=0, pady=10)

            self.q_learning_parameters_entry[parameter] = tk.Text(self.main_frame, width=15, height=1)
            row += 1
            self.q_learning_parameters_entry[parameter].grid(row=row, column=1, padx=0, pady=10)

        self.use_existing_q_tables_label = tk.Label(self.main_frame, text="Use existing Q tables:")
        row += 1
        self.use_existing_q_tables_label.grid(row=row, column=1, padx=0, pady=10)

        self.use_existing_q_tables = tk.BooleanVar()
        self.check_use_existing_q_tables = ttk.Checkbutton(self.main_frame, text="Use Existing Tables",
                                                           variable=self.use_existing_q_tables,
                                                           onvalue=True, offvalue=False)
        row += 1
        self.check_use_existing_q_tables.grid(row=row, column=1, padx=0, pady=10)

        # rain, traffic light and traffic white noise settings

        self.rain_intensity_label = tk.Label(self.main_frame, text="Rain Intensity:")
        row += 1
        self.rain_intensity_label.grid(row=row, column=0, padx=0, pady=10)

        self.drop_rain_intensity = ttk.Combobox(self.main_frame, values=rain_intensity_values)
        self.drop_rain_intensity.current(0)
        self.drop_rain_intensity.grid(row=row + 1, column=0, padx=0, pady=10)

        self.traffic_lights_label = tk.Label(self.main_frame, text="Traffic Light:")
        self.traffic_lights_label.grid(row=row, column=1, padx=0, pady=10)

        self.traffic_lights = tk.BooleanVar()
        self.check_traffic_lights = ttk.Checkbutton(self.main_frame, text="add traffic light",
                                                   variable=self.traffic_lights,
                                                   onvalue=True, offvalue=False)

        self.check_traffic_lights.grid(row=row + 1, column=1, padx=0, pady=10)

        self.traffic_white_noise_label = tk.Label(self.main_frame, text="Traffic White Noise:")
        self.traffic_white_noise_label.grid(row=row, column=2, padx=0, pady=10)

        self.traffic_white_noise = tk.BooleanVar()
        self.check_traffic_white_noise = ttk.Checkbutton(self.main_frame, text="add traffic white noise",
                                                         variable=self.traffic_white_noise,
                                                         onvalue=True, offvalue=False)
        self.check_traffic_white_noise.grid(row=row + 1, column=2, padx=0, pady=10)

        # start new simulation button
        self.start_routing_comparisons_button = ttk.Button(self.main_frame, text="Start Routing Comparisons",
                                                           command=self.rcwc.prepare_route_comparison)
        row += 2
        self.start_routing_comparisons_button.grid(row=row, column=1, padx=0, pady=10)

        self.return_to_main_menu_button = ttk.Button(self.main_frame, text="Return to main menu",
                                                        command=self.rcwc.back_to_main_menu)
        row += 2
        self.return_to_main_menu_button.grid(row=row, column=1, padx=0, pady=10)
        # Bind the canvas to configure it to update its scroll region when the frame size changes
        self.main_frame.bind("<Configure>", self.on_frame_configure)

        # Call the update_scrollregion function to set the scrollable region
        self.update_scrollregion()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_scrollregion(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def set_load_status_label(self, text):
        self.load_status_label.config(text=text)

    def main(self):
        self.mainloop()

    def get_city_name(self):
        return self.city_map_entry.get("1.0", 'end').replace('\n', '')

    def get_starting_time(self):
        return self.drop_time_entries[Start_key][Hours_key].get(), \
        self.drop_time_entries[Start_key][Minutes_key].get(), \
        self.drop_time_entries[Start_key][Seconds_key].get(), self.cal[Start_key].get_date()

    def get_date(self,title):
        raw_date = self.cal[title].get_date()
        date = raw_date.split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        return day, month, year

    def get_time(self,title):
        return self.drop_time_entries[title][Hours_key].get(), \
        self.drop_time_entries[title][Minutes_key].get(), \
        self.drop_time_entries[title][Seconds_key].get(), self.cal[End_key].get_date()
    def get_algorithms(self):
        return self.algorithms_boolean_dict

    def get_cars_amount(self):
        return self.cars_amount_entry.get()

    def get_simulations_amount(self):
        return self.simulations_amount_entry.get()

    def get_city_map(self):
        return self.city_map_entry.get("1.0", 'end').replace('\n', '')

    def get_date_from_title(self, title):
        raw_date = self.cal[title].get_date()
        date = raw_date.split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        return day, month, year

    def get_rain_intensity(self):
        rain_val = self.drop_rain_intensity.get()
        return rain_intensity_dict[rain_val]

    def get_traffic_lights(self):
        return self.traffic_lights.get()

    def get_use_existing_q_tables(self):
        return self.use_existing_q_tables.get()

    def get_number_of_episodes(self):
        return self.q_learning_parameters_entry[Number_of_episodes].get()

    def get_used_algorithms(self):
        algorithms_list = []
        for algorithm in self.algorithms_boolean_dict.keys():
            if self.algorithms_boolean_dict[algorithm].get():
                algorithms_list.append(algorithm)
        return algorithms_list

    def get_add_traffic_white_noise(self):
        return self.traffic_white_noise.get()

    def get_max_steps_per_episode(self):
        return self.q_learning_parameters_entry[Max_steps_per_episode].get()

    def get_starting_time_date(self,title_key):
        raw_date = self.cal[title_key].get_date()
        date = raw_date.split('/')
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        return  year,month,day, int(self.drop_time_entries[title_key][Hours_key].get()), \
        int(self.drop_time_entries[title_key][Minutes_key].get()), int(self.drop_time_entries[title_key][Seconds_key].get())


if __name__ == "__main__":
    app = Routing_Comparisons_Window(None)
    app.main()
