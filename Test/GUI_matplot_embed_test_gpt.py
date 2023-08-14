# import tkinter as tk
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.animation import FuncAnimation
# import numpy as np
# import matplotlib.pyplot as plt
#
# class MyAnimation:
#     def __init__(self, figure):
#         self.figure = figure
#         self.ax = self.figure.add_subplot(xlim=(0, 2), ylim=(-1, 1))
#         self.line, = self.ax.plot([], [], lw=2)
#         self.animation = FuncAnimation(self.figure, self.update, frames=np.linspace(0, 2 * np.pi, 128), init_func=self.init, blit=True)
#
#     def init(self):
#         self.line.set_data([], [])
#         return self.line,
#
#     def update(self, frame):
#         x = np.linspace(0, 2 * np.pi, 1000)
#         y = np.sin(x + frame)
#         self.line.set_data(x, y)
#         return self.line,
#
# class MyTkinterApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Matplotlib Animation in Tkinter")
#
#         self.figure = Figure(figsize=(5, 4), dpi=100)
#         self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
#         self.canvas.get_tk_widget().pack()
#
#         self.animation = MyAnimation(self.figure)
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = MyTkinterApp(root)
#     root.mainloop()
#
# # import tkinter as tk
# # from matplotlib.figure import Figure
# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# # from matplotlib.animation import FuncAnimation
# # import numpy as np
# #
# # class MyAnimation:
# #     def __init__(self, figure):
# #         self.figure = figure
# #         self.ax = self.figure.add_subplot(xlim=(0, 2), ylim=(-1, 1))
# #         self.line, = self.ax.plot([], [], lw=2)
# #         self.animation = FuncAnimation(self.figure, self.update, frames=np.linspace(0, 2 * np.pi, 128), init_func=self.init, blit=True)
# #
# #     def init(self):
# #         self.line.set_data([], [])
# #         return self.line,
# #
# #     def update(self, frame):
# #         x = np.linspace(0, 2 * np.pi, 1000)
# #         y = np.sin(x + frame)
# #         self.line.set_data(x, y)
# #         return self.line,
# #
# # class MyTkinterWindow(tk.Tk):
# #     def __init__(self):
# #         super().__init__()
# #         self.title("Matplotlib Animation in Custom Tkinter Window")
# #
# #         self.figure = Figure(figsize=(5, 4), dpi=100)
# #         self.canvas = FigureCanvasTkAgg(self.figure, master=self)
# #         self.canvas.get_tk_widget().pack()
# #
# #         self.animation = MyAnimation(self.figure)
# #
# # if __name__ == "__main__":
# #     app = MyTkinterWindow()
# #     app.mainloop()
# #
# # import tkinter as tk
# # from matplotlib.figure import Figure
# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# # from matplotlib.animation import FuncAnimation
# # import osmnx as ox
# #
# # class MyOSMNXAnimation:
# #     def __init__(self, ax):
# #         self.ax = ax
# #         self.graph = ox.graph_from_place("tel aviv, israel", network_type="drive")
# #         self.edge_colors = "red"  # Customize as needed
# #         self.node_colors = "blue"  # Customize as needed
# #
# #     def update(self, frame):
# #         # Update animation frame based on your logic
# #         pass
# #
# # class MyTkinterWindow(tk.Tk):
# #     def __init__(self):
# #         super().__init__()
# #         self.title("OSMNX Animation in Custom Tkinter Window")
# #
# #         self.figure = Figure(figsize=(10, 10), dpi=100)
# #         self.canvas = FigureCanvasTkAgg(self.figure, master=self)
# #         self.canvas.get_tk_widget().pack()
# #
# #         self.ax = self.figure.add_subplot(111)
# #         self.osmnx_animation = MyOSMNXAnimation(self.ax)
# #         self.animation = FuncAnimation(self.figure, self.osmnx_animation.update, frames=range(100), interval=100)
# #
# # if __name__ == "__main__":
# #     app = MyTkinterWindow()
# #     app.mainloop()
# #
# # import tkinter as tk
# # from matplotlib.figure import Figure
# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# # from matplotlib.animation import FuncAnimation
# # from GUI import Animate_Simulation as asim # Replace with the actual import path
# #
# # class AnimationApp(tk.Tk):
# #     def __init__(self):
# #         super().__init__()
# #         self.title("Animation in Tkinter")
# #
# #         self.figure = Figure(figsize=(10, 10), dpi=100)
# #         self.canvas = FigureCanvasTkAgg(self.figure, master=self)
# #         self.canvas.get_tk_widget().pack()
# #
# #         self.animation = asim.Animate_Simulation()
# #         self.ax = self.figure.add_subplot(111)
# #         self.animation.create_animation(self.ax)
# #
# # if __name__ == "__main__":
# #     app = AnimationApp()
# #     app.mainloop()

import numpy as np
import matplotlib.pyplot as plt
import time

x, y = np.random.random((2, 10))

fig, ax = plt.subplots()
scat = ax.scatter(x, y, s=150)

# Show the figure, then remove one point every second.
fig.show()
for _ in range(10):
    time.sleep(1)
    xy = np.delete(scat.get_offsets(), 0, axis=0)
    scat.set_offsets(xy)
    plt.draw()