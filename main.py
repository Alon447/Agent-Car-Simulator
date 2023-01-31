import networkx as nx
import osmnx as ox
import folium
import matplotlib.pyplot as plt

def test():
    # specify origin and destination coordinates
    origin = (37.7896239, -122.4011153)
    destination = (37.7888889, -122.3991668)

    # download the street network within a 1km buffer of the origin and destination
    G = ox.graph_from_point(origin, dist=3000, network_type='drive')
    G = ox.project_graph(G)

    # calculate the shortest path
    route = nx.shortest_path(G, origin, destination)

    # create a folium map centered at the origin
    m = folium.Map(location=origin, zoom_start=13)

    # add the route to the map as a red line
    folium.PolyLine(route, color='red', weight=2.5, opacity=1).add_to(m)

    # add markers for the origin and destination
    folium.Marker(origin, icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(destination, icon=folium.Icon(color='red')).add_to(m)

    # display the map
    m


TEL_AVIV = (32.11, 32.07, 34.79, 34.75) # north, south, east, west
POLEG = [32.2874, 32.2677, 34.8591, 34.8313] # north, south, east, west
# define the bounding box for Tel Aviv
north, south, east, west = 32.11, 32.07, 34.79, 34.75

# download the road network data for Tel Aviv
G = ox.graph_from_bbox(POLEG[0],POLEG[1],POLEG[2],POLEG[3], network_type='drive')
"""
# plot the road network

fig, ax = ox.plot_graph(G, node_size=0, edge_linewidth=0.5)
G=G.to_directed().edges(data=True)

print(G)
# show the plot
#plt.show()

lat = 40.7896239
lon = -73.9598939
distance = 2000
#graph = ox.graph_from_point((lat, lon), network_type='drive')
ox.plot_graph(G)
#print(G.nodes())
#print(G.degree(297034569))
#route = ox.shortest_path(G=G, orig=297034569, dest=298072093)
#ox.plot_graph_route(G, route)
# create a directed graph
dir_graph = G.to_directed()

# create the dual graph
ox.plot_graph(dir_graph)
"""

test()

