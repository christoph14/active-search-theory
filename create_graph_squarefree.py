from math import ceil, floor, sqrt
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np

from utils import check_objective_function, create_objective, write_graph
from visualization import plot_iteration

#Specify name
for p in range(5,50):
    if any([i if p/i==p//i else 0 for i in range(2,ceil(sqrt(p))+1)]):
            continue
    graph_name=f"data/squarefree/squarefree_p{p}.pickle"
    V=[(a,b) for a in range(1,p) for b in range(p)]
    G = nx.Graph()
    G.add_nodes_from(V)
    for a in range(1,p):
        for b in range(p):
            for c in range(1,p):
                d =(a*c-b) % p
                G.add_edge((a,b),(c,d))
                print((a,b),(c,d))
    #nx.draw(G,with_labels=True)
    #plt.show()
    nx.relabel_nodes(G,{v:i for i,v in enumerate(G.nodes())},copy=False)
    G=create_objective(G)

    print(f"Objective is {"" if check_objective_function(G) else "not"} convex.")


    assert check_objective_function(G), "Error: Objective function is not convex."
    write_graph(G,graph_name)
