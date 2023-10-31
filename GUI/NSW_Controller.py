from GUI import Insert_Car_Window as icw
from GUI import Insert_Block_Road as ibr
from Utilities import Getters as gtrs
from Utilities import Errors as errors


class NSW_Controller:
    """
    This class is used to control the new simulation window
    NSW stands for New Simulation Window
    """
    def __init__(self, view, controller):
        self.map_loaded = False
        self.ready_to_start = False
        self.view = view
        self.controller = controller
        self.blocked_road = None
        self.blocked_roads = []
        self.simulation_manager_ready = False
        self.simulation_params_dict = {}
        self.initialize_simulation_params_dict()


    def initialize_simulation_params_dict(self):
        self.simulation_params_dict["map loaded"] = None
        self.simulation_params_dict["simulation duration"] = None
        self.simulation_params_dict["simulation starting_time"] = False
        self.simulation_params_dict["rain intensity"] = False
        self.simulation_params_dict["traffic lights"] = False
        self.simulation_params_dict["add traffic white noise"] = False
        return

    def add_new_car(self):
        if not self.map_loaded:
            errors.no_map_loaded_error()
        else:
            self.icw = icw.Insert_Car_Window(self.view,self.controller)

    def block_road(self):
        # Code for blocking a road
        print("Blocking road")
        if not self.map_loaded:
            errors.no_map_loaded_error()
        else:
            self.blocked_road = ibr.Insert_Block_Road(self.view, self.controller)

    def unblock_all_roads(self):
        # Code for unblocking all roads
        self.controller.unblock_all_roads()
        print("Unblocking all roads")

    def start_simulation(self):
        """
        Code for starting the simulation
            needed parameters:
              simulation duration
              simulation starting time
              rain intensity
              traffic lights
              add traffic white noise
        :return:
        """

        if not self.controller.check_can_run_simulation():
            errors.cant_run_simulation_error()
            return
        rain_intensity = int(self.view.get_rain_intensity())
        traffic_lights = self.view.get_traffic_lights()
        add_traffic_white_noise = self.view.get_traffic_white_noise()
        plot_results = self.view.get_plot_results()

        self.controller.start_simulation(traffic_lights, rain_intensity, add_traffic_white_noise,plot_results)
        print("Starting simulation")

    def back_to_main_menu(self):
        # Destroy the current simulation window if it exists
        self.view.destroy()

        # Unhide the main window
        # self.view.deiconify()
        self.controller.start_main_window()

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