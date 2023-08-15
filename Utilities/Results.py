import json
import time

from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import osmnx as ox
from Main_Files.Road_Network import Road_Network
from Utilities.Getters import Time_taken, Reached_destination, Simulation_number, Route, Distance_travelled, \
    node_route_to_osm_route, Source, Destination


def save_results_to_JSON(graph_name, results):
    """
    Save simulation results to a JSON file.

    Args:
    graph_name (str): Name of the graph.
    results (dict): Dictionary containing simulation results.

    Returns:
    None
    """
    # self.simulation_results.append(results)
    json_name = f'simulation_results_{graph_name}'
    with open(f'../Results/{json_name}.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)
    return json_name


def read_results_from_JSON(graph_name):
    """
    Read simulation results from a JSON file.

    Returns:
    dict: Dictionary containing the loaded simulation results.
    """
    with open(f'../Results/simulation_results_{graph_name}.json', 'r') as infile:
        new_simulation_results = json.load(infile)
    return new_simulation_results

def car_times_bar_chart(SM, car_number):
        """
        This function plots a bar chart of the times of a specific car in the simulation.

        :param SM: Simulation_Manager object
        :param car_number: The car number for which the chart will be plotted.
        """
        times = []
        colors = []

        for result in SM.simulation_results:
            car_key = f'{car_number}'
            times.append(result[car_key][Time_taken])
            if result[car_key][Reached_destination]:
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
        return

def print_simulation_results(SM):
    """
    simulation_results follow the format:
    all_simulations : [ simulation_1:{simulation_number, car_1_info:{..},car_2_info:{..} }, { {},{} }, { {},{} } ]
    the function prints the results of the simulation in a readable format

    :param SM: Simulation_Manager object

    :return: None
    """
    for result in SM.simulation_results:
        for array_index, result_dict in result.items():
            if array_index != Simulation_number:
                print("*******************************************")
                print("Simulation number: ", result[Simulation_number])

                print(array_index, ": ")
                for key, value in result_dict.items():
                    if key != Route and key != Time_taken and key != Distance_travelled:
                        print(key, ": ", value)
                    elif key == Time_taken:
                        print(key, ": ", int(value / 60), "minutes")
                    elif key == Distance_travelled:
                        print(key, ": ", round(value / 1000, 1), "km")
                    else:
                        print("Route length: ", len(value), "roads")

    return

def plot_past_result(past_result_json_name):
    """
    This function plots the past result of the simulation.

    :param past_result_json:

    :return: None
    """
    global ax, fig, origin_x, dest_x, origin_y, dest_y
    substring_to_remove = "simulation_results_"
    graph_name = past_result_json_name.replace(substring_to_remove, "")
    RN = Road_Network(graph_name)
    # Load the past result
    with open(f'../Results/{past_result_json_name}.json') as json_file:
        past_result = json.load(json_file)
    origins = []
    destinations = []
    # Plot the past result where simulation number = 0
    route_labels = []  # List to store labels for each route
    first_simulation = past_result[0]
    routes = []
    for key in first_simulation.keys():
        if key != Simulation_number:
            car_results = first_simulation[key]
            car_source = car_results[Source]
            car_destination = car_results[Destination]
            origin_x, origin_y = RN.get_xy_from_node_id(car_source)
            origins.append((origin_x, origin_y))
            dest_x, dest_y = RN.get_xy_from_node_id(car_destination)
            destinations.append((dest_x, dest_y))
            car_route = car_results[Route]
            routes.append(car_route)
            route_labels.append(f"Route {key}")  # Add a label for the current route

    if len(routes) == 1:
        route = node_route_to_osm_route(RN, routes[0])
        fig, ax = ox.plot_graph_route(
            RN.graph, route, route_color='red', route_linewidth=2, node_size=0, bgcolor='white', show=False,
            close=False)
    else:
        for i in range(len(routes)):
            routes[i] = node_route_to_osm_route(RN, routes[i])
        fig, ax = ox.plot_graph_routes(RN.graph, routes, route_color='red', route_linewidth=2, node_size=0, bgcolor='white',show=False,
            close=False)

    plt.title('Past Result of Simulation')
    for i in range(len(origins)):
        orig_x, orig_y = origins[i]
        dest_x, dest_y = destinations[i]
        ax.scatter(orig_x, orig_y, color='black', s=50, label='Start')
        ax.scatter(dest_x, dest_y, color='yellow', s=50, label='End')
    ax.legend()

    plt.show(block=True)
    # plt.pause(2)
    # plt.close()
    return

# plot q learning results
def car_times_bar_chart_Q_agent(src, dst, all_training_paths_nodes, all_training_times, ax=None):

    if ax is None:
        ax = plt.gca()
    colors = []

    for path in all_training_paths_nodes:
        if path[-1] == dst:
            colors.append('green')
        else:
            colors.append('red')
    # time_seconds = [td.total_seconds() for td in times]
    ax.bar((range(1, len(all_training_times) + 1)), all_training_times, color=colors)

    # Add labels and title
    ax.set_xlabel('Simulation Number')
    ax.set_ylabel('Time taken [seconds] by Q Agent')
    ax.set_title('Bar Chart: Times of Q Agent in Simulation, Source: {}, Destination: {}'.format(src, dst))
    legend_labels = ['Reached Destination', 'Not Reached Destination']
    legend_colors = ['green', 'red']
    legend_patches = [mpatches.Patch(color=color, label=label) for color, label in
                      zip(legend_colors, legend_labels)]

    ax.legend(handles=legend_patches, title='Legend', loc='upper right')

def plot_rewards(src, dst, var:list, ax=None):
    """
    Plot the mean rewards over training episodes.

    Args:
        var (list): List of mean rewards.

    Returns:
        None
    """
    if ax is None:
        ax = plt.gca()

    ax.plot(range(1, len(var) + 1), var)
    ax.set_xlabel('Interval (Every 100 Episodes)')
    ax.set_ylabel('Mean Episode Reward')
    ax.set_title('Mean Rewards over Training, Source: {}, Destination: {}'.format(src, dst))

def plot_results(src, dst, all_training_paths_nodes, all_training_times, mean_rewards):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))  # Create a 2-row, 1-column subplot layout

    car_times_bar_chart_Q_agent(src, dst, all_training_paths_nodes, all_training_times, ax1)
    plot_rewards(src, dst, mean_rewards, ax2)

    plt.tight_layout()  # Adjust layout for better spacing
    plt.show(block=True)
    # plt.pause(5)
    # plt.close()
    return
