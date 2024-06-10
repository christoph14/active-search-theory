import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from utils import centroid


def plot_feasible(G, S, c=None, pos=None):
    # Highlight target
    f = nx.get_node_attributes(G, 'objective')
    target_node = min(f, key=f.get)
    fixed = pos.keys() if pos is not None else None
    pos = nx.spring_layout(G, seed=22, pos=pos, fixed=fixed)
    nx.draw_networkx(G.subgraph(target_node), pos=pos, node_size=400, node_color='red')

    # Highlight centroid
    c = centroid(G, S) if c is None else c
    nx.draw_networkx(G.subgraph(c), pos=pos, node_size=350, node_color='yellow')

    colors = np.array(['#1f78b4'] * nx.number_of_nodes(G))
    colors[S] = 'g'
    nx.draw(G, with_labels=True, node_color=colors, font_weight='bold', pos=pos)
    plt.show()
