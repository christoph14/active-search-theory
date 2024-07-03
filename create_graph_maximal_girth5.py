from enum import unique
from math import ceil, floor, sqrt
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np

from utils import check_objective_function, create_objective, write_graph
from visualization import plot_iteration, plot_graph

def find_pair(H):
    distances = nx.floyd_warshall_numpy(H)
    degrees=np.array([d for n,d in H.degree()])
    weighted_distances =  distances * np.outer(degrees,degrees)
    #print(distances)
    matches = np.where(distances==4)
    if len(matches[0])==0:
        matches = np.where(distances==3)
    if len(matches[0])==0:
        return None
    minweight_index=np.argmin([weighted_distances[i][j] for i,j in zip(matches[0],matches[1])])
    v=matches[0][minweight_index]
    w=matches[1][minweight_index]
    return [v,w,distances[v][w]]


n=10
H=nx.petersen_graph()
H.add_node(n)
H.add_edge(0,n)
n+=1
while((pair:=find_pair(H))!=None):
    #plot_graph(H)
    v,w,dist = pair
    print(pair)
    if dist==3:
        H.add_node(n)
        H.add_edge(v,n)
        H.add_edge(w,n)
        n+=1
    if dist==4:
        H.add_edge(v,w)
    print(n)
    print(max([(d,n) for n,d in H.degree()]))
    
print("END")
plot_graph(H)



# Generalization of Petersen graph:
# Start with C5 plus extra connected node
# While there is a node pair of distance 3,4 which is not contained in a C5 (prove that >=5 cannot happen)
#   If pair distance is 3:
#       Add new node and edges to complete a C5
#   If pair distance is 4:
#       Add edge to complete C5

#    graph_name=f"data/Generalized_Petersen_{k}.pickle"

#    H=create_objective(H)

#    print(f"Objective is {"" if check_objective_function(H) else "not"} convex.")


#    assert check_objective_function(H), "Error: Objective function is not convex."
#    write_graph(H,graph_name)
