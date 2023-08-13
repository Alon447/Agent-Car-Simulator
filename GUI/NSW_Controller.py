from GUI import Insert_Car_Window as icw


class NSW_Controller:
    def __init__(self, view, controller):
        self.map_loaded = False
        self.ready_to_start = False
        self.view = view
        self.controller = controller
        self.blocked_roads = []


    def add_new_car(self):
        if self.map_loaded:
            icw.Insert_Car_Window(self.view)
        else:
            self.view.no_map_loaded_error()
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
        self.controller.start_main()

    def load_simulation(self):
        # Code to load a simulation
        print("Loading simulation")

    def open_settings(self):
        # Code to open settings
        print("Opening settings")

    def load_city_map(self):
        city_name = self.view.get_city_name()
        self.map_loaded = self.controller.load_city_map(city_name)
        if self.map_loaded:
            print("loaded city map")
            self.view.set_load_status_label("City map loaded")
        else:
            print("failed to load city map")
            self.view.set_load_status_label("Failed to load city map")

