
# class Window_Controller:

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
    if hasattr(self, "new_window"):
        self.new_window.destroy()
    # Unhide the main window
    self.root.deiconify()


def load_simulation(self):
    # Code to load a simulation
    print("Loading simulation")


def open_settings(self):
    # Code to open settings
    print("Opening settings")