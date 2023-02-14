import folium
import matplotlib.pyplot as plt
from neo4j import GraphDatabase, basic_auth
import pandas as pd
import osmnx as ox
import networkx as nx
import json
from shapely.wkt import dumps


def OSMGraphToNeo4j():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))
    session = driver.session()

    # Load data into a Pandas DataFrame
    data = pd.read_csv("nodes.csv")

    # Create nodes in Neo4j
    for index, row in data.iterrows():
        query = "CREATE (n:Node {id: {id}, latitude: {latitude}, longitude: {longitude}})"
        session.run(query, id=row["id"], latitude=row["latitude"], longitude=row["longitude"])

    # Create relationships in Neo4j
    for index, row in data.iterrows():
        query = "MATCH (n:Node), (m:Node) WHERE n.id = {id} AND m.id = {source_id} CREATE (m)-[:ROAD {length: {length}}]->(n)"
        session.run(query, id=row["id"], source_id=row["source_id"], length=row["length"])

    # Close the session and driver
    session.close()
    driver.close()



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

def OSMGraphToCSV(g):
    df = ox.graph_to_gdfs(G, nodes=True, edges=True)
    print(df)
    df.to_csv('nodes.csv')

TEL_AVIV = (32.11, 32.07, 34.79, 34.75) # north, south, east, west
TEL_AVIV_MINI = (32.0974, 32.0926, 34.7768, 34.7735) # north, south, east, west
POLEG = [32.2838, 32.2684, 34.8529, 34.8361] # north, south, east, west
# define the bounding box for Tel Aviv
north, south, east, west = 32.11, 32.07, 34.79, 34.75

# download the road network data for Tel Aviv
G = ox.graph_from_bbox(POLEG[0],POLEG[1],POLEG[2],POLEG[3], network_type='drive')
#G = ox.graph_from_bbox(TEL_AVIV_MINI[0],TEL_AVIV_MINI[1],TEL_AVIV_MINI[2],TEL_AVIV_MINI[3], network_type='drive')
# download the street network of the location as a graph
for u, v, data in G.edges(data=True):
    print(data)
    #print(u)
    #print(v)
ox.plot_graph(G)
OSMGraphToCSV(G)
#OSMGraphToNeo4j()
#testNeo4j()
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

#test()

