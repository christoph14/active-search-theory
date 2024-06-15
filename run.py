# %%
import sys
import os
from matplotlib import pyplot as plt
import networkx as nx
from strategy import binary_search
from utils import collect_instances, create_objective, read_graph
from visualization import plot_iteration
from argparse import ArgumentParser
import logging

# %%
# Parse arguments

parser = ArgumentParser()
parser.add_argument("path",help="input graph or folder of graphs", default="data/Petersen.pickle")
parser.add_argument("--plots",action="store_true",dest="plots", help="generates an instance from every graph and every node as target")
parser.add_argument("-t","--target",type=int,help="node index to be used as target. Generates new labels.")
parser.add_argument('-v', '--verbose',help="verbose logging",action="store_const", dest="loglevel", const=logging.INFO,
)
args = parser.parse_args()
logging.basicConfig(level=args.loglevel,format='%(message)s')

instances = collect_instances(args.path)

# %%
for instance in instances:
    logging.info(f"\nInstance: {instance[0]}")
    G=read_graph(instance)
    if args.target in range(G.number_of_nodes()) or 'objective' not in G[0]:
        G=create_objective(G,args.target)

    logging.info(f"n={G.number_of_nodes()}")
    logging.info(f"m={G.number_of_edges()}")
    #nx.draw(G)
    #plt.show()

    distances = nx.floyd_warshall_numpy(G,sorted(G.nodes))
    node_labels = nx.get_node_attributes(G, 'objective')
    target_node = min(node_labels,key=node_labels.get)


    #Specify algorithm

    stats = binary_search(G, distances)

    # Analysis
    target_sets = [iteration[0] for iteration in stats]
    assert target_sets[-1][0]==target_node, "Wrong node found as target"
    no_halving = [i for i in range(1,len(stats)) if len(target_sets[i])*2>len(target_sets[i-1])]
    total_queries = stats[-1][3]
    logging.info(f"Binary Search took {len(stats)-1} iterations. Number of nodes queried: {len(total_queries):>2}/{G.number_of_nodes()}  ({100*len(total_queries)/G.number_of_nodes():>3.0f}%)")
    logging.info(f"No halving in these {len(no_halving)} iterations: {no_halving}")

    #if len(total_queries)/G.number_of_nodes() > 0.5 or len(no_halving)>5:
    if len(no_halving)>0:
        logging.warning(f"\nInstance: {instance[0]}")
        logging.warning(f"Binary Search took {len(stats)-1} iterations. Number of nodes queried: {len(total_queries):>2}/{G.number_of_nodes()}  ({100*len(total_queries)/G.number_of_nodes():>3.0f}%)")
        logging.warning(f"No halving in these {len(no_halving)} iterations: {no_halving}")

    # Plots
    if len(instances)<5 and args.plots:
        plot_node_positions = nx.kamada_kawai_layout(G)
        for iteration in stats:
            S,selected_node,centroid,_ = iteration
            plot_iteration(G,S,plot_node_positions,target_node,selected_node,node_ids=True)
# %%
