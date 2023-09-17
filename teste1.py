import networkx as nx
import solving_algorithms
from networkx.algorithms import approximation


f = open("datasets/test2(20).txt", "r")
max_nodes = int(f.readline().rstrip())
max_edges = int(f.readline().rstrip())

print(max_nodes, "nodes")
print(max_edges, "edges")

# create weighted edges
G = nx.Graph()

for i in range(1, max_edges + 1):
    edge = f.readline().rstrip().split(" ")
    G.add_edge(int(edge[1]), int(edge[2]), weight=int(edge[3]))

# create terminal nodes list
max_terminals = int(f.readline().rstrip())
terminal_list = []
for i in range(1, max_terminals + 1):
    terminal = f.readline().rstrip().split(" ")
    terminal_list.append(int(terminal[1]))

print("Terminal nodes:", terminal_list)

# close file
f.close()

terminal_list = [2, 6, 5]

steiner_tree = approximation.steiner_tree(G, terminal_list, method='mehlhorn')

print(terminal_list)
print(steiner_tree.nodes)
print(steiner_tree.degree[2])