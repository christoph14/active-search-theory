import networkx as nx
import numpy as np

from utils import check_objective_function, create_objective, write_graph
from visualization import plot_iteration

#Specify name
graph_name="data/Petersen.pickle"
G=nx.petersen_graph()

G=create_objective(G)

print(f"Objective is {"" if check_objective_function(G) else "not"} convex.")

node_positions=nx.spring_layout(G)
plot_iteration(G,G.nodes, node_positions, target_node=0)


assert check_objective_function(G), "Error: Objective function is not convex."
write_graph(G,graph_name)
