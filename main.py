import networkx as nx
import matplotlib.pyplot as plt
from solving_algorithms import solve
from time import time

def plot_graph(G, terminal_list):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='b')
    nx.draw_networkx_nodes(G, pos, nodelist=terminal_list, node_size=700, node_color='r')
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    plt.show()


def create_graph(path):
    f = open(path, "r")
    optimal_cost = int(f.readline().rstrip())
    max_edges = int(f.readline().rstrip())

    # create weighted edges
    graph = nx.Graph()
    for i in range(1, max_edges + 1):
        edge = f.readline().rstrip().split(" ")
        graph.add_edge(int(edge[1]), int(edge[2]), weight=int(edge[3]))

    # create terminal nodes list
    max_terminals = int(f.readline().rstrip())
    terminal_list = []
    for i in range(1, max_terminals + 1):
        terminal = f.readline().rstrip().split(" ")
        terminal_list.append(int(terminal[1]))

    f.close()
    return graph, terminal_list, optimal_cost


G, terminals, optimal_cost = create_graph("datasets/PACE_TRACK_2/135(164009591).txt")

execution_time = []
algorithm = "kou"

for i in range(1):
    start_time = time()
    steiner_tree = solve(G, terminals, algorithm)
    end_time = time()
    execution_time.append(end_time - start_time)
total_weight = sum(steiner_tree[u][v]['weight'] for u, v in steiner_tree.edges)

average_time = sum(execution_time) / len(execution_time)

# plot a graph with the time of execution for each iteration
plt.plot(execution_time)
plt.ylabel('Time')
plt.xlabel('Iteration')
plt.show()

if algorithm == "kou":
    number_of_leaves = 0
    for node in steiner_tree.nodes:
        if steiner_tree.degree[node] == 1:
            number_of_leaves += 1
    print(number_of_leaves)
    approximation_ratio = 2 * (1 - 1 / number_of_leaves)

print("--------------------")
print("Average time:", average_time)
print("--------------------")
print(len(G.nodes), "nodes")
print(len(G.edges), "edges")
print(f"Terminal nodes {len(terminals)}: ", terminals)
print("--------------------")
print("Best Steiner Tree Edges:", steiner_tree.edges)
print("Total Weight:", total_weight)
print("Optimal Weight:", optimal_cost)
print("Approximation ratio:", total_weight/optimal_cost)
print("Max approximation ratio:", approximation_ratio)
print("Worst approximation case:", optimal_cost * approximation_ratio)



