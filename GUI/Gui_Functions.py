import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring  # Import askstring from tkinter.simpledialog
from tkinter.simpledialog import Dialog

# class CustomInputDialog(Dialog):
#     def __init__(self, parent, title, prompts):
#         self.prompts = prompts
#         super().__init__(parent, title=title)
#
#     def body(self, frame):
#         self.entries = []
#         for prompt in self.prompts:
#             ttk.Label(frame, text=prompt).pack()
#             entry = ttk.Entry(frame)
#             entry.pack()
#             self.entries.append(entry)
#         return self.entries[0]  # Set initial focus

class CarNavigationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Navigation")

        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.grid(row=0, column=0, padx=100, pady=100)

        self.title_label = ttk.Label(self.main_frame, text="Car Navigation System", font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        button_style = ttk.Style()
        button_style.configure("TButton", font=("Helvetica", 14))

        self.new_simulation_button = ttk.Button(self.main_frame, text="Start New Simulation", command=self.start_new_simulation, width=20)
        self.new_simulation_button.pack(pady=10)

        self.load_simulation_button = ttk.Button(self.main_frame, text="Load Simulation", command=self.load_simulation, width=20)
        self.load_simulation_button.pack(pady=10)

        self.settings_button = ttk.Button(self.main_frame, text="Settings", command=self.open_settings, width=20)
        self.settings_button.pack(pady=10)

        self.exit_button = ttk.Button(self.main_frame, text="Exit", command=self.root.quit, width=20)
        self.exit_button.pack(pady=10)

    def start_new_simulation(self):
        # Code to start a new simulation
        self.root.withdraw()  # Hide the main window
        print("Starting new simulation")

        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("New Simulation")
        self.new_window.geometry("550x550")  # Set the dimensions of the new window (width x height)

        # Add a spacer frame above the title label
        spacer_frame = ttk.Frame(self.new_window)
        spacer_frame.pack(pady=50)

        self.title_label = ttk.Label(self.new_window, text="Car Navigation System", font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        self.add_car_button = ttk.Button(self.new_window, text="Add New Car", command=self.add_new_car)
        self.add_car_button.pack(pady=10)

        self.block_road_button = ttk.Button(self.new_window, text="Block Road", command=self.block_road)
        self.block_road_button.pack(pady=10)

        self.unblock_all_roads_button = ttk.Button(self.new_window, text="Unblock All Roads", command=self.unblock_all_roads)
        self.unblock_all_roads_button.pack(pady=10)

        self.start_simulation_button = ttk.Button(self.new_window, text="Start Simulation", command=self.start_simulation)
        self.start_simulation_button.pack(pady=10)

        self.back_to_main_menu_button = ttk.Button(self.new_window, text="Back to Main Menu", command=self.back_to_main_menu)
        self.back_to_main_menu_button.pack(pady=10)

    def add_new_car(self):
        print("Adding new car")

    def block_road(self):
        # Code for blocking a road
        print("Blocking road")

    def unblock_all_roads(self):
        # Code for unblocking all roads
        print("Unblocking all roads")

    def start_simulation(self):
        # Code for starting the simulation
        print("Starting simulation")

    def back_to_main_menu(self):
        # Destroy the current simulation window if it exists
        if hasattr(self, "new_window"):
            self.new_window.destroy()
        # Unhide the main window
        self.root.deiconify()
    def load_simulation(self):
        # Code to load a simulation
        print("Loading simulation")

    def open_settings(self):
        # Code to open settings
        print("Opening settings")

def main():
    root = tk.Tk()
    app = CarNavigationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
