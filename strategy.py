import networkx as nx
import numpy as np

from utils import centroid
from visualization import plot_feasible


def random_selection(_, t):
    rng = np.random.default_rng()
    all_nodes = np.array(list(t.keys()))
    unknown_nodes = all_nodes[np.isnan(list(t.values()))]
    return rng.choice(unknown_nodes)


def binary_search(G, t, f, plot=False, pos=None):
    # Precompute all distances
    distances = nx.floyd_warshall_numpy(G)

    # Initialize relevant nodes
    S = list(G.nodes)

    rng = np.random.default_rng(16)  # choose right neighbor, TODO change

    while len(S) > 1:
        # S_copy = S.copy()
        print(f"{len(S)} nodes remaining")
        c = centroid(G, S, distances)
        S_minus_all = []

        # Plot graph
        if plot:
            plot_feasible(G, S, c=c, pos=pos)

        # Sets for testing
        remove = []
        keep = S.copy()

        t[c] = f[c]
        end = True
        for v in nx.neighbors(G, c):
            t[v] = f[v]
            center_dist = nx.shortest_path_length(G, c)
            neighb_dist = nx.shortest_path_length(G, v)

            S_minus = [u for u in S if neighb_dist[u] > center_dist[u]]
            S_plus = [u for u in S if neighb_dist[u] < center_dist[u]]
            S_equals = [u for u in S if neighb_dist[u] == center_dist[u]]
            # print("|S^=| =", len([u for u in G.nodes if b[u] == a[u]]))
            if t[v] > t[c]:
                # Remove S^+
                remove = np.union1d(remove, S_plus)
                keep = np.setdiff1d(keep, S_plus)
                nodes = S_plus
            elif t[v] <= t[c]:
                # Remove S^-
                nodes = S_minus
                remove = np.union1d(remove, S_minus)
                keep = np.setdiff1d(keep, S_minus)
                S_minus_all.extend(S_minus)
                # S_plus = np.union1d(S_plus, [u for u in S_copy if neighb_dist[u] < center_dist[u]])
                # S_minus = np.union1d(S_minus, [u for u in S_copy if neighb_dist[u] > center_dist[u]])
                end = False
            else:
                nodes = []
            S = np.setdiff1d(S, nodes)
        print(f"|remove| = {len(set(remove))}, |keep| = {len(set(keep))}")
        if end:
            return c
        # print(f"Nodes in the intersection of all S^=: {all_equals}")
    assert len(S) == 1, "No remaining nodes!"
    return S[0]


def binary_search_neighbor(G, t, f, plot=False, pos=None):
    # Precompute all distances
    distances = nx.floyd_warshall_numpy(G)

    # Initialize relevant nodes
    S = list(G.nodes)

    rng = np.random.default_rng(16)  # choose right neighbor, TODO change

    select_center = True
    while len(S) > 1:
        # S_copy = S.copy()
        print(f"{len(S)} nodes remaining")
        if select_center:
            c = centroid(G, S, distances)
            select_center = False
        else:
            old_center = c
            neighbor_candidates = list(filter(lambda v: f[v] < f[old_center], G.neighbors(old_center)))
            c = rng.choice(neighbor_candidates)
            select_center = True
        S_minus_all = []

        # Plot graph
        if plot:
            plot_feasible(G, S, c=c, pos=pos)

        # Sets for testing
        remove = []
        keep = S.copy()

        t[c] = f[c]
        end = True
        for v in nx.neighbors(G, c):
            t[v] = f[v]
            center_dist = nx.shortest_path_length(G, c)
            neighb_dist = nx.shortest_path_length(G, v)

            S_minus = [u for u in S if neighb_dist[u] > center_dist[u]]
            S_plus = [u for u in S if neighb_dist[u] < center_dist[u]]
            S_equals = [u for u in S if neighb_dist[u] == center_dist[u]]
            # print("|S^=| =", len([u for u in G.nodes if b[u] == a[u]]))
            if t[v] > t[c]:
                # Remove S^+
                remove = np.union1d(remove, S_plus)
                keep = np.setdiff1d(keep, S_plus)
                nodes = S_plus
            elif t[v] <= t[c]:
                # Remove S^-
                nodes = S_minus
                remove = np.union1d(remove, S_minus)
                keep = np.setdiff1d(keep, S_minus)
                S_minus_all.extend(S_minus)
                # S_plus = np.union1d(S_plus, [u for u in S_copy if neighb_dist[u] < center_dist[u]])
                # S_minus = np.union1d(S_minus, [u for u in S_copy if neighb_dist[u] > center_dist[u]])
                end = False
            else:
                nodes = []
            S = np.setdiff1d(S, nodes)
        print(f"|remove| = {len(set(remove))}, |keep| = {len(set(keep))}")
        if end:
            return c
        # print(f"Nodes in the intersection of all S^=: {all_equals}")
    assert len(S) == 1, "No remaining nodes!"
    return S[0]
