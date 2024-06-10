import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from strategy import random_selection, binary_search
from utils import check_objective_function, create_objective_function_star

# Initialise random generator
seed = None  # 6
rng = np.random.default_rng(seed)

# Create random graph
n = 100
p = 0.05
G = nx.erdos_renyi_graph(n, p, seed=rng)
# G = nx.random_regular_graph(d=3, n=n)
iterations = 1
while not nx.is_connected(G):
    if iterations >= 1000:
        break
    iterations += 1
    G = nx.erdos_renyi_graph(n, p, seed=rng)
assert nx.is_connected(G), f"Could not generate a connected graph in {iterations} iterations!"
print("Graph created.")
G = nx.convert_node_labels_to_integers(G)

# Create objective function
f = create_objective_function_star(G, seed=rng)
nx.set_node_attributes(G, f, 'objective')
assert check_objective_function(G), "Error: Objective function is not convex."
target_node = min(f, key=f.get)

# Plot generated graph
PLOT = False
if PLOT:
    colors = ['#1f78b4'] * n
    colors[target_node] = 'red'
    pos = nx.spring_layout(G, seed=22)
    nx.draw_networkx(G, pos=pos, node_color=colors, node_size=600)
    plt.show()
    node_labels = {node: round(value, 2) for node, value in f.items()}
    nx.draw_networkx(G, pos=pos, node_color=colors, node_size=600, labels=node_labels)
    plt.show()

# Random search
t = {node: np.nan for node in G.nodes}
queries = 0
while np.isnan(t[target_node]):
    v = random_selection(G, t)
    queries += 1
    t[v] = f[v]
print(f"Random: Found minimum with with {queries} {"query" if queries == 1 else "queries"}.")

# Active search
t = {node: np.nan for node in G.nodes}
v_min = binary_search(G, t, f)
assert v_min == target_node, "Did not find the correct node!"
queries = sum(~np.isnan(list(t.values())))
print(f"Active: Found minimum with with {queries} {"query" if queries == 1 else "queries"}.")

degree_sequence = (d for n, d in G.degree())
d_max = max(degree_sequence)
n = nx.number_of_nodes(G)
print(f"Theoretical bound for d = {d_max} and n = {n} is d log n =", d_max * np.log2(n))
