import statistics

import matplotlib.pyplot as plt
import json
import Utilities.Getters as Getters
import osmnx as ox
from Main_Files import Road_Network

if __name__=="__main__":
    with open('run_time_data.json', 'r') as infile:
        new_simulation_results = json.load(infile)
    sp_run_times = []
    q_run_times = []
    for run in new_simulation_results:
        sp_run_times.append(new_simulation_results[run]["sp"])
        q_run_times.append(new_simulation_results[run]["q"])

    # avarage run times and standard deviation
    sp_avg = sum(sp_run_times)/len(sp_run_times)
    q_avg = sum(q_run_times)/len(q_run_times)
    sp_std = statistics.stdev(sp_run_times)
    q_std = statistics.stdev(q_run_times)
    print("sp run times in seconds is ", sp_avg,"+-",sp_std)
    print("q run times in seconds is ", q_avg,"+-",q_std)

    # plot run times with sp as x axis and q as y axis
    plt.plot(sp_run_times, q_run_times, 'o')
    plt.xlabel("sp run times in seconds")
    plt.ylabel("q run times in seconds")
    plt.show()

    # car's driving times: sp vs q learning
    with open('times_data.json', 'r') as infile:
        times_data = json.load(infile)
    sp_times = []
    q_times = []
    sp_times_by_sim = []
    q_times_by_sim = []
    # organize times by algorithm. every even index is sp, every odd index is q.
    # every index is a list of times of cars in the simulation, currently when writing this code
    # and comment-the simulation is with 5 cars.
    for run in times_data:
        if int(run) % 2 == 0:
            sp_times_by_sim.append(times_data[run])
            for time in times_data[run]:
                sp_times.append(time)
            continue
        q_times_by_sim.append(times_data[run])
        for time in times_data[run]:
            q_times.append(time)

    #   average times and standard deviation
    sp_avg_drive_time = sum(sp_times)/len(sp_times)
    q_avg_drive_time = sum(q_times)/len(q_times)
    sp_std_drive_time = statistics.stdev(sp_times)
    q_std_drive_time = statistics.stdev(q_times)
    print("sp drive times in seconds is ", sp_avg_drive_time,"+-",sp_std_drive_time)
    print("q drive times in seconds is ", q_avg_drive_time,"+-",q_std_drive_time)

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
    print("q was faster than sp ", q_faster_count, " times")
    print("q was equal to sp ", q_equal_count, " times")
    print("sp was faster than q ", sp_fast_count, " times")

    # scatter q times vs sp times
    x_values = []
    for i in range(len(sp_times)):
        x_values.append(i)
    plt.plot(x_values, sp_times, 'o', label="sp")
    plt.plot(x_values, q_times, 'o', label="q")
    plt.xlabel("simulation number")
    plt.ylabel("time in seconds")
    plt.title("sp vs q learning times")
    plt.legend()
    plt.show()

    plt.cla()
    plt.clf()
    plt.close()
    # scatter the nodes used in the simulation
    RN = Road_Network.Road_Network("TLV")
    fig,ax = ox.plot_graph(RN.graph, bgcolor='white', node_color='black', show=False, close=False)
    plt.title("Nodes used in the simulation")
    # plt.show()
    all_nodes = ["blue"]+Getters.top_right_nodes +["purple"]+ Getters.bottom_right_nodes +["red"]+ Getters.bottom_left_nodes +["green"]+ Getters.top_left_nodes
    cur_color = "blue"
    for node in all_nodes:
        if type(node) == str:
            cur_color = node
            continue
        x,y = RN.get_xy_from_node_id(node)
        ax.scatter(x,y, color=cur_color, s=50)
        # plt.legend()
    plt.show()





