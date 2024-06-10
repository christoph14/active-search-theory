import sys
import networkx as nx
from strategy import binary_search
from utils import read_graph
from visualization import plot_iteration
import numpy as np

# Specify graph

G=read_graph("core-star")

distances = nx.floyd_warshall_numpy(G,sorted(G.nodes))
plot_node_positions = nx.kamada_kawai_layout(G)
node_labels = nx.get_node_attributes(G, 'objective')
target_node = min(node_labels,key=node_labels.get)


#Specify algorithm

stats = binary_search(G, distances)

#Specify plots

for iteration in stats:
    S,selected_node = iteration
    plot_iteration(G,S,selected_node,target_node,plot_node_positions)