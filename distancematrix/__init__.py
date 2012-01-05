__version__ = (0, 0, 1)

import networkx as nx

__all__ = (
    'matrix_calls',
    )


def matrix_calls(pairs, limit=None):
    """
    Given an iterable of pairs (e.g. origin to destination),
    this function will yield individual groups of locations
    that are separated from each other.
    """
    graph = nx.Graph()
    for orig, dest in pairs:
        graph.add_edge(orig, dest)

    result = nx.connected_components(graph)
    if not isinstance(result, list):
        result = list(result)
    if limit is None or not any(len(x) > limit for x in result):
        return result, []

    from pymetis import part_graph
    outside_matrix = []

    while any(len(x) > limit for x in result):
        bad_idx = [i for i, x in enumerate(result) if len(x) > limit][0]
        bad_nodes = result.pop(bad_idx)
        bad_nodes_set = set(bad_nodes)
        adj_list = dict((node, list(bad_nodes_set & set(graph[node].keys())))
                        for node in bad_nodes)

        cuts, part_vert = part_graph(2, adj_list)
        graph_1_nodes = set(bad_nodes[i] for i, x in enumerate(bad_nodes)
                            if part_vert[i] == 0)

        graph_2_nodes = set(bad_nodes[i] for i, x in enumerate(bad_nodes)
                            if part_vert[i] == 1)

        for node_set in (graph_1_nodes, graph_2_nodes):
            for node in node_set:
                for other_node in graph[node]:
                    if other_node not in node_set:
                        outside_matrix.append((node, other_node))

        result.append(list(graph_1_nodes))
        result.append(list(graph_2_nodes))

    return result, outside_matrix
