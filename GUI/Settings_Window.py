# external imports
import os
import tkinter as tk
from tkinter import ttk

# internal imports
from Utilities.Getters import get_specific_directory, Q_Tables_directory, Graphs_directory, Speeds_Data_directory, Results_directory


class Settings_Window(tk.Tk):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Settings")
        self.geometry("800x600")  # Set the dimensions of the new window (width x height)

        self.font = ("Arial", 12)

        self.create_main_frame()

        self.create_settings_sections()

        self.create_confirm_button()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 20)

    def create_settings_sections(self):
        sections_data = [("Q Learning Number Of Steps", self.create_steps_section),
            ("Q Learning Number Of Episodes", self.create_episodes_section),
            ("Q Learning Learning Rate", self.create_learning_rate_section),
            ("Q Learning Discount Factor", self.create_discount_factor_section),
            ("Q Learning Epsilon", self.create_epsilon_section),
            ("Car Duration (Hours)", self.create_car_duration_section),
            ("Remove Saved Q Tables", self.create_remove_saved_q_tables_section),
            ("Remove Saved Speeds Data", self.create_remove_saved_speeds_data_section),
            ("Remove Saved Graphs", self.create_remove_saved_speeds_data_section),
            ("Remove Saved Results", self.create_remove_saved_results_section)]

        for idx, (section_title, section_creation_function) in enumerate(sections_data):
            if idx % 2 == 0:
                outer_frame = ttk.Frame(self.main_frame)
                outer_frame.pack(fill = tk.BOTH, expand = True, pady = 10)

            section_frame = ttk.LabelFrame(outer_frame, text = section_title)
            section_frame.pack(side = tk.LEFT, padx = 10, pady = 5, fill = tk.BOTH, expand = True)

            section_creation_function(section_frame)

    def create_steps_section(self, parent_frame):
        self.steps_entry = tk.Text(parent_frame, width = 15, height = 1, font = self.font)
        self.steps_entry.pack(pady = 5)

        self.steps_entry.insert(tk.END, "200")

    def create_episodes_section(self, parent_frame):
        self.episodes_entry = tk.Text(parent_frame, width = 15, height = 1, font = self.font)
        self.episodes_entry.pack(pady = 5)

        self.episodes_entry.insert(tk.END, "2000")

    def create_learning_rate_section(self, parent_frame):
        self.learning_entry = tk.Text(parent_frame, width = 15, height = 1, font = self.font)
        self.learning_entry.pack(pady = 5)

        self.learning_entry.insert(tk.END, "0.1")

    def create_discount_factor_section(self, parent_frame):
        self.discount_entry = tk.Text(parent_frame, width = 15, height = 1, font = self.font)
        self.discount_entry.pack(pady = 5)

        self.discount_entry.insert(tk.END, "0.9")

    def create_epsilon_section(self, parent_frame):
        self.epsilon_entry = tk.Text(parent_frame, width = 15, height = 1, font = self.font)
        self.epsilon_entry.pack(pady = 5)

        self.epsilon_entry.insert(tk.END, "0.2")

    def create_car_duration_section(self, parent_frame):
        self.car_duration_entry = tk.Text(parent_frame, width = 15, height = 1, font = self.font)
        self.car_duration_entry.pack(pady = 5)

        self.car_duration_entry.insert(tk.END, "2")

    def create_remove_saved_q_tables_section(self, parent_frame):
        self.remove_saved_q_tables_button = ttk.Button(parent_frame, text = "Remove Saved Q Tables", command = self.remove_saved_q_tables)
        self.remove_saved_q_tables_button.pack(pady = 5)

    def create_remove_saved_speeds_data_section(self, parent_frame):
        self.remove_saved_speeds_data_button = ttk.Button(parent_frame, text = "Remove Saved Speeds Data", command = self.remove_saved_speeds_data)
        self.remove_saved_speeds_data_button.pack(pady = 5)

    def create_remove_saved_graphs_section(self, parent_frame):
        self.remove_saved_graphs_button = ttk.Button(parent_frame, text = "Remove Saved Graphs", command = self.remove_saved_graphs)
        self.remove_saved_graphs_button.pack(pady = 5)

    def create_remove_saved_results_section(self, parent_frame):
        self.remove_saved_results_button = ttk.Button(parent_frame, text = "Remove Saved Results", command = self.remove_saved_results)
        self.remove_saved_results_button.pack(pady = 5)

    def create_confirm_button(self):
        confirm_frame = ttk.Frame(self.main_frame)
        confirm_frame.pack(pady = 10)

        self.confirm_button = ttk.Button(confirm_frame, text = "Confirm", command = self.confirm_settings)
        self.confirm_button.pack()

    def confirm_settings(self):
        self.controller.confirm_settings(
            steps = self.steps_entry.get("1.0", 'end').replace('\n', ''),
            episodes = self.episodes_entry.get("1.0", 'end').replace('\n', ''),
            learning_rate = self.learning_entry.get("1.0", 'end').replace('\n', ''),
            discount_factor = self.discount_entry.get("1.0", 'end').replace('\n', ''),
            epsilon = self.epsilon_entry.get("1.0", 'end').replace('\n', ''),
            car_duration = self.car_duration_entry.get("1.0", 'end').replace('\n', ''))
        self.destroy()

        # Unhide the main window
        # self.view.deiconify()
        self.controller.start_main_window()

    def remove_saved_q_tables(self):
        directory_path = get_specific_directory(Q_Tables_directory)
        for file in os.listdir(directory_path):
            if file.endswith(".pkl"):
                print(f"{os.path.join(directory_path, file)} was deleted")
                os.remove(os.path.join(directory_path, file))
        return

    def remove_saved_speeds_data(self):
        directory_path = get_specific_directory(Speeds_Data_directory)
        for file in os.listdir(directory_path):
            if file.endswith(".json"):
                print(f"{os.path.join(directory_path, file)} was deleted")
                os.remove(os.path.join(directory_path, file))
        return

    def remove_saved_graphs(self):
        directory_path = get_specific_directory(Graphs_directory)
        for file in os.listdir(directory_path):
            if file.endswith(".graphml"):
                print(f"{os.path.join(directory_path, file)} was deleted")
                os.remove(os.path.join(directory_path, file))
        return

    def remove_saved_results(self):
        directory_path = get_specific_directory(Results_directory)
        for file in os.listdir(directory_path):
            if file.endswith(".json"):
                print(f"{os.path.join(directory_path, file)} was deleted")
                os.remove(os.path.join(directory_path, file))
        return
    def main(self):
        self.mainloop()