# external imports
import os
import tkinter as tk
from tkinter import ttk

# internal imports
from Utilities.Getters import get_specific_directory, Q_Tables_directory, Graphs_directory, Speeds_Data_directory, Results_directory


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

        self.steps_entry.insert(tk.END, "200")

        # episodes
        self.episodes_label = tk.Label(self.main_frame, text = "Enter Q Learning Number Of Episodes:", font = ("Ariel", 14))
        self.episodes_label.pack(pady = 10)

        self.episodes_entry = tk.Text(self.main_frame, width = 15, height = 1, font = ("Ariel", 14))
        self.episodes_entry.pack(pady = 10)

        self.episodes_entry.insert(tk.END, "2000")

        # car duration
        self.car_duration_label = tk.Label(self.main_frame, text = "Enter Car Duration (Hours):", font = ("Ariel", 14))
        self.car_duration_label.pack(pady = 10)

        self.car_duration_entry = tk.Text(self.main_frame, width = 15, height = 1, font = ("Ariel", 14))
        self.car_duration_entry.pack(pady = 10)

        self.car_duration_entry.insert(tk.END, "2")

        # delete all q tables button
        self.delete_all_q_tables_button = ttk.Button(self.main_frame, text = "Delete All Saved Q Tables", command = self.remove_saved_q_tables)
        self.delete_all_q_tables_button.pack(pady = 10)

        # delete all speeds data button
        self.delete_all_q_tables_button = ttk.Button(self.main_frame, text = "Delete All Saved Speeds Data", command = self.remove_saved_speeds_data)
        self.delete_all_q_tables_button.pack(pady = 10)

        # delete all graphs button
        self.delete_all_q_tables_button = ttk.Button(self.main_frame, text = "Delete All Saved Graphs", command = self.remove_saved_graphs)
        self.delete_all_q_tables_button.pack(pady = 10)

        # delete all results button
        self.delete_all_q_tables_button = ttk.Button(self.main_frame, text = "Delete All Saved Results", command = self.remove_saved_results)
        self.delete_all_q_tables_button.pack(pady = 10)


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