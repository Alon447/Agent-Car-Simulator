import tkinter as tk
from tkinter import ttk

import GUI.Main_Window_Controller as mwc


# TODO: Add menu to load simulation by name/choose from list of saved simulations
#   also add functionality as written in the controller file
#   maybe option to load statistics only?
class Main_Window(tk.Tk):
    """
    This class is used to create the main window (first menu) of the program
    """
    def __init__(self, controller):
        """
        This method initializes the main window
        creates all the widgets and places them in the window
        :param controller:
        """
        super().__init__()

        self.mwc = mwc.Main_Window_Controller(self, controller)
        self.controller = controller
        self.title("Car Navigation")
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.grid(row=0, column=0, padx=100, pady=100)

        self.title_label = ttk.Label(self.main_frame, text="Car Navigation System", font=("Ariel", 20))
        self.title_label.pack(pady=20)

        button_style = ttk.Style()
        button_style.configure("TButton", font=("Ariel", 14))

        # start new simulation button
        self.new_simulation_button = ttk.Button(self.main_frame, text="Start New Simulation",
                                                command=self.mwc.start_new_simulation, width=20)
        self.new_simulation_button.pack(pady=10)

        # load simulation button
        self.load_simulation_button = ttk.Button(self.main_frame, text="Load Simulation",
                                                 command=self.mwc.load_simulation, width=20)
        self.load_simulation_button.pack(pady=10)

        # route comparison button
        self.route_comparison_button = ttk.Button(self.main_frame, text="Route Comparison",
                                                    command=self.mwc.start_route_comparison, width=20)
        self.route_comparison_button.pack(pady=10)

        self.display_comparisons_results_button = ttk.Button(self.main_frame, text="Display Comparisons Results",
                                                    command=self.mwc.display_comparisons_results_window, width=20)
        self.display_comparisons_results_button.pack(pady=10)

        # settings button
        self.settings_button = ttk.Button(self.main_frame, text="Settings", command=self.mwc.open_settings, width=20)
        self.settings_button.pack(pady=10)

        # exit button
        self.exit_button = ttk.Button(self.main_frame, text="Exit", command=self.mwc.quit, width=20)
        self.exit_button.pack(pady=10)



    def main(self):
        self.mainloop()
