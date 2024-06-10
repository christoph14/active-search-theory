import networkx as nx
import numpy as np

from utils import centroid

# Iteratively select a node and query its and its neighbors values.
# Then disregard nodes which cant be target.
# Specify wwhat information is used to determine non-target nodes (deletion_effort):
#  - incident edges:    Consider all edges incident to the center/selected node
#  - triangles:         + Consider edges forming triangles between neighbors of c
#  - neighbors_pairs:   + Consider all shortest paths betwen all pairs of neighbors
def binary_search(G, distances, deletion_effort="incident_edges"):
    f = nx.get_node_attributes(G, 'objective')
    stats = []
    queries = {} #to make sure we do not use unknown labels

    # Initialize relevant nodes
    S = list(G.nodes)
    while len(S) > 1:
        print(f"{len(S)} nodes remaining")
        c = centroid(G, S, distances)

        stats.append([S,c])

        # Sets for testing
        remove = []

        queries[c] = f[c]
        for v in nx.neighbors(G, c):
            queries[v] = f[v]

            S_minus = [u for u in S if distances[u][v] > distances[u][c]]
            S_plus = [u for u in S if distances[u][v] < distances[u][c]]
            S_equals = [u for u in S if distances[u][v] == distances[u][c]]
            #print(f"S- of ({c},{v}) {S_minus}")
            #print(f"S+ of ({c},{v}) {S_plus}")
            # print("|S^=| =", len([u for u in G.nodes if b[u] == a[u]]))
            if queries[v] > queries[c]:
                # Remove S^+
                remove += S_plus
            elif queries[v] <= queries[c]:
                # Remove S^-
                remove += S_minus

        len_S = len(S)
        S= [x for x in S if x not in remove]
        print(f"removed {len_S-len(S):>3} nodes which is {100*(len_S-len(S))/len_S:>3.0f}% of S")
    print(f"\nNumber of nodes queried: {len(queries)}/{G.number_of_nodes()}")
    return stats
