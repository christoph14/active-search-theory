import math
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


def plot_iteration(G,S,selected_node, target_node, node_positions, target_color=False, node_ids=False):
    f = nx.get_node_attributes(G, 'objective')

    cmap=LinearSegmentedColormap.from_list('rg',["g", "w", "r"], N=256) 

    # Highlight selection and target
    nx.draw(G.subgraph(selected_node), with_labels=False, pos=node_positions, node_size=400, node_color='yellow')
    nx.draw(G.subgraph(target_node), with_labels=False, pos=node_positions, node_size=400, node_color='red')

    if target_color or node_ids:
        colors = [f.get(node) for node in G.nodes()]
        if not node_ids:
            labels = {node: "S" if node in S else "" for node in G.nodes()}
            nx.draw(G, with_labels=True, labels=labels, node_color=colors, cmap=cmap, pos=node_positions)
        else:
            nx.draw(G, with_labels=True, node_color=colors, cmap=cmap, pos=node_positions)
    else:
        colors = ["green" if node in S else 'grey' for node in G.nodes()]
        labels = {node: math.floor(f.get(node)) for node in G.nodes()}
        nx.draw(G, with_labels=True, labels=labels, node_color=colors, font_weight='bold', pos=node_positions)
    
    plt.show()