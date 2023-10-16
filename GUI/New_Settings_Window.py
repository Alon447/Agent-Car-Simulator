import tkinter as tk
from tkinter import ttk

class New_Settings_Window(tk.Tk):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Settings")
        self.geometry("800x600")  # Set the dimensions of the new window (width x height)

        # Add a spacer frame above the title label
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack()
        # Decide q learning parameters
        # steps
        self.steps_label = tk.Label(self.main_frame, text = "Enter Q Learning Number Of Steps:", font = ("Ariel", 14))
        self.steps_label.pack(pady = 10)

        self.steps_entry = tk.Text(self.main_frame, width = 15, height = 1, font = ("Ariel", 14))
        self.steps_entry.pack(pady = 10)

        self.steps_entry.insert(tk.END, "200")  # TODO: remove this line after testing
        # episodes
        self.episodes_label = tk.Label(self.main_frame, text = "Enter Q Learning Number Of Episodes:", font = ("Ariel", 14))
        self.episodes_label.pack(pady = 10)

        self.episodes_entry = tk.Text(self.main_frame, width = 15, height = 1, font = ("Ariel", 14))
        self.episodes_entry.pack(pady = 10)

        self.episodes_entry.insert(tk.END, "2000")  # TODO: remove this line after testing
        # car duration
        self.car_duration_label = tk.Label(self.main_frame, text = "Enter Car Duration (Hours):", font = ("Ariel", 14))
        self.car_duration_label.pack(pady = 10)

        self.car_duration_entry = tk.Text(self.main_frame, width = 15, height = 1, font = ("Ariel", 14))
        self.car_duration_entry.pack(pady = 10)

        self.car_duration_entry.insert(tk.END, "2")  # TODO: remove this line after testing

        # confirm button
        self.confirm_button = ttk.Button(self.main_frame, text = "Confirm", command = self.confirm_settings)
        self.confirm_button.pack(pady = 10)

    def confirm_settings(self):
        self.controller.confirm_settings(steps = self.steps_entry.get("1.0", 'end').replace('\n', ''),
                                         episodes = self.episodes_entry.get("1.0", 'end').replace('\n', ''),
                                         car_duration = self.car_duration_entry.get("1.0", 'end').replace('\n', ''))
        self.destroy()

        # Unhide the main window
        # self.view.deiconify()
        self.controller.start_main_window()

    def main(self):
        self.mainloop()