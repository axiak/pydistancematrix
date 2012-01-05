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

    outside_matrix = set()

    while any(len(x) > limit for x in result):
        bad_idx = [i for i, x in enumerate(result) if len(x) > limit][0]
        bad_nodes = result.pop(bad_idx)

        partitions = partition_nodes(graph, bad_nodes, limit)

        for nodes in partitions:
            node_set = set(nodes)
            for node in nodes:
                for other_node in graph[node]:
                    if other_node not in node_set:
                        outside_matrix.add(tuple(sorted((node, other_node))))

        result.extend(partitions)

    return result, sorted(list(outside_matrix))


def partition_nodes(graph, node_list, limit):
    if len(node_list) - limit < 4 and len(node_list) / float(limit) < 1.10:
        return simple_partition(graph, node_list, limit)
    else:
        return pymetis_partition(graph, node_list, limit)

def simple_partition(graph, node_list, limit):
    node_connection_list = [(len(graph[node]), node)
                            for node in node_list]
    node_connection_list.sort()
    result = [node_list]
    for i in range(len(node_list) - limit):
        result.append([node_connection_list[i][1]])
        node_list.remove(node_connection_list[i][1])
    return result

def pymetis_partition(graph, node_list, limit):
    node_set = set(node_list)
    node_map = dict((node, i) for i, node in enumerate(node_list))
    adj_lists = dict((node_map[node], list(node_map[other_node]
                                           for other_node in node_set & set(graph[node].keys())))
                     for node in node_list)
    from pymetis import part_graph

    cuts, part_vert = part_graph(2, adj_lists)
    results = [[] for _ in range(max(part_vert) + 1)]
    node_map_rev = dict((v, k) for k, v in node_map.items())

    for node_idx, partition in enumerate(part_vert):
        results[partition].append(node_map_rev[node_idx])

    return results
