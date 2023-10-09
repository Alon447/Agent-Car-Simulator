import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import GUI.RCW_Controller as rcwc
from Utilities.Getters import routing_algorithms, hours, minutes, seconds, days_of_the_week, rain_intensity_values


class Routing_Comparisons_Windows(tk.Tk):
    def __init__(self, controller = None):
        # self.root = self
        self.rcwc = rcwc.RCW_Controller(self, controller)
        super().__init__()
        self.controller = controller
        self.title("Car Routing Comparisons and Statistics")
        # self.geometry("1000x1000")
        # self.make
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.grid(row=0, column=0, padx=100, pady=100)

        self.title_label = ttk.Label(self.main_frame, text="Car Routing Comparisons and Statistic",
                                     font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        button_style = ttk.Style()
        button_style.configure("TButton", font=("Helvetica", 14))

        # load city map

        self.city_map_label = tk.Label(self.main_frame, text="Enter city map:")
        self.city_map_label.pack(pady=10)

        self.city_map_entry = tk.Text(self.main_frame, width=15, height=1)
        self.city_map_entry.pack(pady=10)

        self.load_status_label = ttk.Label(self.main_frame, text="City map not loaded")
        self.load_status_label.pack(pady=10)

        self.city_map_button = ttk.Button(self.main_frame, text="Load City Map", command=self.rcwc.load_city_map)
        self.city_map_button.pack(pady=10)

        # choose sources and destinations

        # choose routing algorithms

        self.algorithms_label = tk.Label(self.main_frame, text="Choose routing algorithms:")
        self.algorithms_label.pack(pady=10)

        self.algorithms_boolean_dict = {}
        for algorithm in routing_algorithms:
            self.algorithms_boolean_dict[algorithm] = tk.BooleanVar()
            self.algorithms_boolean_dict[algorithm].set(False)
            self.algorithm_checkbutton = tk.Checkbutton(self.main_frame, text=algorithm,
                                                        command=self.rcwc.toggle_algorithm(algorithm,
                                                                                           self.algorithms_boolean_dict[
                                                                                               algorithm]),
                                                        variable=self.algorithms_boolean_dict[algorithm],
                                                        onvalue=True, offvalue=False)
            self.algorithm_checkbutton.pack()

        # choose cars amount

        self.cars_amount_label = tk.Label(self.main_frame, text="Enter amount of cars:")
        self.cars_amount_label.pack(pady=10)

        self.cars_amount_entry = tk.Text(self.main_frame, width=15, height=1)
        self.cars_amount_entry.pack(pady=10)

        # choose simulations amount

        self.simulations_amount_label = tk.Label(self.main_frame, text="Enter amount of simulations:")
        self.simulations_amount_label.pack(pady=10)

        self.simulations_amount_entry = tk.Text(self.main_frame, width=15, height=1)
        self.simulations_amount_entry.pack(pady=10)

        # choose simulation times

        self.simulation_starting_time_label = tk.Label(self.main_frame, text="Enter simulation starting time:")
        self.simulation_starting_time_label.pack(pady=10)

        self.hour_menu_label = ttk.Label(self.main_frame, text="Hours")
        self.hour_menu_label.pack(side=tk.LEFT)

        self.drop_hours = ttk.Combobox(self.main_frame, values=hours)
        self.drop_hours.current(8)
        self.drop_hours.pack(side=tk.LEFT, padx=10)

        self.min_menu_label = ttk.Label(self.main_frame, text="Minute")
        self.min_menu_label.pack(pady=10, padx=10)

        self.drop_minutes = ttk.Combobox(self.main_frame, values=minutes)
        self.drop_minutes.current(0)
        self.drop_minutes.pack(pady=10, padx=10)

        self.sec_menu_label = ttk.Label(self.main_frame, text="Second")
        self.sec_menu_label.pack(side=tk.RIGHT, pady=10, padx=10)

        self.drop_seconds = ttk.Combobox(self.main_frame, values=seconds)
        self.drop_seconds.current(0)
        self.drop_seconds.pack(side=tk.RIGHT, pady=10, padx=10)

        self.day_menu_label = ttk.Label(self.main_frame, text="Day")
        self.day_menu_label.pack(pady=10)

        cur_year = int(datetime.datetime.now().year)
        cur_month = int(datetime.datetime.now().month)
        cur_day = int(datetime.datetime.now().day)

        self.cal = Calendar(self.main_frame, selectmode='day',
                            year=cur_year, month=cur_month,
                            day=cur_day, date_pattern='dd/mm/yyyy')

        # self.cal.place(relx=0.5, rely=0.9)# need to fix placings




if __name__ == "__main__":
    window = Routing_Comparisons_Windows()
    window.mainloop()