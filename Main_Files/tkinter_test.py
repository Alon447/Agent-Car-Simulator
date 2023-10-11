import datetime
import PySimpleGUI as sg
from Main_Files import Car
import Simulation_manager
import GUI.Animate_Simulation as AS

# Constants for time intervals
WEEK = 604800
DAY = 86400
HOUR = 3600
MINUTE = 60
# Simulation parameters
SIMULATION_SPEEDS_JSON_NAME = "simulation_speeds.json"
TRAFFIC_LIGHTS = True
USE_ALREADY_GENERATED_Q_TABLE = True
NUMBER_OF_SIMULATIONS = 1
Rain_intensity = 0 # 0-3 (0 = no rain, 1 = light rain, 2 = moderate rain, 3 = heavy rain)
REPEAT = True
SIMULATION_SPEED = 30  # X30 faster than one second interval
# Define the layout of the GUI
layout = [
    [sg.Text("Simulation Start Time:"), sg.InputText("2023-06-29 08:00:00", key="start_time")],
    [sg.Text("Number of Simulations:"), sg.InputText("1", key="num_simulations")],
    [sg.Text("Simulation Speed:"), sg.InputText("30", key="simulation_speed")],
    [sg.Button("Start Simulation"), sg.Button("Exit")],
    [sg.Output(size=(60, 20))]
]

# Create the window
window = sg.Window("Traffic Simulation GUI", layout)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    if event == "Start Simulation":
        # Convert user input to appropriate data types
        start_time = datetime.datetime.strptime(values["start_time"], "%Y-%m-%d %H:%M:%S")
        num_simulations = int(values["num_simulations"])
        simulation_speed = float(values["simulation_speed"])

        # Initialize Simulation Manager
        SM = Simulation_manager.Simulation_manager('TLV', 3 * DAY, TRAFFIC_LIGHTS, Rain_intensity, start_time, SIMULATION_SPEEDS_JSON_NAME)
        CM = SM.car_manager
        RN = SM.road_network
        RN.blocked_road(534)

        # Initialize Animation
        ASS = AS.Animate_Simulation(animation_speed=simulation_speed, repeat=REPEAT)

        # Initialize cars
        cars = []
        cars.append(Car.Car(1, 15, 410, start_time, RN, route_algorithm="q", use_existing_q_table=USE_ALREADY_GENERATED_Q_TABLE))
        cars.append(Car.Car(3, 15, 510, start_time, RN, route_algorithm="sp"))

        # Run simulations
        SM.run_full_simulation(cars, num_simulations)
        routes = SM.get_simulation_routes(cars, 0)

        # Plot and display simulation results
        ASS.plotting_custom_route(SM, routes, cars)
        # AS.car_times_bar_chart(SM, 4)
        # AS.car_times_bar_chart(SM, 1)
        # AS.car_times_bar_chart(SM, 3)

        # Manage and display simulation results
        # SRM = Simulation_Results_Manager(SM.graph_name)
        # SRM.save_results_to_JSON(SM.simulation_results)
        # SM.simulation_results = SRM.read_results_from_JSON()
        # ASS.print_simulation_results(SM)

# Close the window when the event loop exits
window.close()
