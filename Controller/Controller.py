import GUI
from GUI.Main_Gui_Functions import Main_GUI_Functions
import tkinter as tk

class Controller:
    def __init__(self):
        self.view = None
        self.model = None
        self.tkroot = tk.Tk()

    def start(self):
        # self.view.main(self)
        self.tkroot.mainloop()

    def set_view(self, view):
        self.view = view

    def set_model(self, model):
        self.model = model
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
        if hasattr(self.view, "new_window"):
            self.view.new_window.destroy()
        # Unhide the main window
        self.view.root.deiconify()

    def load_simulation(self):
        # Code to load a simulation
        print("Loading simulation")

    def open_settings(self):
        # Code to open settings
        print("Opening settings")


if __name__ == "main":
    root = tk.Tk()
    controller = Controller()
    app = Main_GUI_Functions(root, controller)
    controller.set_view(app)
    controller.start()
