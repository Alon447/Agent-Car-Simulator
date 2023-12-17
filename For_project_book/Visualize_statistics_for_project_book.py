import statistics

import matplotlib.pyplot as plt
import json
import Utilities.Getters as Getters
import osmnx as ox
from Main_Files import Road_Network

if __name__ == "__main__":
    run_time_data_file_name = "TLV_run_time_data.json" #enter the name of the file you want to visualize
    cars_times_file_name = "TLV_cars_times.json" #enter the name of the file you want to visualize
    with open(f'../{Getters.Route_comparisons_results_directory}/{run_time_data_file_name}', 'r') as infile:
        new_simulation_results = json.load(infile)
    sp_run_times = []
    q_run_times = []
    q_learning_times = []
    for run in new_simulation_results:
        sp_run_times.append(new_simulation_results[run][Getters.SP])
        q_run_times.append(new_simulation_results[run][Getters.Q])
        q_learning_times.append(new_simulation_results[run][Getters.Q+" learning_time"])

    # avarage run times and standard deviation
    sp_avg = sum(sp_run_times) / len(sp_run_times)
    q_avg = sum(q_run_times) / len(q_run_times)
    q_learning_times_avg = sum(q_learning_times) / len(q_learning_times)
    sp_std = statistics.stdev(sp_run_times)
    q_std = statistics.stdev(q_run_times)
    q_learning_times_std = statistics.stdev(q_learning_times)
    print("sp run times in seconds is %.3f" % sp_avg, "+-%.3f" % sp_std, " standard deviation")
    print("q run times in seconds is %.3f" % q_avg, "+-%.3f" % q_std, " standard deviation")
    print("q learning times in seconds is %.3f" % q_learning_times_avg, "+-%.3f" % q_learning_times_std, " standard deviation")

    # plot run times with sp as x axis and q as y axis
    plt.plot(sp_run_times, q_run_times, 'o')
    plt.xlabel("sp run times in seconds")
    plt.ylabel("q run times in seconds")
    plt.show()

    # car's driving times: sp vs q learning
    with open(f'../{Getters.Route_comparisons_results_directory}/{cars_times_file_name}', 'r') as infile:
        times_data = json.load(infile)
    sp_times = []
    q_times = []
    sp_times_by_sim = []
    q_times_by_sim = []
    # organize times by algorithm. every even index is sp, every odd index is q.
    # every index is a list of times of cars in the simulation, currently when writing this code
    # and comment-the simulation is with 5 cars.
    for run in times_data:
        sp_times+=times_data[run][Getters.SP]
        q_times+=times_data[run][Getters.Q]

    #   average times and standard deviation
    sp_avg_drive_time = sum(sp_times) / len(sp_times)
    q_avg_drive_time = sum(q_times) / len(q_times)
    sp_std_drive_time = statistics.stdev(sp_times)
    q_std_drive_time = statistics.stdev(q_times)
    print("sp drive times in seconds is %.3f" % sp_avg_drive_time, "+- %.3f" % sp_std_drive_time)
    print("q drive times in seconds is %.3f" % q_avg_drive_time, "+-%.3f" % q_std_drive_time)
    print("*" * 50)

    #   calculate how many times Q learning was faster than SP
    q_faster_count = 0
    q_equal_count = 0
    sp_fast_count = 0
    for i in range(len(sp_times)):
        if sp_times[i] > q_times[i]:
            q_faster_count += 1
        elif sp_times[i] == q_times[i]:
            q_equal_count += 1
        else:
            sp_fast_count += 1
    print("q navigation was faster than sp navigation", q_faster_count, " times")
    print("q navigation was equal to sp navigation", q_equal_count, " times")
    print("sp navigation was faster than q navigation", sp_fast_count, " times")
    print("*" * 50)

    # scatter q times vs sp times
    x_values = []
    for i in range(len(sp_times)):
        x_values.append(i)
    plt.plot(x_values, sp_times, 'o', label="sp")
    plt.plot(x_values, q_times, 'o', label="q")
    plt.xlabel("agent time index in the times array")
    plt.ylabel("time in seconds")
    plt.title("sp vs q learning times")
    plt.legend()
    plt.show()

    plt.cla()
    plt.clf()
    plt.close()

    q_to_sp_time_ratio = []
    for i in range(len(sp_times)):
        q_to_sp_time_ratio.append(sp_times[i] / q_times[i])

    plt.hist(q_to_sp_time_ratio, bins=20, edgecolor='black', linewidth=1.2)
    plt.xlabel("sp time / q time")
    plt.ylabel("number of cars")
    plt.title("sp time / q time histogram")
    plt.show()

    plt.cla()
    plt.clf()
    plt.close()

    sp_run_faster_count = 0
    q_run_faster_count = 0
    same_time_count = 0

    sp_to_q_run_time_ratio = []
    for i in range(len(sp_run_times)):
        sp_to_q_run_time_ratio.append(sp_run_times[i] / q_run_times[i])
        if sp_run_times[i] > q_run_times[i]:
            q_run_faster_count += 1
        elif sp_run_times[i] < q_run_times[i]:
            sp_run_faster_count += 1
        else:
            same_time_count += 1
    plt.hist(sp_to_q_run_time_ratio, bins=20, edgecolor='black', linewidth=1.2)
    plt.xlabel("sp run time / q run time")
    plt.ylabel("number of runs")
    plt.title("sp run time / q run time histogram")
    plt.show()

    plt.cla()
    plt.clf()
    plt.close()

    print("sp ran faster than q run", sp_run_faster_count, " times")
    print("q ran faster than sp run", q_run_faster_count, " times")
    print("sp ran equal to q run", same_time_count, " times")

    # scatter the nodes used in the simulation
    RN = Road_Network.Road_Network("TLV")
    fig, ax = ox.plot_graph(RN.graph, bgcolor='white', node_color='black', show=False, close=False)
    plt.title("Nodes used in the simulation")
    # plt.show()

    all_nodes = ["blue"] + Getters.top_right_nodes + ["purple"] + Getters.bottom_right_nodes + [
        "red"] + Getters.bottom_left_nodes + ["green"] + Getters.top_left_nodes
    cur_color = "blue"
    for node in all_nodes:
        if type(node) == str:
            cur_color = node
            continue
        x, y = RN.get_xy_from_node_id(node)
        ax.scatter(x, y, color=cur_color, s=50)
        # plt.legend()
    plt.show()