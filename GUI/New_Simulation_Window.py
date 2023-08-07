import tkinter as tk
from tkinter import ttk
import GUI.NSW_Controller as nswc


class New_Simulation_Window(tk.Tk):
    def __init__(self, controller):
        self.nswc = nswc.NSW_Controller(self, controller)
        super().__init__()
        self.title("New Simulation")
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.grid(row=0, column=0, padx=100, pady=100)  # Set the dimensions of the new window (width x height)

        # Add a spacer frame above the title label
        # spacer_frame = ttk.Frame(self.main_frame)
        # spacer_frame.pack(pady=50)

        self.title_label = ttk.Label(self.main_frame, text="Car Navigation System", font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        self.add_car_button = ttk.Button(self.main_frame, text="Add New Car", command=self.nswc.add_new_car)
        self.add_car_button.pack(pady=10)

        self.block_road_button = ttk.Button(self.main_frame, text="Block Road", command=self.nswc.block_road)
        self.block_road_button.pack(pady=10)

        self.unblock_all_roads_button = ttk.Button(self.main_frame, text="Unblock All Roads",
                                                   command=self.nswc.unblock_all_roads)
        self.unblock_all_roads_button.pack(pady=10)

        self.start_simulation_button = ttk.Button(self.main_frame, text="Start Simulation",
                                                  command=self.nswc.start_simulation)
        self.start_simulation_button.pack(pady=10)

        self.back_to_main_menu_button = ttk.Button(self.main_frame, text="Back to Main Menu",
                                                   command=self.nswc.back_to_main_menu)
        self.back_to_main_menu_button.pack(pady=10)

    def main(self):
        self.mainloop()
