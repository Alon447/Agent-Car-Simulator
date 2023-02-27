import networkx as nx

# create an empty graph
from matplotlib import pyplot as plt

G = nx.Graph()

# add nodes (intersections) to the graph
G.add_node("A")
G.add_node("B")
G.add_node("C")
G.add_node("D")

# add edges (roads) to the graph
G.add_edge("A", "B")
G.add_edge("B", "C")
G.add_edge("C", "D")
G.add_edge("D", "A")

# visualize the graph
G.number_of_nodes()
plt.show()

