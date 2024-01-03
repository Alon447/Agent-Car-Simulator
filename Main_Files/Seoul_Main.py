import datetime
import os
import networkx as nx
from Main_Files import Car
import Simulation_manager
import osmnx as ox
import matplotlib.pyplot as plt
import GUI.Animate_Simulation as AS
from Utilities.Getters import get_random_src_dst
from Utilities.Results import save_results_to_JSON, read_results_from_JSON, car_times_bar_chart, \
    print_simulation_results, plot_simulation_overview, get_simulation_times

START_TIME1 = datetime.datetime(year=2023, month=10, day=4, hour=8, minute=0, second=0)
START_TIME2 = datetime.datetime(year=2023, month=10, day=4, hour=14, minute=0, second=0)

# Constants for time intervals
WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60

# Simulation parameters
NUMBER_OF_SIMULATIONS = 1
TRAFFIC_LIGHTS = False
TRAFFIC_WHITE_NOISE = False
Rain_intensity = 0  # 0-3 (0 = no rain, 1 = light rain, 2 = moderate rain, 3 = heavy rain)
PLOT_RESULTS = True

# Q-Learning parameters
USE_ALREADY_GENERATED_Q_TABLE = False
NUM_EPISODES = 2000

cur = os.getcwd()
parent = os.path.dirname(cur)
data = os.path.join(parent, "Graphs")
path = data + "\\" + "real_seoul_graph" + ".graphml"
graph = ox.load_graphml(path)

# Access and print node attributes
# for node, data in graph.nodes(data=True):
#     print(f"Node {node} attributes:")
#     print(data)  # Print all attributes for each node

# # Access and print edge attributes
# for u, v, data in graph.edges(data=True):
#     print(f"Edge ({u}, {v}) attributes:")
#     print(data.get('road_id'))  # Print all attributes for each edge

SM = Simulation_manager.Simulation_manager("real_seoul_graph", TRAFFIC_LIGHTS, Rain_intensity, TRAFFIC_WHITE_NOISE,
                                           PLOT_RESULTS, START_TIME1, start_time = START_TIME1)
# plt.figure(figsize=(8, 6))
# pos = nx.spring_layout(graph)  # or use other layout algorithms like nx.circular_layout, nx.random_layout, etc.
# nx.draw(graph, pos, with_labels=True, node_size=50, node_color='skyblue', edge_color='gray', font_size=8)
# plt.title('Graph Visualization')
# plt.show()
CM = SM.car_manager
RN = SM.road_network

cars = []

src1, dst1 = 719, 665
src2, dst2 = 200, 300
src3, dst3 = 300, 400
cars.append(
    Car.Car(1, src3, dst3, START_TIME1, RN, route_algorithm="q", use_existing_q_table=USE_ALREADY_GENERATED_Q_TABLE))
cars.append(
    Car.Car(2, src3, dst3, START_TIME1, RN, route_algorithm="sp", use_existing_q_table=USE_ALREADY_GENERATED_Q_TABLE))
# cars.append(
    # Car.Car(3, src3, dst3, START_TIME1, RN, route_algorithm="random", use_existing_q_table=USE_ALREADY_GENERATED_Q_TABLE))
SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS, num_episodes=3000, max_steps_per_episode=100)
routes = SM.get_simulation_routes(cars, 0)