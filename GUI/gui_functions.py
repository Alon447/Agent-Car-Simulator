import tkinter as tk
from tkinter import ttk

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
        print("Starting new simulation")

        new_window = tk.Toplevel(self.root)
        new_window.title("New Simulation")
        new_window.geometry("550x550")  # Set the dimensions of the new window (width x height)

        # Add a spacer frame above the title label
        spacer_frame = ttk.Frame(new_window)
        spacer_frame.pack(pady=50)

        self.title_label = ttk.Label(new_window, text="Car Navigation System", font=("Helvetica", 20))
        self.title_label.pack(pady=20)


        self.add_car_button = ttk.Button(new_window, text="Add New Car")
        self.add_car_button.pack(pady=10)

        self.block_road_button = ttk.Button(new_window, text="Block Road")
        self.block_road_button.pack(pady=10)

        self.unblock_all_roads_button = ttk.Button(new_window, text="Unblock All Roads")
        self.unblock_all_roads_button.pack(pady=10)

        self.start_simulation_button = ttk.Button(new_window, text="Start Simulation")
        self.start_simulation_button.pack(pady=10)

        self.back_to_main_menu_button = ttk.Button(new_window, text="Back to Main Menu", command=new_window.destroy)
        self.back_to_main_menu_button.pack(pady=10)

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
