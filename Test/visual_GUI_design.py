import datetime
import tkinter as tk
from tkinter import ttk, Scrollbar
from tkcalendar import Calendar, DateEntry
import GUI.RCW_Controller as rcwc
from Utilities.Getters import routing_algorithms, hours, minutes, seconds, days_of_the_week, rain_intensity_values
import datetime
import tkinter as tk
from tkinter import ttk, Scrollbar
from tkcalendar import Calendar, DateEntry
import GUI.RCW_Controller as rcwc
from Utilities.Getters import routing_algorithms, hours, minutes, seconds, days_of_the_week, rain_intensity_values

class Routing_Comparisons_Windows(tk.Tk):
    def __init__(self, controller=None):
        # self.root = self
        self.rcwc = rcwc.RCW_Controller(self, controller)
        super().__init__()
        self.controller = controller
        self.title("Car Routing Comparisons and Statistics")

        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        # Place the scrollbar in the grid with rowspan to cover the entire canvas
        self.scrollbar.grid(row=0, column=1, sticky="ns", rowspan=100)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)

        # Rest of your code...

        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.main_frame.grid(row=0, column=0, padx=0, pady=10, sticky="nsew")

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    window = Routing_Comparisons_Windows()
    window.mainloop()
