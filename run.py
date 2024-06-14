# %%
import sys
import os
from matplotlib import pyplot as plt
import networkx as nx
from strategy import binary_search
from utils import create_objective, read_graph
from visualization import plot_iteration
from argparse import ArgumentParser

# %%
# Parse arguments

parser = ArgumentParser()
parser.add_argument("path",help="input graph or folder of graphs", default="data/Petersen.pickle")
parser.add_argument("--plots",type=bool,default=False,help="generates an instance from every graph and every node as target")
parser.add_argument("-t","--target",type=int,help="node index to be used as target. Generates new labels.")
args = parser.parse_args()


instances = []
if os.path.isdir(args.path):
    directory = os.fsencode(args.path)    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".pickle") or filename.endswith(".s6"): 
            instances.append(os.path.join(args.path, filename))
            print(os.path.join(args.path, filename))
            continue
else:
    instances=[args.path]

# %%
for instance in instances:
    print(f"\nInstance: {instance}")
    G=read_graph(instance)
    if args.target in range(G.number_of_nodes()):
        G=create_objective(G,args.target)

    print(f"n={G.number_of_nodes()}")
    print(f"m={G.number_of_edges()}")
    #nx.draw(G)
    #plt.show()

    distances = nx.floyd_warshall_numpy(G,sorted(G.nodes))
    node_labels = nx.get_node_attributes(G, 'objective')
    target_node = min(node_labels,key=node_labels.get)


    #Specify algorithm

    stats = binary_search(G, distances)

    # Analysis
    target_sets = [iteration[0] for iteration in stats]
    for i in range(1,len(stats)):
        if len(target_sets[i])*2>len(target_sets[i-1]):
            print(f"No halving in iteration {i}")
    assert target_sets[-1][0]==target_node, "Wrong node found as target"

    # Plots
    if len(instances)<5 and args.plots:
        plot_node_positions = nx.kamada_kawai_layout(G)
        for iteration in stats:
            S,selected_node,centroid = iteration
            plot_iteration(G,S,plot_node_positions,target_node,selected_node,node_ids=True)
# %%
