import json

import datetime
from Main_Files import Car
from Main_Files import Simulation_manager
import GUI.Animate_Simulation as AS
from Utilities.Getters import get_random_src_dst
from Utilities.Results import save_results_to_JSON, read_results_from_JSON, car_times_bar_chart, \
    print_simulation_results, plot_simulation_overview, get_simulation_times

# initilazires
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

# Q-Learning parameters
USE_ALREADY_GENERATED_Q_TABLE = True
NUM_EPISODES = 2000

# Animation parameters
ANIMATE_SIMULATION = True
REPEAT = True
SIMULATION_SPEED = 5  # X30 faster than one second interval

PLOT_RESULTS = True

# Initialize Simulation Manager
PLACE_NAME = 'TLV'
SM = Simulation_manager.Simulation_manager(PLACE_NAME, 7 * DAY, TRAFFIC_LIGHTS, Rain_intensity, TRAFFIC_WHITE_NOISE,
                                           PLOT_RESULTS, START_TIME1)
graph_name = "TLV"
json_name = f'simulation_results_{graph_name}'
plot_simulation_overview(json_name, SM)