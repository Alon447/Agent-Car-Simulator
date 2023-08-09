# import csv
# from datetime import datetime
#
# from matplotlib import pyplot as plt
#
#
# def get_speeds_for_id(csv_filename, target_id):
#     speeds_list = []
#     dates=[]
#
#     with open(csv_filename, newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter='\t')
#
#         # Skip the header row
#         next(reader)
#
#         # Iterate through the rows and find the speeds for the specific ID
#         for row in reader:
#             r = row[0].split(",")
#             current_id = r[0]
#
#             if current_id == target_id:
#                 speeds=[]
#                 for i in range(2, 32, 5):
#                     date_time_str = r[i+3]
#                     date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
#
#                     dates.append(date_time_obj)
#                     if r[i] == 'ND':
#                         if i == 2:
#                             speeds.append(speeds_list[-1])
#                         else:
#                             speeds.append(speeds[-1])
#                     else:
#                         speeds.append(float(r[i]))
#
#                 # speeds = [r[2], r[7], r[12], r[17], r[22], r[27]]
#                 speeds_list.extend(speeds)
#
#     return dates, speeds_list
#
# # Replace 'Graphs.csv' with the actual filename of your CSV file
# csv_filename = 'trafficinfo.csv'
# target_id = '1210030100'  # Replace with the specific ID you want to extract speeds for
#
# dates, speeds_for_id = get_speeds_for_id(csv_filename, target_id)
# print("Speeds for ID {}: {}".format(target_id, speeds_for_id))
# # Plot the graph
# plt.figure(figsize=(10, 6))
# plt.plot(dates, speeds_for_id, marker='o', linestyle='-')
# plt.xlabel("Time")
# plt.ylabel("Speed (km/h)")
# plt.title("Speeds over Time")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()
import datetime

import numpy as np
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Set the parameters for the normal distribution
# mean = 40  # Mean of the distribution
# std_dev = 1  # Standard deviation of the distribution
# num_samples = 10000  # Number of samples in the list
#
# # Generate the list of numbers following a normal distribution
# normal_distribution_data = np.random.normal(mean, std_dev, num_samples)
#
# # Plot the histogram to visualize the distribution
# plt.hist(normal_distribution_data, bins=50, density=True, alpha=0.6, color='g')
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Random Numbers Following Normal Distribution')
# plt.grid(True)
# plt.show()
import osmnx as ox
from matplotlib import pyplot as plt


def get_lat_lng(address):
    # Perform geocoding
    location = ox.geocode(address)
    latitude = location[0]
    longitude = location[1]
    return latitude, longitude

def main():
    while(True):
        address = input("Enter an address: ")

        lat, lng = get_lat_lng(address)

        if lat is not None and lng is not None:
            print(f"Latitude: {lat}, Longitude: {lng}")

if __name__ == "__main__":
    # Retrieve the graph
    G = ox.load_graphml('../Graphs/TLV.graphml')

    # Plot the graph
    fig, ax = ox.plot_graph(ox.project_graph(G), show=False)

    # Add raindrops effect
    num_raindrops = 500
    x_coords = np.random.uniform(ax.get_xlim()[0], ax.get_xlim()[1], num_raindrops)
    y_coords = np.random.uniform(ax.get_ylim()[0], ax.get_ylim()[1], num_raindrops)
    raindrop_size = 0.1

    ax.scatter(x_coords, y_coords, s=raindrop_size, color='blue', alpha=0.6)

    # Show the rain-covered graph
    plt.show()
