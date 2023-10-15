import datetime
import json
import random
import time

from Main_Files import Car
import Simulation_manager
import GUI.Animate_Simulation as AS
from Utilities.Getters import get_random_src_dst
from Utilities.Results import save_results_to_JSON, read_results_from_JSON, car_times_bar_chart, \
    print_simulation_results, plot_simulation_overview, get_simulation_times
from Utilities import Getters

START_TIME1 = datetime.datetime(year=2023, month=7, day=2, hour=0, minute=0, second=0)
START_TIME2 = datetime.datetime(year=2023, month=6, day=2, hour=0, minute=0, second=0)
START_TIME3 = datetime.datetime(year=2023, month=6, day=2, hour=0, minute=0, second=0)
START_TIME4 = datetime.datetime(year=2023, month=6, day=2, hour=0, minute=0, second=0)
START_TIME5 = datetime.datetime(year=2023, month=6, day=2, hour=0, minute=0, second=0)

ADD_TO_DAY = [0, 1, 2, 3, 4, 5, 6]  # to cover every day of the week

ADD_TO_HOUR = [i for i in range(0, 22)]  # to cover every hour of the day from 0:00 to 22:00
ADD_TO_MINUTE = [i for i in range(0, 60)]  # to cover every minute of the hour

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
USE_ALREADY_GENERATED_Q_TABLE = False
NUM_EPISODES = 2000

# Animation parameters
ANIMATE_SIMULATION = False
REPEAT = False
SIMULATION_SPEED = 10  # X30 faster than one second interval

PLOT_RESULTS = False

NUM_OF_RUNS = 3
PLACE_NAME = 'TLV'
NUM_OF_CARS = 5

ALGORITHMS = ["q", "sp"]
SP_IND = 1
Q_IND = 0

# nodes from list in place i will be one endpoint of the route
# nodes from list in place 3-i will be the other endpoint of the route
NODES = [Getters.bottom_left_nodes, Getters.bottom_right_nodes, Getters.top_left_nodes, Getters.top_right_nodes]

def checkif_path_is_exist(src,dst,RN):
    try:
        path = RN.get_shortest_path(src, dst)
        return True
    except:
        return False


def choose_random_src_dst():
    src_list = random.randint(0, len(NODES) - 1)
    dst_list = len(NODES) - 1 - src_list
    src = random.choice(NODES[src_list])
    dst = random.choice(NODES[dst_list])
    return src, dst


def create_time_delta(days):
    hour = random.choice(ADD_TO_HOUR)
    minute = random.choice(ADD_TO_MINUTE)
    time_delta = datetime.timedelta(days=days, hours=hour, minutes=minute)
    return time_delta



def generate_cars(existing_settings, algorithm_ind, RN):
    # cars are in the same road network, same day, different starting times, different src and dst
    cars = []
    day = random.choice(ADD_TO_DAY)
    for i in range(NUM_OF_CARS):

        time_delta = create_time_delta(day)
        src, dst = choose_random_src_dst()
        while not checkif_path_is_exist(src,dst,RN):
            src, dst = choose_random_src_dst()
        while (src, dst, time_delta, algorithm_ind) in existing_settings:  # make sure there are no duplicates
            time_delta = create_time_delta(day)
        existing_settings.append((src, dst, time_delta))
        cars.append(Car.Car(i, src, dst, START_TIME1 + time_delta, RN, route_algorithm=ALGORITHMS[algorithm_ind],
                            use_existing_q_table=USE_ALREADY_GENERATED_Q_TABLE))
    return cars

def print_algorithms_success_rate(SM_results):
    total_q = NUM_OF_CARS*NUM_OF_RUNS
    total_sp = NUM_OF_CARS*NUM_OF_RUNS
    q_success = 0
    sp_success = 0
    for i in range(NUM_OF_RUNS):
        for j in range(NUM_OF_CARS):
            if SM_results[i][j][ALGORITHMS[Q_IND]][Getters.Reached_destination]:
                q_success += 1
            if SM_results[i][j][ALGORITHMS[SP_IND]][Getters.Reached_destination]:
                sp_success += 1
    print("q success rate: ", q_success/total_q)
    print("sp success rate: ", sp_success/total_sp)


def change_route_algorithm(cars, algorithm_ind):
    for car in cars:
        car.set_new_routing_algorithm(ALGORITHMS[algorithm_ind])

def get_cars_times(SM):
    times = {} # format: key = simulation index, value = list of times of cars in the simulation and algorithm
    for i, result in enumerate(SM.simulation_results):
        times[i] = []
        for array_index, result_dict in result.items():
            if array_index != Simulation_manager.Simulation_number:
                times[i].append(result_dict[Getters.Time_taken])

def organize_simulation_times(times):
    organized_times = {} # key = simulation index, value = list of times of cars in the simulation and algorithm
    # exery even index is shortest path, every odd index is q learning
    for i in range (0, int(len(times)/NUM_OF_CARS)):
        organized_times[i] = []
        for j in range(0,NUM_OF_CARS):
            organized_times[i].append(times[i*NUM_OF_CARS+j])
    return organized_times

if __name__ == "__main__":
    out_times_data = []  # format: key= run number and algorithm, value = time for full simulation
    SM = Simulation_manager.Simulation_manager(PLACE_NAME, TRAFFIC_LIGHTS, Rain_intensity, TRAFFIC_WHITE_NOISE,
                                               PLOT_RESULTS, START_TIME1)
    RN = SM.road_network
    used_settings = []
    run_time_data = {}  # format: key= run number  value = time for full simulation in seconds and algorithm

    # main loop
    for i in range(NUM_OF_RUNS):
        print("*****run number: ", i,"*****")
        run_time_data[i] = {}
        cur_cars = generate_cars(used_settings, SP_IND, RN)
        start_sp = time.time()
        SM.run_full_simulation(cur_cars, NUMBER_OF_SIMULATIONS, num_episodes=NUM_EPISODES, max_steps_per_episode=100)
        end_sp = time.time()
        run_time_data[i][ALGORITHMS[SP_IND]] = end_sp - start_sp
        change_route_algorithm(cur_cars, Q_IND)
        start_q = time.time()
        cur_learning_time = SM.run_full_simulation(cur_cars, NUMBER_OF_SIMULATIONS, num_episodes=NUM_EPISODES, max_steps_per_episode=100)
        end_q = time.time()
        run_time_data[i][ALGORITHMS[Q_IND]] = end_q - start_q - cur_learning_time
        run_time_data[i]["learning_time"] = cur_learning_time
        # SM.simulation_results = read_results_from_JSON(SM.graph_name)
        # times = get_simulation_times(SM)

    json_name = save_results_to_JSON(SM.graph_name, SM.simulation_results)
    print(organize_simulation_times(get_simulation_times(SM)))
    print(run_time_data)
    json.dump(run_time_data, open("run_time_data.json", 'w')
                , indent=4)
    json.dump(organize_simulation_times(get_simulation_times(SM)), open("times_data.json", 'w'), indent=4)
    # print_algorithms_success_rate(SM.simulation_results)
    pass