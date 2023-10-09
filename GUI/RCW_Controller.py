import datetime

from GUI import Map_Src_Dst_Choose as msdc


# TODO: add functions to send the car parameters to the controller
class RCW_Controller:
    def __init__(self, view, controller):

        self.view = view
        self.controller = controller
        self.cars_amount = 0
        self.simulations_amount = 0
        self.used_algorithms = {}  # key: algorithm name, value: boolean

    def toggle_algorithm(self, algorithm, algorithm_var):
        self.used_algorithms[algorithm] = algorithm_var.get()

    def load_city_map(self):
        city_name = self.view.get_city_name()
        is_map_loaded = self.controller.load_city_map(city_name)
        if is_map_loaded:
            print("loaded city map")
            self.view.set_load_status_label("City map loaded")
            self.map_loaded = True
        else:
            print("failed to load city map")
            self.view.set_load_status_label("Failed to load city map")
            self.map_loaded = False


