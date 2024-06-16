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
    logging.debug(f"Selected target node {target_node}")
    offset = [0 for _ in range(n)]
    f = dict()
    for node in G.nodes:
        dist = nx.shortest_path_length(G, target_node, node)
        f[node] = dist*n + offset[dist]
        offset[dist]+=1
    nx.set_node_attributes(G, f, 'objective')
    return G

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