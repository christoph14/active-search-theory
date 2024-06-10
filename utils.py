import networkx as nx
import numpy as np


def check_objective_function(G):
    f = nx.get_node_attributes(G, 'objective')
    target_node = min(f, key=f.get)
    # print("Target node:", target_node)

    for n in G.nodes:
        paths = nx.all_shortest_paths(G, source=n, target=target_node)
        for path in paths:
            values = [f[v] for v in path]
            if not values == sorted(values, reverse=True):
                # print(f"Path {path} with values {values} is not strictly decreasing.")
                return False
    return True


def create_objective_function_random(G, seed=None, max_iter=10000):
    if seed is None:
        rng = np.random.default_rng()
    elif isinstance(seed, int):
        rng = np.random.default_rng(seed)
    elif isinstance(seed, np.random.Generator):
        rng = seed
    else:
        raise TypeError("seed is not correct.")

    iterations = 0
    while iterations < max_iter:
        iterations += 1
        f = {node: value for (node, value) in zip(G.nodes, rng.random(nx.number_of_nodes(G)))}
        nx.set_node_attributes(G, f, 'objective')
        if check_objective_function(G):
            break
    raise ValueError(f"Could not create a valid objective function in {max_iter} iterations!")


def create_objective_function_star(G: nx.Graph, seed: object = None) -> dict:
    if seed is None:
        rng = np.random.default_rng()
    elif isinstance(seed, int):
        rng = np.random.default_rng(seed)
    elif isinstance(seed, np.random.Generator):
        rng = seed
    else:
        raise TypeError("seed is not correct.")
    target = rng.choice(list(G.nodes))
    f = {node: np.nan for node in G.nodes}
    distances = nx.shortest_path_length(G, source=target)
    d = 0
    while np.isnan(list(f.values())).any():
        selected_nodes = np.where(np.array(list(distances.values())) == d)[0]
        for node in np.array(list(distances.keys()))[selected_nodes]:
            f[node] = rng.random() + d
        d += 1
    return f


def centroid(G, S, distances=None, return_all=False):
    if distances is None:
        distances = nx.floyd_warshall_numpy(G)
    if return_all:
        c = np.where(np.sum(distances[S], axis=0) == np.sum(distances[S], axis=0).min())[0]
    else:
        c = np.argmin(np.sum(distances[S], axis=0))
    return c
