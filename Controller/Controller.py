from GUI.Main_Window import Main_Window
from GUI.New_Simulation_Window import New_Simulation_Window


class Controller:

    def __init__(self):
        self.view = None
        self.model = None

    #view control
    def start_main(self):
        self.view = Main_Window(self)
        self.view.main()

    def start_new_simulation(self):
        self.view = New_Simulation_Window(self)
        self.view.main()


    #model control



    #gather settings
    def add_car(self):
        pass


if __name__ == "__main__":
    controller = Controller()
    controller.start_main()
