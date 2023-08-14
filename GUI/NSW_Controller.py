from GUI import Insert_Car_Window as icw

#TODO: add functionality of sending simulation parameters to the controller
class NSW_Controller:
    def __init__(self, view, controller):
        self.map_loaded = False
        self.ready_to_start = False
        self.view = view
        self.controller = controller
        self.blocked_roads = []
        self.simulation_manager_ready = False
        self.simulation_params_dict = {}
        self.simulation_params_dict["map loaded"] = None
        self.simulation_params_dict["simulation duration"] = None
        self.simulation_params_dict["simulation starting_time"] = False
        self.simulation_params_dict["rain intensity"] = False
        self.simulation_params_dict["traffic lights"] = False
        self.simulation_params_dict["add traffic white noise"] = False

    def add_new_car(self):

        # if not self.check_simulation_requirements():
        #     self.view.simulation_requirements_error()
        #     return
        # else:
        #     self.view.no_map_loaded_error()
        if not self.map_loaded:
            self.view.no_map_loaded_error()
        else:
            self.icw = icw.Insert_Car_Window(self.view,self.controller)


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

        self.view.destroy()
        # Unhide the main window
        # self.view.deiconify()
        self.controller.start_main_window()

    def load_simulation(self):
        # Code to load a simulation
        print("Loading simulation")

    def open_settings(self):
        # Code to open settings
        print("Opening settings")

    def load_city_map(self):
        city_name = self.view.get_city_name()
        ml = self.simulation_params_dict["map loaded"] = self.controller.load_city_map(city_name)
        if ml:
            print("loaded city map")
            self.view.set_load_status_label("City map loaded")
            self.map_loaded = True
        else:
            print("failed to load city map")
            self.view.set_load_status_label("Failed to load city map")
            self.map_loaded = False

    def check_simulation_requirements(self):
        if self.simulation_params_dict["map loaded"] is None or self.simulation_params_dict[
            "simulation duration"] is None:
            return False
        return True
