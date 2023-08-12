import datetime

from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import osmnx as ox
from matplotlib.animation import FuncAnimation
from shapely.geometry import Point
import geopandas as gpd
import numpy as np

from Utilities.Speeds import color_edges_by_speed


class Animate_Simulation:
    def __init__(self, animation_speed = 1, repeat = True ):
        self.animation = None
        self.animation_speed = self.choose_animation_speed(animation_speed)
        self.repeat = repeat
        self.last_speed_update_time = None

        # animation route variables
        self.edge_colors = []
        self.node_colors = []
        self.origins = []
        self.destinations = []

    def choose_animation_speed(self, animation_speed):
        return 1000/animation_speed
    def print_simulation_results(self, SM):
        """
        simulation_results follow the format:
            all_simulations : [ simulation_1:{simulation_number, car_1_info:{..},car_2_info:{..} }, { {},{} }, { {},{} } ]
        the function prints the results of the simulation in a readable format
        :param SM: Simulation_Manager object

        :return: None
        """
        for result in SM.simulation_results:
            for array_index, result_dict in result.items():
                if array_index != "simulation_number":
                    print("*******************************************")
                    print("Simulation number: ", result['simulation_number'])

                    print(array_index, ": ")
                    for key, value in result_dict.items():
                        if key != "route" and key != "time_taken" and key != "distance_travelled":
                            print(key, ": ", value)
                        elif key == "time_taken":
                            print(key, ": ", int(value / 60), "minutes")
                        elif key == "distance_travelled":
                            print(key, ": ", round(value / 1000, 1), "km")
                        else:
                            print("Route length: ", len(value), "roads")

        return


    def car_times_bar_chart(self, SM, car_number):
        """
        This function plots a bar chart of the times of a specific car in the simulation.

        :param SM: Simulation_Manager object
        :param car_number: The car number for which the chart will be plotted.
        """
        times = []
        colors = []

        for result in SM.simulation_results:
            car_key = car_number
            times.append(result[car_key]['time_taken'])
            if result[car_key]['reached_destination']:
                colors.append('green')
            else:
                colors.append('red')
        # time_seconds = [td.total_seconds() for td in times]
        plt.bar((range(1, len(times) + 1)), times, color=colors)

        # Add labels and title
        plt.xlabel('Simulation Number')
        plt.ylabel('Time taken [seconds] by Car {}'.format(car_number))
        plt.title('Bar Chart: Times of Car {} in Simulation'.format(car_number))
        legend_labels = ['Reached Destination', 'Not Reached Destination']
        legend_colors = ['green', 'red']
        legend_patches = [mpatches.Patch(color=color, label=label) for color, label in
                          zip(legend_colors, legend_labels)]

        plt.legend(handles=legend_patches, title='Legend', loc='upper right')

        plt.show()


    def plotting_custom_route(self, SM, custom_routes: list, cars: list):
        """
        this is the way for a car that finished its route to plot it on the map at the end
        saves the function here for future use.
        the function plots the custom route on the map and animates the car moving on the route

        :param SM: Simulation_Manager object
        :param custom_routes: list of routes (lists of node IDs) of selected cars
        :param cars: list of the selected cars objects
        :return: None
        """
        # Define the custom route as a list of node IDs
        RN = SM.road_network
        graph = SM.road_network.graph
        scatter_list = []
        cars_ids = [car.id for car in cars]
        start_time = SM.simulation_datetime_start
        blocked_roads = SM.road_network.blocked_roads_dict

        # color the edges by speed
        self.edge_colors = color_edges_by_speed(SM, start_time, blocked_roads)

        # color the nodes by traffic lights
        self.node_colors = [
            plt.cm.RdYlGn(node.traffic_lights) if node.traffic_lights else
            'lightgrey'
            for node in RN.nodes_array
        ]
        # Plot the graph
        fig, ax = ox.plot_graph(graph, figsize=(10, 10), show=False, close=False, edge_color=self.edge_colors,
                                node_color=self.node_colors, bgcolor='white', node_size=5)
        colors = ['red', 'blue', 'purple']  # Add more colors as needed

        for j, route in enumerate(custom_routes):
            origin_x, origin_y = RN.get_xy_from_node_id(route[0])
            if cars[j].route_algorithm == "q":
                color = colors[2]
            elif cars[j].route_algorithm == "sp":
                color = colors[1]
            else:
                color=colors[0]
            label = f'Car {j + 1} ({cars[j].route_algorithm})'  # Create a label for the scatter plot

            scatter_list.append(ax.scatter(origin_x,  # x coordiante of the first node of the j route
                                           origin_y,  # y coordiante of the first node of the j route
                                           label=label,
                                           alpha=.75,
                                           color=color))
            print("scatter list: ", scatter_list)
            geometry_data = [(origin_y, origin_x)]
            gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in geometry_data], crs='epsg:4326')
            self.origins.append(gdf)

            dest_x, dest_y = RN.get_xy_from_node_id(route[-1])
            geometry_data = [(dest_y, dest_x)]
            gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in geometry_data], crs='epsg:4326')
            self.destinations.append(gdf)

        # plot origins and destinations
        for i in range(len(self.origins)):
            if i==0:
                self.origins[i].plot(ax=ax, color='black', label=f'Origin')
                self.destinations[i].plot(ax=ax, color='yellow', label=f'Destination')
            self.origins[i].plot(ax=ax, color='black')
            self.destinations[i].plot(ax=ax, color='yellow')
        # Add a legend with labels from scatter plots
        plt.legend(frameon=False)
        self.handles, self.labels = ax.get_legend_handles_labels()

        # ax.legend(
        #     handles=handles + scatter_list, labels=labels + [scatter.get_label() for scatter in scatter_list],
        #     frameon=False
        #     )

        # animate the route
        self.animate_route(SM, ax, fig, scatter_list, cars_ids)
        return


    def animate_route(self, SM, ax, fig, scatter_list, chosen_cars_ids):
        """
        This function animates the route of the car on the map.
        :param SM:
        :param ax:
        :param fig:
        :param scatter_list:
        :param chosen_cars_ids:
        :param new_routes:
        :return:
        """
        num_updates = len(SM.simulation_update_times)  # Get the number of simulation update times
        temp_dict = {id:j for j,id in enumerate(chosen_cars_ids)}
        self.last_speed_update_time = SM.simulation_update_times[0]

        # Create a flag to control animation pause/resume
        self.is_paused = False

        def on_key(event):
            if event.key == ' ':
                self.is_paused = not self.is_paused

        # Connect the key press event to the on_key function
        fig.canvas.mpl_connect('key_press_event', on_key)

        def animate(i):
            if self.is_paused:
                return  # Pause the animation if is_paused is True
            update_idx = i
            current_time = SM.simulation_update_times[update_idx]
            delta_time = (current_time - self.last_speed_update_time).total_seconds()
            for j, updates in enumerate(SM.car_manager.updated_dictionary[current_time]):
                try:
                    blocked_roads = SM.road_network.blocked_roads_dict

                    if delta_time > 600 or delta_time < 0:
                        self.last_speed_update_time = current_time
                        current_time = current_time.replace(second=0)
                        self.edge_colors = color_edges_by_speed(SM, current_time, blocked_roads)
                        # handles, labels = ax.get_legend_handles_labels()

                        ax.clear()
                        ox.plot_graph(SM.road_network.graph, figsize=(10, 10), show=False, close=False, edge_color=self.edge_colors,
                                      node_color=self.node_colors, bgcolor='white', node_size=5,ax=ax)

                        # plot origins and destinations
                        for i in range(len(self.origins)):
                            if i == 0:
                                self.origins[i].plot(ax=ax, color='black')
                                self.destinations[i].plot(ax=ax, color='yellow')
                            self.origins[i].plot(ax=ax, color='black')
                            self.destinations[i].plot(ax=ax, color='yellow')
                        # plt.legend(frameon=False)
                        ax.legend(
                            handles=self.handles + scatter_list, labels=self.labels ,
                            frameon=False
                            )
                        for sc in scatter_list:
                            ax.add_artist(sc)

                    x_j, y_j = updates[1][0], updates[1][1]
                    scatter_list[temp_dict[updates[0]]].set_offsets(np.c_[x_j, y_j])

                except:
                    print("Error in animate function")
                    continue

            # Clear previous text annotation
            if ax.texts:
                for text in ax.texts:
                    text.remove()

            # Define vertical positions for text annotations
            text_vertical_positions = [0.95, 0.9]

            # Add text annotation for simulation date
            date_text = ax.text(0.95, text_vertical_positions[0], f'Simulation Date: {current_time.strftime("%A")}',
                                transform=ax.transAxes, color='black', fontsize=12, fontweight='bold',
                                horizontalalignment='right')

            # Add text annotation for simulation time
            time_text = ax.text(0.95, text_vertical_positions[0], f'Simulation Time: {current_time.strftime("%H:%M")}',
                                transform=ax.transAxes, color='black', fontsize=12, fontweight='bold',
                                horizontalalignment='right')

            # Make sure the text annotations do not overlap
            date_text.set_y(text_vertical_positions[0])
            time_text.set_y(text_vertical_positions[1])

        self.animation = FuncAnimation(fig, animate, frames = num_updates, interval = self.animation_speed, repeat = self.repeat)
        plt.show()
