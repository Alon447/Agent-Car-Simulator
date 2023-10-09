import tkinter as tk
from tkinter import ttk

import GUI.Main_Window_Controller as mwc

class Main_Window(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.mwc = mwc.Main_Window_Controller(self, controller)
        self.controller = controller
        self.title("Car Navigation")

        # Create a Canvas widget with a scrollbar
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # Add a vertical scrollbar for the canvas
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configure the canvas to work with the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to hold your buttons
        self.main_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor=tk.NW)

        self.title_label = ttk.Label(self.main_frame, text="Car Navigation System", font=("Ariel", 20))
        self.title_label.grid(row=0, column=0, pady=20)

        button_style = ttk.Style()
        button_style.configure("TButton", font=("Ariel", 14))

        # start new simulation button
        for i in range(100):
            self.new_simulation_button = ttk.Button(self.main_frame, text="Start New Simulation",
                                                    command=self.mwc.start_new_simulation, width=10)
            self.new_simulation_button.grid(row=i+1, column=0, pady=10)

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
