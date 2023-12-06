# external imports
import datetime
import json
import os

# internal imports
import Utilities.Results as Results

class LSW_Controller:
    """
    This class is used to control the new load simulation window
    NLSW stands for New Load Simulation Window
    """
    def __init__(self, view, controller):
        self.map_loaded = False
        self.ready_to_start = False
        self.view = view
        self.controller = controller
        self.blocked_roads = []
        self.simulation_manager_ready = False
        self.simulation_params_dict = {}

    def confirm(self, selected_simulation):
        """
        This function is used to confirm the user's choice of simulation to load
        :param selected_simulation:
        :return:
        """
        print("selected simulation: ", selected_simulation)
        if type(selected_simulation) is tuple:
            for item in selected_simulation:
                item_name = self.view.simulation_id_from_treeview(item).split(".")[0] # remove the .json from the name
                Results.plot_simulation_overview(item_name)
                self.controller.load_simulation(item_name)
        return

    def back_to_menu(self):
        # Destroy the current simulation window if it exists
        self.view.destroy()

        # Unhide the main window
        # self.view.deiconify()
        self.controller.start_main_window()

    def load_existing_simulations(self):
        past_simulations_array, path = self.controller.get_past_simulations()
        for simulation_name in past_simulations_array:
            file_path = path + "/" + simulation_name
            modification_time = os.path.getmtime(file_path)
            modification_datetime = datetime.datetime.fromtimestamp(modification_time).replace(microsecond=0)

            with open(file_path, 'r') as file:
                if file_path.endswith(".json"):
                    json_data = json.load(file)
                    self.view.add_existing_simulation(json_data, simulation_name, modification_datetime)

    def get_number_of_saves(self):
        return self.controller.get_past_simulations()[0].__len__()