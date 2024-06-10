import networkx as nx

from utils import check_objective_function, write_graph

#Specify name
graph_name="Path32"

G = nx.path_graph(32)
f = {i: i for i in G.nodes}

nx.set_node_attributes(G, f, 'objective')



assert check_objective_function(G), "Error: Objective function is not convex."
write_graph(G,graph_name)
