import matplotlib.pyplot as plt

from Utilities import Errors as errors
from Utilities.Getters import *



class DCRW_Controller:
    def __init__(self,view, controller):
        self.view = view
        self.controller = controller
        self.car_times_files = None
        self.run_time_files = None
        self.chosen_car_times_file = None
        self.chosen_run_time_file = None
        self.algorithm_statistics_cars = None
        self.algorithm_statistics_run_times = None



    # def show_numerical_statistics(self):
    #     self.view.withdraw()
    #     self.controller.start_numerical_statistics_window()

    def load_past_results(self):
        all_results_files =  self.controller.get_run_times_and_cars_times_files()
        self.car_times_files = all_results_files[cars_times_file_name]
        self.run_time_files = all_results_files[run_time_data_file_name]
        self.view.add_existing_car_times_files(self.car_times_files)

    def display_algorithms_statistics(self):
        if self.chosen_car_times_file is None:
            errors.no_file_chosen_error()
            return
        self.algorithm_statistics_cars = self.controller.calculate_car_times_statistics(self.chosen_car_times_file)
        self.view.set_textbox_statistics(self.algorithm_statistics_cars)

    def back_to_menu(self):
        # Destroy the current simulation window if it exists
        self.view.destroy()

        # Unhide the main window
        # self.view.deiconify()
        self.controller.start_main_window()

    def confirm(self,selected_file,treeview):
        print(self.car_times_files)
        print(self.run_time_files)
        selected_file = self.get_fixed_file_name_from_treeview(selected_file,treeview)
        print(selected_file)
        if selected_file is None:
            errors.no_file_chosen_error()
            return
        if selected_file in self.car_times_files:
            self.chosen_car_times_file = selected_file
        elif selected_file in self.run_time_files:
            self.chosen_run_time_file = selected_file
        self.display_algorithms_statistics()
        return

    def get_fixed_file_name_from_treeview(self,selected_file,treeview):
        if selected_file is None:
            return None
        return self.view.simulation_id_from_treeview(selected_file,treeview)
