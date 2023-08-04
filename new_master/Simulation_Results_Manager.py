import json

import pandas as pd
from matplotlib import pyplot as plt


class Simulation_Results_Manager:
    def __init__(self):
        self.simulation_results = []


    def save_results_to_JSON(self, results):
        self.simulation_results.append(results)
        with open('simulation_results.json', 'w') as outfile:
            json.dump(results, outfile, indent=4)

    def read_results_from_JSON(self):
        with open('simulation_results.json', 'r') as infile:
            new_simulation_results = json.load(infile)
        return new_simulation_results

# SRM = Simulation_Results_Manager()
# SRM.read_results_from_JSON()
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import numpy as np
#
# # Create figure and axes
# fig, ax = plt.subplots()
#
# # Data for the scatter plot
# x_data = np.random.rand(50)
# y_data = np.random.rand(50)
#
# # Create the initial scatter plot
# scatter = ax.scatter(x_data, y_data)
#
# def update(frame):
#     """Animation function to update the scatter plot"""
#     # Update the data for the scatter plot (e.g., random points for demonstration)
#     x_data = np.random.rand(50)
#     y_data = np.random.rand(50)
#
#     # Update the scatter plot with new data
#     scatter.set_offsets(np.c_[x_data, y_data])
#
#     # Return the artists to be redrawn in this frame (scatter plot in this case)
#     return scatter,
#
# # Create the animation
# animation = FuncAnimation(fig, update, frames=100, interval=50, blit=True)
#
# # Display the animation in PyCharm's interactive plot viewer
# plt.show()

