import itertools
import networkx as nx
from networkx.algorithms.approximation import steiner_tree
from networkx.utils import pairwise


def solve(G, terminals, algorithm):
    if algorithm == "exact":
        return brute_force_steiner_tree(G, terminals)
    elif algorithm == "approximation":
        edges = kou_steiner_tree(G, terminals)
        if G.is_multigraph():
            edges = (
                (u, v, min(G[u][v], key=lambda k: G[u][v][k][weight])) for u, v in edges
            )
        return G.edge_subgraph(edges)
    else:
        raise ValueError("Algorithm not found.")


def is_steiner_tree(subgraph, terminals):
    return set(terminals).issubset(subgraph.nodes)


def brute_force_steiner_tree(graph, terminals):
    # initialize variables to store the best tree and its weight.
    best_tree = None
    best_weight = float('inf')

    # generate all possible subsets of nodes in the graph.
    all_nodes = set(graph.nodes)
    for subset_size in range(len(terminals), len(all_nodes) + 1):
        for node_subset in itertools.combinations(all_nodes, subset_size):
            # create a subgraph containing the current node subset.
            subgraph = graph.subgraph(node_subset)
            subgraph = nx.minimum_spanning_tree(subgraph)

            # check if the subgraph is connected and contains all terminals.
            if not nx.is_connected(subgraph) or not is_steiner_tree(subgraph, terminals):
                continue

            # calculate the total weight of the subgraph.
            total_weight = sum(graph[u][v]['weight'] for u, v in subgraph.edges)

            # check if this subgraph is better than the current best.
            if total_weight < best_weight:
                best_tree = subgraph
                best_weight = total_weight

    if best_tree is None:
        raise ValueError("No Steiner tree found for the given terminals.")

    return best_tree


def kou_steiner_tree(graph, terminals, weight="weight", metric_closure=None, mst_H=None):
    if metric_closure is None:
        metric_closure = compute_metric_closure(graph, weight)

    if mst_H is None:
        mst_H = compute_minimum_spanning_tree(metric_closure, terminals)

    # convert the generator of edges to a list
    mst_H_edges = list(mst_H)

    subgraph_S = graph.edge_subgraph(mst_H_edges)
    mst_S = nx.minimum_spanning_edges(subgraph_S, weight=weight, data=False)

    steiner_tree = graph.edge_subgraph(mst_S).copy()
    prune_nonterminal_leaves(steiner_tree, terminals)

    return steiner_tree.edges()


def prune_nonterminal_leaves(graph, terminals):
    terminal_nodes = set(terminals)
    for node in list(graph.nodes):
        if node not in terminal_nodes and graph.degree(node) == 1:
            graph.remove_node(node)


def compute_metric_closure(graph, weight="weight"):
    metric_closure = nx.Graph()
    nodes = set(graph.nodes)

    # ensure the graph is connected while processing the first node
    all_paths_iter = nx.all_pairs_dijkstra(graph, weight=weight)
    u, (distance, path) = next(all_paths_iter)
    if nodes - set(distance):
        msg = "The graph is not connected; the metric_closure cannot be defined."
        raise nx.NetworkXError(msg)
    nodes.remove(u)
    for v in nodes:
        metric_closure.add_edge(u, v, distance=distance[v], path=path[v])

    # process the remaining nodes
    for u, (distance, path) in all_paths_iter:
        nodes.remove(u)
        for v in nodes:
            metric_closure.add_edge(u, v, distance=distance[v], path=path[v])

    return metric_closure


def compute_minimum_spanning_tree(graph, terminals, weight="weight"):
    terminal_subgraph = graph.subgraph(terminals)
    mst_edges = nx.minimum_spanning_edges(terminal_subgraph, weight="distance", data=True)
    all_mst_edges = itertools.chain.from_iterable(pairwise(d["path"]) for u, v, d in mst_edges)
    if graph.is_multigraph():
        all_mst_edges = (
            (u, v, min(graph[u][v], key=lambda k: graph[u][v][k][weight]))
            for u, v in all_mst_edges
        )
    subgraph_S = graph.edge_subgraph(all_mst_edges)
    mst_S = nx.minimum_spanning_edges(subgraph_S, weight=weight, data=False)
    return mst_S

