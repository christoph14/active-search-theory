import networkx as nx
import numpy as np


def rule_out_nodes_based_on_edge(G,S,distances,e,queries):
    low,high=e
    if queries[low]>queries[high]:
        high,low=e
    S_minus = [u for u in S if distances[u][high] < distances[u][low]]
    # S_plus = [u for u in S if distances[u][low] > distances[u][high]]
    # S_equals = [u for u in S if distances[u][v] == distances[u][c]]
    #print(f"S- of ({c},{v}) {S_minus}")
    #print(f"S+ of ({c},{v}) {S_plus}")

    return S_minus

# Iteratively select a node and query its and its neighbors values.
# Then disregard nodes which cant be target.
# Specify what information is used to determine non-target nodes (deletion_effort):
#  - incident edges:    Consider all edges incident to the center/selected node
#  - triangles:         + Consider edges forming triangles between neighbors of c
# Specify which node is selected (pivot):
#  - centroid:          Vertex minimizing summed distance to remaining targets
#  - best-worst-case    Vertex maximizing possible node deletions over all possible labelings
def binary_search(G, distances, pivot="centroid", deletion_effort="incident_edges"):
    f = nx.get_node_attributes(G, 'objective')
    target_node = min(f,key=f.get)
    stats = []
    queries = {} #to make sure we do not use unknown labels

    # Initialize relevant nodes
    S = list(G.nodes)
    while len(S) > 1:
        print(f"{len(S)} nodes remaining")

        # choose centroid:
        #  among nodes with non-queried label choose the one with highest label (assuming worst case)
        #  if all centroids are queried choose the one with minimum label (probably cannot happen)
        centroids = centroid(G, S, distances,return_all=True)
        c = centroids[np.argmax([f[v] if v not in queries else -f[v] for v in centroids])] 
        c = centroids[np.argmax([f[v] for v in centroids])] 
        print(f"Centroid of size {len(centroids)}. Choosing node {c}. {"Label of c is already known." if c in queries else ""} {"Target in Centroid." if target_node in centroids else ""}")
        print(centroids)
        stats.append([S,c,centroids])
        old_len_S = len(S)

        queries[c] = f[c]
        for v in nx.neighbors(G, c):
            queries[v] = f[v]
        if queries[c]==min(list(queries.values())):
            S=[c]

        ruled_out = []
        for v in nx.neighbors(G,c):
            ruled_out += rule_out_nodes_based_on_edge(G,S,distances,(c,v),queries)
            if deletion_effort=="triangles":
                for w in nx.common_neighbors(G,c,v):
                    ruled_out+=rule_out_nodes_based_on_edge(G,S,distances,(v,w),queries)
        S= [x for x in S if x not in ruled_out]
        if len(ruled_out)==0 and len(S)>1:
            raise Exception("No nodes were ruled out.")
        print(f"ruled out {old_len_S-len(S):>3} nodes which is {100*(old_len_S-len(S))/old_len_S:>3.0f}% of S")
    print(f"Number of nodes queried: {len(queries)}/{G.number_of_nodes()}  ({100*len(queries)/G.number_of_nodes():>3.0f}%)")
    stats.append([S,None,None])
    return stats


def centroid(G, S, distances=None, return_all=False):
    if distances is None:
        distances = nx.floyd_warshall_numpy(G,sorted(G.nodes))
    if return_all:       
        c = np.where(np.sum(distances[S], axis=0) == np.sum(distances[S], axis=0).min())[0]
        #print(c)
        #print(np.sum(distances[S], axis=0))
    else:
        c = np.argmin(np.sum(distances[S], axis=0))
    return c
