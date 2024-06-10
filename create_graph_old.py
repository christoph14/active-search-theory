
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from utils import centroid, check_objective_function, write_graph, read_graph


G = nx.Graph()
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
    G = nx.compose(G, G_add)
G.add_edges_from([(0, 10), (4, 10 + path_length), (6, 10 + 2 * path_length), (9, 10 + 3 * path_length)])

# Extend path behind c to ensure that c is centroid
G_add = nx.path_graph(1 + 1)
mapping = {v: G.number_of_nodes() - 1 + v for v in G_add.nodes}
mapping[0] = inner_nodes + path_length - 1
nx.relabel_nodes(G_add, mapping, copy=False)
G = nx.compose(G, G_add)


# Create labels
target_node = inner_nodes + 2 * path_length
f = dict()
for node in G.nodes:
    if node == 0:
        f[node] = nx.shortest_path_length(G, target_node, node)*10 + 10
    else:
        f[node] = nx.shortest_path_length(G, target_node, node)*10 + np.random.randint(0,10)
# f = {node: nx.shortest_path_length(G, target_node, node) + np.random.rand() for node in G.nodes}
print('Difficult case?', f[1] > f[4])

nx.set_node_attributes(G, f, 'objective')
assert check_objective_function(G), "Error: Objective function is not convex."
target_node = min(f, key=f.get)

print("Center nodes:", centroid(G, G.nodes, return_all=True))

write_graph(G,"core-star-integral")
