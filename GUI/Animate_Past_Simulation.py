# external imports
import json
from datetime import timedelta, datetime
from matplotlib import pyplot as plt
import osmnx as ox
from matplotlib.animation import FuncAnimation
from shapely.geometry import Point
import geopandas as gpd
import numpy as np

# internal imports
from Main_Files.Road_Network import Road_Network
import Utilities.Getters  as Getters
from Utilities.Speeds import color_edges_by_speed_json


class Animate_Past_Simulation:
    def __init__(self, animation_speed=30, repeat=True):
        self.animation = None
        self.animation_speed = 1000 / animation_speed
        self.repeat = repeat
        self.last_speed_update_time = None
        self.RN = None
        self.handles, self.labels = None, None
        self.is_paused = False
        self.running = True

        # animation route variables
        self.simulation_data = []
        self.sources = []
        self.destinations = []
        self.update_times = []
        self.edge_colors = []
        self.simulation_update_times = {}
        self.day_of_week = None

    def plot_simulation(self, simulation_json_file):
        ############################################################
        # helper functions
        def create_geo_dataframe(node_id, container):
            x, y = self.RN.get_xy_from_node_id(self.simulation_data[i][node_id])
            geometry_data = [(y, x)]
            gdf = gpd.GeoDataFrame(geometry = [Point(lon, lat) for lat, lon in geometry_data], crs = 'epsg:4326')
            container.append(gdf)
            return x, y
        ############################################################
        scatter_list = []
        substring_to_remove = "simulation_results_"

        # get the city name from the json name and create a road network object of the city
        self.graph_name = simulation_json_file.replace(substring_to_remove, "")
        self.RN = Road_Network(self.graph_name)
        graph = self.RN.graph

        # Load the past result
        with open(f'../Results/{simulation_json_file}.json') as json_file:
            past_result = json.load(json_file)

        # get all the relevant data from the json file (source, destination, blocked roads, route, starting time, etc.)
        simulation_data = past_result[0]

        # save the data in a list
        for key in simulation_data.keys():
            if key != Getters.Simulation_number: # Ignore the simulation number
                self.simulation_data.append(simulation_data[key])

        # Calculate the simulation update times
        self.simulation_update_times = self.calculate_simulation_update_times()
        self.day_of_week = list(self.simulation_update_times.keys())[0].strftime("%A")

        # Convert the day name to an integer
        day_of_week_int = Getters.day_mapping[self.day_of_week]
        self.blocked_roads = {}
        temp_blocked_roads = self.simulation_data[0][Getters.Blocked_roads]
        for sub_array in temp_blocked_roads:
            key = sub_array[0]  # First place (integer) as the key
            value = sub_array[1]  # Second place (datetime) as the value
            self.blocked_roads[key] = value
        update_index = list(self.simulation_update_times.keys())
        self.last_speed_update_time = update_index[0]
        self.edge_colors = color_edges_by_speed_json(self.graph_name,day_of_week_int, self.RN, update_index[0], self.blocked_roads)
        self.node_colors = [
            plt.cm.RdYlGn(node.traffic_lights) if node.traffic_lights else
            '#EAEAEA'
            for node in self.RN.nodes_array
        ]

        # Plot the graph
        fig, ax = ox.plot_graph(graph, figsize = (10, 10), show = False, close = False,
                                edge_color = self.edge_colors,node_color = self.node_colors,  bgcolor = 'white',
                                node_size = 5)
        color_mapping = {Getters.Q: 'red', Getters.SP: 'blue'}

        for i in range(len(self.simulation_data)):

            origin_x, origin_y = create_geo_dataframe(Getters.Source, self.sources)
            create_geo_dataframe(Getters.Destination, self.destinations)

            route_algorithm_name = self.simulation_data[i][Getters.Routing_algorithm]
            color = color_mapping.get(route_algorithm_name, 'purple')
            label = f'Car {i} ({route_algorithm_name})'  # Create a label for the scatter plot
            scatter_list.append(ax.scatter(origin_x,  # x coordiante of the first node of the j route
                                           origin_y,  # y coordiante of the first node of the j route
                                           label = label, alpha = .75, color = color))
        # plot origins and destinations
        for i in range(len(self.sources)):
            self.sources[i].plot(ax = ax, color = 'black', label = 'car ' + str(i+1) + ' origin')
            self.destinations[i].plot(ax = ax, color = 'yellow', label = 'car ' + str(i+1) + ' destination')  # Add a legend with labels from scatter plots

        # Add a legend with labels from scatter plots
        plt.legend(frameon = False)
        self.handles, self.labels = ax.get_legend_handles_labels()

        # animate the route
        self.animate_route(ax, fig, scatter_list)
        return

    def animate_route(self, ax, fig, scatter_list):
        # animation function.  This is called sequentially
        ####################################################
        # helper functions
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

        ####################################################

        print("animate route")
        num_updates = len(self.simulation_update_times)
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
            update_index = list(self.simulation_update_times.keys())
            current_time = update_index[i]
            delta_time = (current_time - self.last_speed_update_time).total_seconds()
            for j, updates in enumerate(self.simulation_update_times[current_time]):
                try:
                    if delta_time > 600 or delta_time < 0:
                        self.edge_colors = []
                        self.last_speed_update_time = current_time
                        current_time = current_time.replace(second=0)
                        self.day_of_week = current_time.strftime("%A")
                        day_of_week_int = Getters.day_mapping[self.day_of_week]
                        self.edge_colors = color_edges_by_speed_json(self.graph_name, day_of_week_int, self.RN, current_time, self.blocked_roads)
                        ax.clear()
                        ox.plot_graph(self.RN.graph, figsize = (10, 10), show = False, close = False,
                                                edge_color = self.edge_colors, node_color = self.node_colors,
                                                bgcolor = 'white', node_size = 5, ax=ax)

                        # plot origins and destinations
                        for i in range(len(self.sources)):
                            self.sources[i].plot(ax = ax, color = 'black')
                            self.destinations[i].plot(ax = ax, color = 'yellow')
                        ax.legend(handles = self.handles + scatter_list, labels = self.labels, frameon = False)
                        for sc in scatter_list:
                            ax.add_artist(sc)
                    x_j, y_j = updates[1][0], updates[1][1]
                    scatter_list[updates[0]-1].set_offsets(np.c_[x_j, y_j])

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
            date_text = ax.text(0.95, text_vertical_positions[0],
                                f'Simulation Date: {current_time.strftime("%A")}', transform = ax.transAxes,
                                color = 'black', fontsize = 12, fontweight = 'bold',
                                horizontalalignment = 'right')

            # Add text annotation for simulation time
            time_text = ax.text(0.95, text_vertical_positions[0],
                                f'Simulation Time: {current_time.strftime("%H:%M")}', transform = ax.transAxes,
                                color = 'black', fontsize = 12, fontweight = 'bold',
                                horizontalalignment = 'right')

            # Make sure the text annotations do not overlap
            date_text.set_y(text_vertical_positions[0])
            time_text.set_y(text_vertical_positions[1])

        self.animation = FuncAnimation(fig, animate, frames = num_updates, interval = self.animation_speed,
                                       repeat = self.repeat, repeat_delay = 0)
        plt.show(block = True)
        return

    def calculate_simulation_update_times(self):
        """
        This function calculates the update times of the simulation

        :return: sorted dictionary of the update times based on the simulation data,
        the key is the time and the value is a list of tuples of the form (car_id, (x,y), node_id)
        the first key is the earliest time and the last key is the latest time

        """
        car_update_times = {}

        for i, car in enumerate(self.simulation_data):
            # the parameter i is the car id
            start_time = car[Getters.Start_time]
            date_format = "%Y-%m-%d %H:%M:%S"

            # Convert the string to a datetime object
            current_time = datetime.strptime(start_time, date_format)
            update_list = []
            node_id = car[Getters.Route][0]
            x, y = self.RN.get_xy_from_node_id(node_id)
            update_list.append((i + 1, (x, y), node_id))
            if current_time in car_update_times and car_update_times[current_time]:
                car_update_times[current_time].append((i + 1, (x, y), node_id))
            else:
                car_update_times[current_time] = update_list

            for j, road in enumerate(car[Getters.Roads_used]):
                # print(road)
                update_list=[]
                time_interval = road[list(road.keys())[0]]
                current_time += timedelta(seconds = time_interval)
                node_id = car[Getters.Route][j+1]
                x,y = self.RN.get_xy_from_node_id(node_id)
                update_list.append((i+1,(x,y),node_id))
                if current_time in car_update_times and car_update_times[current_time]:
                    car_update_times[current_time].append((i + 1, (x, y), node_id))
                else:
                    car_update_times[current_time] = update_list
        sorted_dict = {k: v for k, v in sorted(car_update_times.items(), key = lambda item: item[0])}

        return sorted_dict
