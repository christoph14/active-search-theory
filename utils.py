import networkx as nx
import numpy as np
import os
import pickle
import logging

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
    if target_node==None or target_node not in range(n):
        target_node = list(G.nodes())[np.random.randint(0,n)]
    logging.info(f"Selected target node {target_node}")
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
def read_graph(instance):
    name,string,format = instance
    if format=="pickle-file":
        with open(string,"rb") as f:
            G=pickle.load(f)
    elif format=="s6-file":
        with open(string,"rb") as f:
            G=nx.from_sparse6_bytes(f.readline())
    elif format=="s6-bytes":
        G=nx.from_sparse6_bytes(string)
    elif format=="g6-bytes":
        G=nx.from_graph6_bytes(string)
    else:
        raise Exception("Non supported file format")
    if 'objective' in G[0]:
        assert check_objective_function(G), "Error: Objective function is not convex."
    assert list(G.nodes())==list(range(G.number_of_nodes())), "Error: We need node names to match ids"
    return G

def extract_instances(filepath, linenumber=None):
    instances=[]
    if filepath.endswith(".pickle"):
        instances.append([filepath,filepath,"pickle-file"])
    if filepath.endswith(".s6"):
        with open(filepath,"rb") as f:
            for i,line in enumerate(f.readlines()):
                instances.append([f"{filepath}:{i}",line[:-1],"s6-bytes"])
    if filepath.endswith(".g6"):
        with open(filepath,"rb") as f:
            for i,line in enumerate(f.readlines()):
                instances.append([f"{filepath}:{i}",line[:-1],"g6-bytes"])
    if linenumber != None:
        return [instances[int(linenumber)]]
    return instances


def collect_instances(path):
    instances = []
    if os.path.isdir(path):
        directory = os.fsencode(path)    
        for file in sorted(os.listdir(directory)):
            filename = os.fsdecode(file)            
            filepath = os.path.join(path, filename)
            instances += extract_instances(filepath)
        return instances
    if ":" in path:
        path,linenumber=path.split(":")
        return extract_instances(path,linenumber)
    return extract_instances(path)