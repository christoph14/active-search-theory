import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from strategy import binary_search
from utils import check_objective_function

G = nx.path_graph(32)
f = {i: i for i in G.nodes}

nx.draw(G, with_labels=True)
plt.show()
nx.draw(G, with_labels=True, labels=f)
plt.show()

nx.set_node_attributes(G, f, 'objective')
assert check_objective_function(G), "Error: Objective function is not convex."
target_node = min(f, key=f.get)

# Active search
t = {node: np.nan for node in G.nodes}
v_min = binary_search(G, t, f)
assert v_min == target_node, "Did not find the correct node!"
queries = sum(~np.isnan(list(t.values())))
print(f"Active: Found minimum with with {queries} {"query" if queries == 1 else "queries"}.")

degree_sequence = (d for n, d in G.degree())
d_max = max(degree_sequence)
n = nx.number_of_nodes(G)
print(f"Theoretical bound for d = {d_max} and n = {n} is (d+1) log n =", (d_max + 1) * np.log2(n))
