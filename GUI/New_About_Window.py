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
        self.geometry("800x600")  # Set the dimensions of the new window (width x height)

        self.configure(bg = "#f5f5f5")  # Set the background color


        # add a text box
        self.text = tk.Text(wrap = tk.WORD,  bg="lightgray", width = 110, height = 100, border = 0)
        self.main_frame = tk.Frame(bg = "lightgray", bd = 5)
        self.main_frame.place(relwidth = 0.8, relheight = 0.8, relx = 0.1, rely = 0.1)
        # set our writing styles
        self.text.tag_config("header", font = ("Helvetica", 18, "bold"))
        self.text.tag_config("subheader", font = ("Helvetica", 14, "bold"))
        self.text.tag_config("normal",font = ("Ariel", 12))
        # insert the texts
        self.text.insert(tk.END, "Project Title\n", "header")
        self.text.insert(tk.END, "Car Navigation Simulator\n", "normal")
        self.text.insert(tk.END, "\nProject Key Features:\n\n", "header")
        self.text.insert(tk.END,"Start New Simulation - Used to create a new simulation of your choice,\n\n","subheader")
        self.text.insert(tk.END,"   First choose a city in the world and load its map.\n\n","normal")
        self.text.insert(tk.END,"   After that apply the desired settings\n\n","normal")
        self.text.insert(tk.END,"   Plot Q Learning Training Results - If selected it will print a plot with   \n\n","normal")
        self.text.insert(tk.END, "\nProject Objectives:\n", "header")
        self.text.insert(tk.END, "Our main objective is to create a navigation simulator that can simulate car navigation in a congested city, the car can navigates using different algorithms including:\n\n", "normal")
        self.text.insert(tk.END, "Q-learning algorithm that empowers vehicles to navigate using machine learning.\n\n", "normal")
        self.text.insert(tk.END, "Shortest path algorithm that minimizes the distance the car travels.\n\n", "normal")
        self.text.insert(tk.END, "Random algorithm that guesses the path with complete randomness.\n\n", "normal")

        self.text.insert(tk.END, "\nTeam Members:\n", "header")
        self.text.insert(tk.END, "Alon Reicher\n", "normal")
        self.text.insert(tk.END, "Liad Gam\n", "normal")

        self.text.config(state = tk.DISABLED)  # Disable editing

        self.text.grid(row = 0, column = 0, columnspan = 20)  # Use grid layout

        self.back_to_main_menu_button = ttk.Button(self.main_frame, text="Back to Main Menu",
                                                   command=self.back_to_main_menu)
        self.back_to_main_menu_button.grid(row=1, column=0, columnspan=2)

    # def back_to_main_menu(self):
    #     # Destroy the current simulation window if it exists
    #     self.destroy()
    #
    #     # Unhide the main window
    #     # self.view.deiconify()
    #     self.controller.start_main_window()
    #
    #     #return to main menu button
    #     self.back_button = ttk.Button(self, text = "Back to Main Menu", command = self.back_to_main_menu)
    #     self.back_button.grid(row = 1, column = 0, padx = 10, pady = 20)

    def main(self):
        self.mainloop()

    def back_to_main_menu(self):
        # Destroy the current window
        self.destroy()

        # Unhide the main window
        self.controller.start_main_window()