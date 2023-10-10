
#TODO: add functions to support loading existin simulation from file
class Main_Window_Controller:
    """
    This class is used to control the main window (first menu) of the program
    implements methods for all the buttons in the main window
    """
    def __init__(self, view, controller):
        self.view = view
        self.controller = controller

    def start_new_simulation(self):
        # self.quit()
        self.view.destroy()
        self.controller.start_new_simulation_window()

    def load_simulation(self):
        # Code to load a simulation
        print("Loading simulation")
        self.view.destroy()
        self.controller.load_simulation_window()

    def back_to_main_menu(self):
        # Destroy the current simulation window if it exists
        if hasattr(self.view, "new_window"):
            self.view.new_window.destroy()
        # Unhide the main window
        self.view.deiconify()

    def quit(self):
        self.view.destroy()

    def open_settings(self):
        # Code to open settings
        print("Opening settings")
