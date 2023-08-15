import datetime

from Main_Files import Car
import Simulation_manager
import GUI.Animate_Simulation as AS
from Utilities.Getters import get_random_src_dst
from Utilities.Results import save_results_to_JSON, read_results_from_JSON, car_times_bar_chart, \
    print_simulation_results, plot_past_result

# initilazires
START_TIME1 = datetime.datetime(year=2023, month=6, day=29, hour=8, minute=0, second=0)
START_TIME2 = datetime.datetime(year=2023, month=6, day=29, hour=19, minute=0, second=0)
START_TIME3 = datetime.datetime(year=2023, month=6, day=29, hour=13, minute=0, second=0)
START_TIME4 = datetime.datetime(year=2023, month=6, day=30, hour=12, minute=0, second=0)
START_TIME5 = datetime.datetime(year=2023, month=7, day=1, hour=15, minute=0, second=0)

# Constants for time intervals
WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60

# Simulation parameters
NUMBER_OF_SIMULATIONS = 1
TRAFFIC_LIGHTS = True
ADD_TRAFFIC_WHITE_NOISE = False
Rain_intensity = 0 # 0-3 (0 = no rain, 1 = light rain, 2 = moderate rain, 3 = heavy rain)


# Q-Learning parameters
USE_ALREADY_GENERATED_Q_TABLE = False
NUM_EPISODES = 2500

# Animation parameters
ANIMATE_SIMULATION = False
REPEAT = True
SIMULATION_SPEED = 10  # X30 faster than one second interval

# Initialize Simulation Manager
SM = Simulation_manager.Simulation_manager('TLV', 7 * DAY, TRAFFIC_LIGHTS, Rain_intensity, ADD_TRAFFIC_WHITE_NOISE, START_TIME1)
# CM = SM.car_manager
RN = SM.road_network

# Block roads
# RN.block_road(534)
# SM.update_road_blockage(168, START_TIME1)
# SM.update_road_blockage(181, START_TIME2)
# SM.update_road_blockage(182)
# SM.update_road_blockage(912)
# SM.update_road_blockage(382)

# Initialize cars
cars = []
# for i in range(20):
#     src1, dst1 = get_random_src_dst(RN)
#     cars.append(Car.Car(i, src1, dst1, START_TIME1, RN, route_algorithm = "q", num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))

src2, dst2 = 250, 207
src4, dst4 = 558, 735
src3, dst3 = get_random_src_dst(RN)
cars.append(Car.Car(1, src2, dst2, START_TIME1, RN, route_algorithm="sp",use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
# cars.append(Car.Car(2, src3, dst3, START_TIME1, RN, route_algorithm="q",num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
# cars.append(Car.Car(3, src2, dst2, START_TIME1, RN, route_algorithm="q",num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
# cars.append(Car.Car(4, src2, dst2, START_TIME1, RN, route_algorithm="q",num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))
# cars.append(Car.Car(5, src2, dst2, START_TIME1, RN, route_algorithm="q",num_episodes = NUM_EPISODES, use_existing_q_table = USE_ALREADY_GENERATED_Q_TABLE))


# Run simulations
SM.run_full_simulation(cars, NUMBER_OF_SIMULATIONS, num_episodes = 3500, max_steps_per_episode = 150)
routes = SM.get_simulation_routes(cars, 0)

# Initialize Animation
ASS = AS.Animate_Simulation(animation_speed=SIMULATION_SPEED, repeat=REPEAT)

json_name = save_results_to_JSON(SM.graph_name,SM.simulation_results)
SM.simulation_results = read_results_from_JSON(SM.graph_name)
print_simulation_results(SM)
plot_past_result(json_name)

# car_times_bar_chart(SM, 2)
# car_times_bar_chart(SM, 1)
# car_times_bar_chart(SM, 3)

# Manage and display simulation results
# Plot and display simulation results
if ANIMATE_SIMULATION:
    ASS.plotting_custom_route(SM, routes, cars)



