
class NSW_Controller:
    def __init__(self, view, controller):
        self.view = view
        self.controller = controller

    def add_new_car(self):
        print("Adding new car")

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