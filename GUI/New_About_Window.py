import tkinter as tk
from tkinter import ttk

class New_About_Window(tk.Tk):
    """
    This class is used to create the About Us window
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("About the Project")
        self.geometry("1000x600")  # Set the dimensions of the new window (width x height)

        self.configure(bg = "#f5f5f5")  # Set the background color

        about_us_text = """
           **About Us**

           **Project Name:** Car Navigation Simulator

           **Project Purpose/Description:**
           The Car Navigation Simulator is a cutting-edge project designed to revolutionize car navigation experiences. 
           Our simulator offers a realistic and dynamic environment that mimics city navigation, complete with traffic congestion, traffic lights, and blocked roads. 
           The primary goal of this project is to develop a sophisticated Q-learning algorithm that enables efficient car navigation within this complex urban landscape.

           **Project Goals/Objectives:**
           Our main objective is to create a Q-learning algorithm that empowers vehicles to navigate cities with precision and efficiency. 
           Through the Car Navigation Simulator, we aim to achieve the following goals:

           1. **Realistic Simulation:** Provide a highly realistic simulation environment that replicates the challenges and intricacies of real-world city navigation.

           2. **Traffic Dynamics:** Simulate dynamic traffic conditions, including traffic jams and congestion, to test and enhance navigation algorithms.

           3. **Traffic Light Interaction:** Model the interaction between vehicles and traffic lights, allowing for the development and testing of strategies to optimize traffic flow.

           4. **Blocked Roads Handling:** Implement scenarios where roads become inaccessible, challenging the algorithm to find alternative routes.

           5. **Efficiency and Learning:** Develop a Q-learning algorithm that continuously learns and adapts, enabling vehicles to find the most efficient routes.

           **Team Members:**
           - Alon Reicher
           - Liad Gam

           The Car Navigation Simulator project represents a significant step forward in the field of navigation and artificial intelligence. 
           With a commitment to innovation and real-world relevance, 
           our team is dedicated to creating a simulator that not only replicates the challenges of city driving but also helps shape the future of efficient urban navigation.
           """

        self.settings_label = ttk.Label(self, text = about_us_text, font = ("Arial", 12), background = "#f5f5f5",
                                        wraplength = 600)
        self.settings_label.grid(row = 0, column = 0, padx = 10, pady = 20)

        #return to main menu button
        self.back_button = ttk.Button(self, text = "Back to Main Menu", command = self.back_to_main_menu)
        self.back_button.grid(row = 1, column = 0, padx = 10, pady = 20)

    def main(self):
        self.mainloop()

    def back_to_main_menu(self):
        # Destroy the current window
        self.destroy()

        # Unhide the main window
        self.controller.start_main_window()