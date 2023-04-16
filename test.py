import numpy as np
import networkx as nx
import osmnx as ox

# Load the map data from OSM
from matplotlib import pyplot as plt

G = ox.load_graphml('./data/tel aviv.graphml')


# Convert the graph to a transition matrix
T = np.zeros((G.number_of_nodes(), G.number_of_nodes(), G.number_of_edges()))
#print(len(G.nodes()))
for i, u in enumerate(G.nodes()):
   # print(i)
    for j, v in enumerate(G.nodes()):
        if u != v:
            try:
                paths = nx.all_shortest_paths(G, u, v, weight="length")
                for path in paths:
                    for k in range(len(path) - 1):
                        edge=G[path[k]][path[k + 1]][0]["edge_id"]
                        T[i, j, int(edge)] = 1
            except nx.NetworkXNoPath:
                pass

# Define the reward matrix
R = np.zeros((G.number_of_nodes(), G.number_of_nodes()))
for i, u in enumerate(G.nodes()):
    for j, v in enumerate(G.nodes()):
        if u != v:
            try:
                path = nx.shortest_path(G, u, v, weight="length")
                R[i, j] = -len(path)
            except nx.NetworkXNoPath:
                pass
R = np.where(R == 0, -100000, R)
print("R", R[20])
# Define the Q-learning parameters
learning_rate = 0.2
discount_factor = 0.1
epsilon = 0.05
n_episodes = 10000
max_steps = 100

# Initialize the Q-table
n_states = G.number_of_nodes()
n_actions = G.number_of_edges()
Q = np.zeros((n_states, n_actions))


# Define the Q-learning algorithm
def q_learning(Q, R, T, learning_rate, discount_factor, epsilon, n_episodes, max_steps):
    start_node = 4
    end_node = 8
    for i in range(n_episodes):
        # Initialize the state
        #print(i)
        #s = np.random.randint(0, n_states)
        #destination = np.random.randint(0, n_states)
        s=start_node
        dest=end_node
        for j in range(max_steps):
            # Choose an action based on the epsilon-greedy strategy
            if np.random.rand() < epsilon:
                a = np.random.randint(0, n_actions)
            else:
                a = np.argmax(Q[s, :])

            # Take the chosen action and observe the next state and reward
            s_next = np.argmax(T[s, :, a])

            r = R[s, s_next]

            # Update the Q-value for the current state-action pair
            Q[s, a] += learning_rate * (r + discount_factor * np.max(Q[s_next, :]) - Q[s, a])
            #print(Q[s, a])
            # Update the state
            s = s_next
            # Check if the episode is over
            if np.random.rand() < 0.1:
                break
    return Q


# Run the Q-learning algorithm
Q = q_learning(Q, R, T, learning_rate, discount_factor, epsilon, n_episodes, max_steps)

# Find the shortest path using the learned Q-table
start_node = 4
end_node = 8
path = [start_node]
s = start_node
i=0
np.set_printoptions(threshold=np.inf)

print(f"Q\n")
print(Q[s, :])


while s != end_node:
    print("s", s)
    a = np.argmax(Q[s, :])
    print("a",a)
    if max(T[s, :, a])==0:
        break
    s_next = np.argmax(T[s, :, a])
    print("T",(T[s, :, a]))
    s = s_next
    path.append(s)
    i+=1
    if i>=10:
        break
#path = nx.shortest_path(G, start_node, end_node)
graph_node_id = {}
for i, node in enumerate(G.nodes):
    graph_node_id[i] = node
# Plot the map and the shortest path
print(path)
#print(graph_node_id)
path2= []
for a in path:
    path2.append(graph_node_id[a])
print(f"Result path:  {path2}")

b=ox.shortest_path(G, graph_node_id[start_node], graph_node_id[end_node], weight="length")
print(f"Shotest path:  {b}")
#fig, ax = ox.plot_graph_route(G, b, node_size=0, edge_linewidth=0.5)
#plt.show()