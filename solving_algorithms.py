import itertools
import networkx as nx
from networkx.algorithms.approximation import steiner_tree
# from networkx.algorithms import approximation.steiner_tree
# from approximation import steiner_tree


def solve(G, terminals, algorithm):
    if algorithm == "brute_force":
        return brute_force_steiner_tree(G, terminals)
    elif algorithm == "melhorn":
        return steiner_tree(G, terminals, method='mehlhorn')
    elif algorithm == "kou":
        return steiner_tree(G, terminals, method='kou')
    else:
        raise ValueError("Algorithm not found.")


def is_steiner_tree(subgraph, terminals):
    return set(terminals).issubset(subgraph.nodes)


def brute_force_steiner_tree(graph, terminals):
    # Initialize variables to store the best tree and its weight.
    best_tree = None
    best_weight = float('inf')

    # Generate all possible subsets of nodes in the graph.
    all_nodes = set(graph.nodes)
    for subset_size in range(len(terminals), len(all_nodes) + 1):
        for node_subset in itertools.combinations(all_nodes, subset_size):
            # Create a subgraph containing the current node subset.
            subgraph = graph.subgraph(node_subset)
            subgraph = nx.minimum_spanning_tree(subgraph)

            # Check if the subgraph is connected and contains all terminals.
            if not nx.is_connected(subgraph) or not is_steiner_tree(subgraph, terminals):
                continue

            # Calculate the total weight of the subgraph.
            total_weight = sum(graph[u][v]['weight'] for u, v in subgraph.edges)

            # Check if this subgraph is better than the current best.
            if total_weight < best_weight:
                best_tree = subgraph
                best_weight = total_weight

    if best_tree is None:
        raise ValueError("No Steiner tree found for the given terminals.")

    return best_tree
