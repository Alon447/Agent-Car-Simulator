import json


class NLSW_Controller:
    def __init__(self, view, model):
        self.map_loaded = False
        self.ready_to_start = False
        self.view = view
        self.model = model
        self.blocked_roads = []
        self.simulation_manager_ready = False
        self.simulation_params_dict = {}

    def load_city_map(self):
        city_name = self.view.get_city_name()
        ml = self.simulation_params_dict["map loaded"] = self.model.load_city_map(city_name)
        if ml:
            print("loaded city map")
            self.view.set_load_status_label("City map loaded")
            self.map_loaded = True
        else:
            print("failed to load city map")
            self.view.set_load_status_label("Failed to load city map")
            self.map_loaded = False

    def load_existing_simulations(self):
        past_simulations_array, path = self.model.get_past_simulations()
        for simulation_name in past_simulations_array:
            file_path = path + "/" + simulation_name
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                self.view.add_existing_simulation(json_data, simulation_name)


