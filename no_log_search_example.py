import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from strategy import binary_search, binary_search_neighbor
from utils import centroid, check_objective_function

# Construct inner graph
G = nx.Graph()
max_degree = 6
inner_nodes = list(range(1, max_degree + 1))
outer_nodes = list(range(max_degree + 1, 2 * max_degree + 1))
G.add_edges_from([(0, i) for i in inner_nodes])
G.add_edges_from([*zip(inner_nodes, outer_nodes)])

for i in range(len(inner_nodes)):
    for j in range(i + 1, len(inner_nodes)):
        v = G.number_of_nodes()
        G.add_edges_from([(inner_nodes[i], v), (v, outer_nodes[j]), (inner_nodes[j], v), (v, outer_nodes[i])])

# for i, v1 in enumerate(outer_nodes):
#     for j, v2 in enumerate(inner_nodes):
#         if i != j:
#             v = G.number_of_nodes()
#             G.add_edges_from([(v1, v), (v, v2)])
core_nodes = G.number_of_nodes()

# Add paths
path_length = 150
for v in [0] + outer_nodes:
    G_add = nx.path_graph(path_length)
    first_node = G.number_of_nodes()
    mapping = {v: first_node + v for v in G_add.nodes}
    nx.relabel_nodes(G_add, mapping, copy=False)
    # for j, node in enumerate(sorted(G_add.nodes)):
    #     f[node] = 10 + j
    G = nx.compose(G, G_add)
    G.add_edge(v, first_node)

# Extend path behind c to ensure that c is centroid
G_add = nx.path_graph(1 + 1)
mapping = {v: G.number_of_nodes() - 1 + v for v in G_add.nodes}
mapping[0] = core_nodes + path_length - 1
nx.relabel_nodes(G_add, mapping, copy=False)
G = nx.compose(G, G_add)

# Connect chains
# v = G.number_of_nodes()
# G.add_node(v)
# G.add_edges_from([(v, 13 + 2 * path_length - 1), (v, 13 + 3 * path_length - 1), (v, 13 + 4 * path_length - 1)])

# Create labels
target_node = core_nodes + 2 * path_length + 1
f = dict()
for node in G.nodes:
    if node == 0:
        f[node] = nx.shortest_path_length(G, target_node, node) + 1
    else:
        f[node] = nx.shortest_path_length(G, target_node, node) + np.random.rand()
# f = {node: nx.shortest_path_length(G, target_node, node) + np.random.rand() for node in G.nodes}

PLOT = False
if PLOT:
    pos3 = nx.spring_layout(
        G, pos={0: (0, 0), 1: (1, 1), 2: (0, -1), 3: (-1, 1), 4: (2, 2), 5: (0, -2), 6: (-2, 2)},
        fixed=[0, 1, 2, 3, 4, 5, 6]
    )
    # Layout for d = 4
    pos4 = nx.spring_layout(
        G, pos={0: (0, 0), 1: (1, 0), 2: (0, -1), 3: (-1, 0), 4: (0, 1), 5: (2, 0), 6: (0, -2), 7: (-2, 0), 8: (0, 2)},
        fixed=[0, 1, 2, 3, 4, 5, 6, 7, 8]
    )
    if max_degree == 3:
        pos = pos3
    elif max_degree == 4:
        pos = pos4
    else:
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
v_min = binary_search(G, t, f, PLOT, pos)
assert v_min == target_node, "Did not find the correct node!"
queries = sum(~np.isnan(list(t.values())))
print(f"Active: Found minimum with with {queries} {"query" if queries == 1 else "queries"}.")

degree_sequence = (d for n, d in G.degree())
d_max = max(degree_sequence)
n = nx.number_of_nodes(G)
print(f"Theoretical bound for d = {d_max} and n = {n} is d log n =", d_max * np.log2(n))
