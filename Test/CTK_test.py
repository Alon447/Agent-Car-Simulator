import customtkinter as ctk
import GUI.Main_Window_Controller as mwc


class Main_Window(ctk.CTk):
    def __init__(self, controller):
        # self.root = self
        self.mwc = mwc.Main_Window_Controller(self, controller)
        super().__init__()
        self.controller = controller
        self.title("Car Navigation")
        # self.make
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=100, pady=100)

        self.title_label = ctk.CTkLabel(self.main_frame, text="Car Navigation System", font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        # button_style = ctk.CTkStyle()
        # button_style.configure("TButton", font=("Helvetica", 14))

        self.new_simulation_button = ctk.CTkButton(self.main_frame, text="Start New Simulation",
                                                   command=self.mwc.start_new_simulation, width=20)
        self.new_simulation_button.pack(pady=10)

        self.load_simulation_button = ctk.CTkButton(self.main_frame, text="Load Simulation",
                                                    command=self.mwc.load_simulation, width=20)
        self.load_simulation_button.pack(pady=10)

        self.settings_button = ctk.CTkButton(self.main_frame, text="Settings", command=self.mwc.open_settings, width=20)
        self.settings_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(self.main_frame, text="Exit", command=self.mwc.quit, width=20)
        self.exit_button.pack(pady=10)

    def main(self):
        self.mainloop()

class MyFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.label = ctk.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")



import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np

# plt.rcParams["figure.figsize"] = [7.00, 3.50]
# plt.rcParams["figure.autolayout"] = True

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

plt.axes(xlim=(0, 2), ylim=(-2, 2))
fig = plt.Figure(dpi=100)
ax = fig.add_subplot(xlim=(0, 2), ylim=(-1, 1))
line, = ax.plot([], [], lw=2)
# line, = plt.plot([], [], lw=2)
canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

# canvas.mpl_connect(
#     "key_press_event", lambda event: print(f"you pressed {event.key}"))
# canvas.mpl_connect("key_press_event", key_press_handler)

button = tkinter.Button(master=root, text="Quit", command=root.quit)
button.pack(side=tkinter.BOTTOM)

toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def init():
    # line.set_data([], [])
    return line,

def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

anim= animation.FuncAnimation(fig, animate, init_func=init,frames=200, interval=20, blit=True)

tkinter.mainloop()
# app = App()
# app.mainloop()
#
# if __name__ == '__main__':
#     import Controller.Controller as Controller
#     c = Controller.Controller()
#     mw = Main_Window(c)
#     mw.mainloop()

# Import module
from tkinter import *

# Create object
root = Tk()

# Adjust size
root.geometry("200x200")


# Change the label text
def show():
    label.config(text=clicked.get())


# Dropdown menu options
options = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set("Monday")

# Create Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.pack()

# Create button, it will change label text
button = Button(root, text="click Me", command=show).pack()

# Create Label
label = Label(root, text=" ")
label.pack()

# Execute tkinter
root.mainloop()
