from matplotlib import pyplot as plt
import osmnx as ox
from matplotlib.animation import FuncAnimation
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
from Utilities.Speeds import color_edges_by_speed


class Animate_Simulation:
    def __init__(self, animation_speed=1, repeat=True):
        self.animation = None
        self.animation_speed = 1000 / animation_speed
        self.repeat = repeat
        self.last_speed_update_time = None

        # animation route variables
        self.edge_colors = []
        self.node_colors = []
        self.origins = []
        self.destinations = []

    def plot_simulation(self, SM, custom_routes: list, cars: list):
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
        blocked_roads = SM.road_network.blocked_roads_dict

        # color the edges by speed
        self.edge_colors = color_edges_by_speed(RN, SM.simulation_update_times[0], blocked_roads)
        self.origins = []
        self.destinations = []
        # color the nodes by traffic lights
        self.node_colors = [
            plt.cm.RdYlGn(node.traffic_lights) if node.traffic_lights else
            '#EAEAEA'
            for node in RN.nodes_array
        ]
        # Plot the graph
        fig, ax = ox.plot_graph(graph, figsize=(10, 10), show=False, close=False, edge_color=self.edge_colors,
                                node_color=self.node_colors, bgcolor='white', node_size=5)
        # colors = ['purple', 'blue', 'red']  # Add more colors as needed

        for j, route in enumerate(custom_routes):
            origin_x, origin_y = RN.get_xy_from_node_id(route[0])

            color_mapping = {"q": 'red', "sp": 'blue'}
            color = color_mapping.get(cars[j].route_algorithm_name, 'purple')

            label = f'Car {cars_ids[j]} ({cars[j].route_algorithm_name})'  # Create a label for the scatter plot

            scatter_list.append(ax.scatter(origin_x,  # x coordiante of the first node of the j route
                                           origin_y,  # y coordiante of the first node of the j route
                                           label=label,
                                           alpha=.75,
                                           color=color))
            # print("scatter list: ", scatter_list)
            geometry_data = [(origin_y, origin_x)]
            gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in geometry_data], crs='epsg:4326')
            self.origins.append(gdf)

            dest_x, dest_y = cars[j].get_xy_destination()
            # dest_x, dest_y = RN.get_xy_from_node_id(route[-1])
            geometry_data = [(dest_y, dest_x)]
            gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in geometry_data], crs='epsg:4326')
            self.destinations.append(gdf)

        # plot origins and destinations
        for i in range(len(self.origins)):
            self.origins[i].plot(ax=ax, color='black', label='car ' + str(cars_ids[i]) + ' origin')
            self.destinations[i].plot(ax=ax, color='yellow', label='car ' + str(cars_ids[i]) + ' destination')
        # Add a legend with labels from scatter plots
        plt.legend(frameon=False)
        self.handles, self.labels = ax.get_legend_handles_labels()

        # animate the route
        self.animate_route(SM, ax, fig, scatter_list, cars_ids)
        return

    def animate_route(self, SM, ax, fig, scatter_list, chosen_cars_ids):
        """
        This function animates the route of the car on the map.

        :param SM: Simulation_Manager object
        :param ax:
        :param fig:
        :param scatter_list:
        :param chosen_cars_ids:
        :return:
        """

        def on_repeat():
            if self.repeat:
                self.animation.event_source.stop()
                self.animation = FuncAnimation(fig, animate, frames=num_updates + 1, interval=self.animation_speed,
                                               repeat=False, repeat_delay=100)
            else:
                self.animation.event_source.stop()

        def on_key(event):
            if event.key == ' ':
                self.is_paused = not self.is_paused
                if self.is_paused and self.running:
                    self.animation.pause()  # Pause the animation if is_paused is True
                    self.running = False
                elif not self.is_paused and not self.running:
                    self.running = True
                    self.animation.resume()  # Resume the animation if is_paused is False
            elif event.key == 'escape':
                self.animation.pause()
                self.running = False
                self.animation = None
                plt.close()

                # plt.close()
                return

        def on_close(event):
            if self.animation is not None:
                self.animation.pause()
            self.running = False
            self.animation = None
            plt.close()
            return

        num_updates = len(SM.simulation_update_times)
        # Get the number of simulation update times
        temp_dict = {id: j for j, id in enumerate(chosen_cars_ids)}

        self.last_speed_update_time = SM.simulation_update_times[0]
        # Create a flag to control animation pause/resume
        self.is_paused = False
        self.running = True

        # Connect the key press event to the on_key function
        fig.canvas.mpl_connect('key_press_event', on_key)
        fig.canvas.mpl_connect('close_event', on_close)

        def animate(i):
            if i >= num_updates:
                on_repeat()
                self.animation.event_source.stop()  # Stop the animation when it's complete
                return
            update_idx = i
            current_time = SM.simulation_update_times[update_idx]
            delta_time = (current_time - self.last_speed_update_time).total_seconds()
            for j, updates in enumerate(SM.car_manager.simulation_update_times[current_time]):
                try:
                    blocked_roads = SM.road_network.blocked_roads_dict

                    if delta_time > 600 or delta_time < 0:
                        self.last_speed_update_time = current_time
                        current_time = current_time.replace(second=0)
                        self.edge_colors = color_edges_by_speed(SM.road_network, current_time, blocked_roads)
                        # handles, labels = ax.get_legend_handles_labels()

                        ax.clear()
                        ox.plot_graph(SM.road_network.graph, figsize=(10, 10), show=False, close=False,
                                      edge_color=self.edge_colors,
                                      node_color=self.node_colors, bgcolor='white', node_size=5, ax=ax)

                        # plot origins and destinations
                        for i in range(len(self.origins)):
                            self.origins[i].plot(ax=ax, color='black')
                            self.destinations[i].plot(ax=ax, color='yellow')
                        # plt.legend(frameon=False)
                        ax.legend(
                            handles=self.handles + scatter_list, labels=self.labels,
                            frameon=False
                        )
                        for sc in scatter_list:
                            ax.add_artist(sc)

                    x_j, y_j = updates[1][0], updates[1][1]
                    scatter_list[temp_dict[updates[0]]].set_offsets(np.c_[x_j, y_j])

                except Exception as e:
                    print(f"Error in animate function {e}")
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

        self.animation = FuncAnimation(fig, animate, frames=num_updates, interval=self.animation_speed,
                                       repeat=self.repeat, repeat_delay=100)
        plt.show(block=True)
        return
