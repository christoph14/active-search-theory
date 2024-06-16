from math import ceil, floor, sqrt
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np

from utils import check_objective_function, create_objective, write_graph
from visualization import plot_iteration

H=nx.cycle_graph(5)


# Generalization of Petersen graph:
# Join H with its complement and connect each node with its copy
# New graph has still girth5 and a new C_5 for every pair of old nodes
# The edges are unfortunately not well distributed after a few iterations
for k in range(1,10):
    G=H
    complement = nx.complement(G)
    H=nx.union(G,complement,rename=("O","C"))
    H.add_edges_from([[f"O{i}",f"C{i}"] for i in G.nodes()])

    #nx.draw(H,with_labels=True)
    #plt.show()
    
    graph_name=f"data/Generalized_Petersen_{k}.pickle"

    H_relabeled = nx.relabel_nodes(H,{v:i for i,v in enumerate(H.nodes())},copy=True)
    H_relabeled=create_objective(H_relabeled)

    print(f"Objective is {"" if check_objective_function(H_relabeled) else "not"} convex.")


    assert check_objective_function(H_relabeled), "Error: Objective function is not convex."
    write_graph(H_relabeled,graph_name)
