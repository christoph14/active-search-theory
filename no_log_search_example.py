import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from strategy import binary_search, binary_search_neighbor
from utils import centroid, check_objective_function

G = nx.Graph()
# G.add_edges_from([
#     (0, 1), (0, 2), (0, 3), (1, 4), (1, 6), (1, 10), (2, 5), (2, 7), (2, 11), (3, 8), (3, 9), (3, 12), (4, 5), (4, 8),
#     (6, 7), (7, 9), (10, 12), (11, 12)
# ])
# f = {0: 10, 1: 1, 2: 2, 3: 3, 4: 5, 5: 3, 6: 2, 7: 5, 8: 4, 9: 4, 10: -1, 11: -1, 12: -2}

G.add_edges_from([
    (0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (1, 7), (2, 5), (2, 6), (2, 8), (3, 7), (3, 8), (3, 9), (4, 5), (4, 7),
    (5, 6), (6, 8), (7, 9), (8, 9)
])

max_degree = 5
G.add_edges_from([
    (0, i) for i in range(1, max_degree + 1)
])

inner_nodes = G.number_of_nodes()

path_length = 2
for i in range(4):
    G_add = nx.path_graph(path_length)
    mapping = {v: G.number_of_nodes() + v for v in G_add.nodes}
    nx.relabel_nodes(G_add, mapping, copy=False)
    # for j, node in enumerate(sorted(G_add.nodes)):
    #     f[node] = 10 + j
    G = nx.compose(G, G_add)
# G.add_edges_from([(0, 13), (4, 13 + path_length), (7, 13 + 2 * path_length), (12, 13 + 3 * path_length)])
G.add_edges_from([(0, 10), (4, 10 + path_length), (6, 10 + 2 * path_length), (9, 10 + 3 * path_length)])

# Add strange nodes and edges
# v1 = G.number_of_nodes()
# v2 = G.number_of_nodes() + 1
# G.add_edges_from([(v1, 4), (v1, 11), (v2, 5), (v2, 12)])
# print(f"Strange nodes: {v1}, {v2}")

# Extend path behind c to ensure that c is centroid
G_add = nx.path_graph(1 + 1)
mapping = {v: G.number_of_nodes() - 1 + v for v in G_add.nodes}
mapping[0] = inner_nodes + path_length - 1
nx.relabel_nodes(G_add, mapping, copy=False)
G = nx.compose(G, G_add)

# Connect chains
# v = G.number_of_nodes()
# G.add_node(v)
# G.add_edges_from([(v, 13 + 2 * path_length - 1), (v, 13 + 3 * path_length - 1), (v, 13 + 4 * path_length - 1)])

# Create labels
target_node = inner_nodes + 2 * path_length
f = dict()
for node in G.nodes:
    if node == 0:
        f[node] = nx.shortest_path_length(G, target_node, node) + 1
    else:
        f[node] = nx.shortest_path_length(G, target_node, node) + np.random.rand()
# f = {node: nx.shortest_path_length(G, target_node, node) + np.random.rand() for node in G.nodes}
print('Difficult case?', f[1] > f[4])

PLOT = True
if PLOT:
    # pos = nx.spring_layout(
    #     G, pos={0: (0, 0), 1: (-1, 1), 2: (1, 1), 3: (0, -1), 4: (-2, 2), 7: (2, 2), 12: (0, -2), 13: (0, 2.5)},
    #     fixed=[0, 1, 2, 3, 4, 7, 12, 13]
    # )
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, pos=pos)
    plt.show()
    nx.draw(G, with_labels=True, pos=pos, labels=f)
    plt.show()
else:
    pos = None

nx.set_node_attributes(G, f, 'objective')
assert check_objective_function(G), "Error: Objective function is not convex."
target_node = min(f, key=f.get)

print("Center nodes:", centroid(G, G.nodes, return_all=True))

# Active search
t = {node: np.nan for node in G.nodes}
v_min = binary_search_neighbor(G, t, f, PLOT, pos)
assert v_min == target_node, "Did not find the correct node!"
queries = sum(~np.isnan(list(t.values())))
print(f"Active: Found minimum with with {queries} {"query" if queries == 1 else "queries"}.")

degree_sequence = (d for n, d in G.degree())
d_max = max(degree_sequence)
n = nx.number_of_nodes(G)
print(f"Theoretical bound for d = {d_max} and n = {n} is d log n =", d_max * np.log2(n))
