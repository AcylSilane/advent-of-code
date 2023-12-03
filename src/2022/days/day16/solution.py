from typing import Tuple, List, TextIO

from functools import cache
import itertools

import re
import tqdm
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def graph_from_input(file: TextIO) -> nx.DiGraph:
    graph = nx.Graph()
    edges = {}

    for line in file:
        name, flow_rate, connections = parse_lines(line)
        edges[name] = connections
        graph.add_node(name, flow_rate=flow_rate)
    for source, destinations in edges.items():
        for destination in destinations:
            graph.add_edge(source, destination)
    return graph


def parse_lines(line: str) -> Tuple[str, int, List[str]]:
    regex = r"(?<=Valve\s)(\w+)|(?<=rate=)(\d+)|(?<=valve)s?\s+(.+?)$"
    raw_name, raw_flow_rate, raw_connections = re.findall(regex, line)
    name = raw_name[0]
    flow_rate = int(raw_flow_rate[1])
    raw_connections = raw_connections[2].split(", ")
    return name, flow_rate, raw_connections


def find_one_way_nodes(graph):
    """Checks for the presence of any one-way edges on the graph; not actually used, but was
    useful when examining the problem statement's graph"""
    unidirectional = []
    for node in graph:
        neighbors = [*graph.neighbors(node)]
        for neighbor in neighbors:
            if node not in graph.neighbors(neighbor):
                unidirectional.append(f"{node}->{neighbor}")
    return unidirectional


def draw_weighted_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos=pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=edge_labels)
    plt.show()


@cache
def get_best_path(current_node, remaining_time, visited_nodes) -> int:
    if remaining_time <= 0:
        return 0

    hi_score = 0
    neighbors = list(full_graph.neighbors(current_node))

    # Branch to ignore the node
    for neighbor in neighbors:
        hi_score = max(hi_score, get_best_path(neighbor, remaining_time - 1, visited_nodes))

    # Branch to release pressure on the node
    rate = flow_rates[current_node]
    if (rate > 0) and (current_node not in visited_nodes):
        visited_nodes = set(visited_nodes)
        visited_nodes.add(current_node)
        score = rate * (remaining_time - 1)
        for neighbor in neighbors:
            hi_score = max(hi_score, score + get_best_path(neighbor, remaining_time - 2, frozenset(visited_nodes)))

    return hi_score


if __name__ == "__main__":
    with open("input.txt", "r") as inp:
        full_graph = graph_from_input(inp)
    flow_rates = nx.get_node_attributes(full_graph, "flow_rate")


    # There are 15 usable nodes, so only 2^15 possible combinations between the human / elephant
    # Because the cache size is unbounded, could take up a lot of ram. On my machine, this chews up
    # about 8.3GB of RAM. If you've got a RAM limitation, you can always cap the size of the functools cache being
    # used to lower memory consumption in exchange for speed.
    useful_nodes = np.array([node for node, rate in flow_rates.items() if rate > 0])
    n_useful = len(useful_nodes)
    masks = map(lambda i: np.array(i, dtype=bool), itertools.product([0, 1], repeat=n_useful))
    best_score = 0
    for mask in tqdm.tqdm(masks, total=2**n_useful):
        human_visited = frozenset(useful_nodes[mask])
        elephant_visited = frozenset(useful_nodes[~mask])

        human_score = get_best_path(current_node="AA", remaining_time=26, visited_nodes=elephant_visited)
        elephant_score = get_best_path(current_node="AA", remaining_time=26, visited_nodes=human_visited)
        best_score = max(best_score, elephant_score + human_score)

    print(f"Part 1: {get_best_path(current_node='AA', remaining_time=30, visited_nodes=frozenset())}")
    print(f"Part 2: {best_score}")
