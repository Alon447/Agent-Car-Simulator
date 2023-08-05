from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import osmnx as ox
from matplotlib.animation import FuncAnimation
from shapely.geometry import Point
import geopandas as gpd
import numpy as np


def print_simulation_results(SM):
    """
    self.simulation_results =  all_simulations : [ simulation_1:{simulation_number, car_1_info:{..},car_2_info:{..} }, { {},{} }, { {},{} } ]
    list - every simulation
    outer dict - single simulation
    inner dict - number of simulation and cars
    :return:
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


def car_times_bar_chart(SM, car_number):
    """
    This function plots a bar chart of the times of a specific car in the simulation.

    Parameters:
    - car_number: The car number for which the chart will be plotted.
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


def plotting_custom_route(SM, custom_routes: list, cars: list):
    """
    this is the way for a car that finished its route to plot it on the map at the end
    saves the function here for future use
    """
    # Define the custom route as a list of node IDs
    RN = SM.road_network
    graph = SM.road_network.graph
    new_routes = []
    rc = []
    scatter_list = []
    orig = []
    dest = []
    cars_ids = [car.id for car in cars]

    edge_colors = [
        'white' if road.is_blocked else
        'red' if road.current_speed < 25 else
        'orange' if road.current_speed < 37 else
        'green'
        for road in SM.road_network.roads_array
    ]

    node_colors = [
        plt.cm.RdYlGn(node.traffic_lights) if node.traffic_lights else
        'lightgrey'
        for node in SM.road_network.nodes_array
    ]
    # Plot the graph
    fig, ax = ox.plot_graph(graph, figsize=(10, 10), show=False, close=False, edge_color=edge_colors,
                            node_color=node_colors, bgcolor='white', node_size=5)

    for j, route in enumerate(custom_routes):
        new_routes.append(SM.transform_node_id_route_to_osm_id_route(route))

        x, y = RN.get_xy_from_node_id(route[0])
        scatter_list.append(ax.scatter(x,  # x coordiante of the first node of the j route
                                       y,  # y coordiante of the first node of the j route
                                       label=f'Car {j}',
                                       alpha=.75))
        origin_x, origin_y = RN.get_xy_from_node_id(route[0])
        geometry_data = [(origin_y, origin_x)]
        gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in geometry_data], crs='epsg:4326')
        orig.append(gdf)

        dest_x, dest_y = RN.get_xy_from_node_id(route[-1])
        geometry_data = [(dest_y, dest_x)]
        gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in geometry_data], crs='epsg:4326')
        dest.append(gdf)

    # Plot the graph
    for i in range(len(new_routes)):
        if i==0:
            orig[i].plot(ax=ax, color='black', label=f'Origin')
            dest[i].plot(ax=ax, color='yellow', label=f'Destination')
        orig[i].plot(ax=ax, color='black')
        dest[i].plot(ax=ax, color='yellow')
    plt.legend(frameon=False)

    # pick route colors

    rc.append("r")
    rc.append("b")
    # Plot the custom route
    # ox.plot_graph_routes(graph, new_routes, route_colors=rc, route_linewidth=6,  node_size=0, bgcolor='k',ax=ax)

    # Show the plot
    # plt.show()
    # return
    animate_route(SM,ax, fig, scatter_list, cars_ids)
    return


def animate_route(SM, ax, fig, scatter_list, chosen_cars_ids):
    num_updates = len(SM.simulation_update_times)  # Get the number of simulation update times
    temp_dict = {id:j for j,id in enumerate(chosen_cars_ids)}

    def animate(i):
        update_idx = i
        edge_colors = [
            'white' if road.is_blocked else
            'red' if road.current_speed < 25 else
            'orange' if road.current_speed < 37 else
            'green'
            for road in SM.road_network.roads_array
        ]
        # ox.plot_graph(SM.road_network.graph, figsize=(10, 10), show=False, close=False, edge_color="blue",
        #               node_color='lightgrey', bgcolor='white',ax=ax)
        current_time = SM.simulation_update_times[update_idx]
        for j, updates in enumerate(SM.car_manager.updated_dictionary[current_time]):
            try:
                x_j, y_j = updates[1][0], updates[1][1]
                scatter_list[temp_dict[updates[0]]].set_offsets(np.c_[x_j, y_j])
            except:
                continue

        # Clear previous text annotation
        if ax.texts:
            for text in ax.texts:
                text.remove()

        # Define vertical positions for text annotations
        text_vertical_positions = [0.95, 0.9]

        # Add text annotation for simulation date
        date_text = ax.text(0.95, text_vertical_positions[0], f'Simulation Date: {current_time.strftime("%d/%m/%Y")}',
                            transform=ax.transAxes, color='black', fontsize=12, fontweight='bold',
                            horizontalalignment='right')

        # Add text annotation for simulation time
        time_text = ax.text(0.95, text_vertical_positions[0], f'Simulation Time: {current_time.strftime("%H:%M:%S")}',
                            transform=ax.transAxes, color='black', fontsize=12, fontweight='bold',
                            horizontalalignment='right')

        # Make sure the text annotations do not overlap
        date_text.set_y(text_vertical_positions[0])
        time_text.set_y(text_vertical_positions[1])

    animation = FuncAnimation(fig, animate, frames=num_updates, interval=200, repeat=True)
    plt.show()
