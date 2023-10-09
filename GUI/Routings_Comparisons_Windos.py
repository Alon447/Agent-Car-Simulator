import datetime
import tkinter as tk
from tkinter import ttk, Scrollbar
from tkcalendar import Calendar, DateEntry
import GUI.RCW_Controller as rcwc
from Utilities.Getters import routing_algorithms, hours, minutes, seconds, days_of_the_week, rain_intensity_values

import GUI.Main_Window_Controller as mwc

class Main_Window(tk.Tk):
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
        self.scrollbar.grid(row=0, column=4, sticky=(tk.N, tk.S))

        # Configure the canvas to work with the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set, width=700, height=1000)

        # Create a frame inside the canvas to hold your buttons
        self.main_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.main_frame, anchor=tk.NW)

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

        times_titles = ["Enter simulation starting time:", "Enter simulation ending time:", "test"]
        for title in times_titles:
            self.simulation_starting_time_label = tk.Label(self.main_frame, text=title)
            row += 1
            self.simulation_starting_time_label.grid(row=row, column=1, padx=0, pady=10)

            col = 0

            self.hour_menu_label = ttk.Label(self.main_frame, text="Hours")
            row += 1
            self.hour_menu_label.grid(row=row, column=col, padx=0, pady=10)

            self.drop_hours = ttk.Combobox(self.main_frame, values=hours)
            self.drop_hours.current(8)
            self.drop_hours.grid(row=row + 1, column=col, padx=0, pady=10)

            col += 1
            self.min_menu_label = ttk.Label(self.main_frame, text="Minute")
            self.min_menu_label.grid(row=row, column=col, padx=10, pady=10)

            self.drop_minutes = ttk.Combobox(self.main_frame, values=minutes)
            self.drop_minutes.current(0)
            self.drop_minutes.grid(row=row + 1, column=col, padx=10, pady=10)

            col += 1
            self.sec_menu_label = ttk.Label(self.main_frame, text="Second")
            self.sec_menu_label.grid(row=row, column=col, padx=0, pady=10)

            self.drop_seconds = ttk.Combobox(self.main_frame, values=seconds)
            self.drop_seconds.current(0)
            self.drop_seconds.grid(row=row + 1, column=col, padx=10, pady=10)

            self.day_menu_label = ttk.Label(self.main_frame, text="Day")
            row += 2
            self.day_menu_label.grid(row=row, column=1, padx=1, pady=10)

            cur_year = int(datetime.datetime.now().year)
            cur_month = int(datetime.datetime.now().month)
            cur_day = int(datetime.datetime.now().day)

            self.cal = Calendar(self.main_frame, selectmode='day',
                                year=cur_year, month=cur_month,
                                day=cur_day, date_pattern='dd/mm/yyyy')

            row += 1
            self.cal.grid(row=row, column=1, padx=1, pady=10)

        # Add more buttons as needed

        # Bind the canvas to configure it to update its scroll region when the frame size changes
        self.main_frame.bind("<Configure>", self.on_frame_configure)

        # Call the update_scrollregion function to set the scrollable region
        self.update_scrollregion()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_scrollregion(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def main(self):
        self.mainloop()

if __name__ == "__main__":
    app = Main_Window(None)
    app.main()
