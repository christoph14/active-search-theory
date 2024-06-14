import networkx as nx
import numpy as np
import pickle

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
            if len(values)!=len(set(values)):
                print("some path has non unique node labels:", path)
                return False
    if len(set(f[v] for v in G.nodes))<G.number_of_nodes():
        print("Node labels are not unique")
        return False
    return True

def create_objective(G,target_node=None):
    n=G.number_of_nodes()
    if target_node==None:
        target_node = np.random.randint(0,n)
    print(f"Selected target node {target_node}")
    offset = [0 for _ in range(n)]
    f = dict()
    for node in G.nodes:
        dist = nx.shortest_path_length(G, target_node, node)
        f[node] = dist*n + offset[dist]
        offset[dist]+=1
    nx.set_node_attributes(G, f, 'objective')
    return G

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

def write_graph(G,file):
    with open(file,"wb") as f:
        pickle.dump(G,f)
def read_graph(file):
    if file.endswith(".pickle"):
        with open(file,"rb") as f:
            G=pickle.load(f)
    elif file.endswith(".s6"):
        with open(file,"rb") as f:
            G=nx.sparse6.from_sparse6_bytes(f.read())
    else:
        raise Exception("Non supported file format")
    if 'objective' not in G[0]:
        print("No node labels. Creating node labels")
        G=create_objective(G)
    assert check_objective_function(G), "Error: Objective function is not convex."
    return G