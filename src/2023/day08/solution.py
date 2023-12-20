"""Solution for day 8"""
from __future__ import annotations
from typing import Dict
import math
import itertools
import functools


class Node:
    """A node in a graph"""

    def __init__(self, name):
        self.name = name
        self.children: Dict[str, Node] = {"L": None, "R": None, }
        self.parents = []

    @property
    def left(self) -> Node:
        return self.children["L"]

    @property
    def right(self) -> Node:
        return self.children["R"]

    def add_child(self, child: Node, side: str) -> Node:
        """Add a child node"""
        if self.children[side] is not None:
            raise ValueError(f"Node already has a child on the {side} side")
        self.children[side] = child
        child.add_parent(self)
        return self

    def add_parent(self, parent) -> Node:
        """Add a parent node"""
        self.parents.append(parent)
        return self

    def __repr__(self):
        return f"Node({self.name} = ({self.children['L'].name}, {self.children['R'].name}))"


def find_node(name: str, nodes: list[Node]) -> Node:
    """Find a node in a list of nodes"""
    for node in nodes:
        if node.name == name:
            return node
    raise ValueError(f"Node {name} not found")


def lcm(a: int, b: int) -> int:
    """Calculate the least common multiple of two numbers"""
    return abs(a * b) // math.gcd(a, b)


# ===========
# Parse Input
# ===========
node_inputs = {}
with open("input.txt", "r") as inp:
    directions = inp.readline().strip()
    inp.readline()  # skip a line
    for line in inp:
        split_line = line.strip().split()
        node_head = split_line[0]
        left_child = split_line[2][1:-1]
        right_child = split_line[3][:-1]
        node_inputs[node_head] = [left_child, right_child]

nodes = [Node(key) for key in node_inputs.keys()]
for parent in nodes:
    left, right = node_inputs[parent.name]
    for child in nodes:
        if child.name == left:
            parent.add_child(child, "L")
        if child.name == right:
            parent.add_child(child, "R")

# ======
# Part 1
# ======

current_node = find_node("AAA", nodes)
goal_node = find_node("ZZZ", nodes)

hops = 0
for direction in itertools.cycle(directions):
    if current_node == goal_node:
        break
    current_node = current_node.children[direction]
    hops += 1
print(f"Part 1: {hops}")

# ======
# Part 2
# ======

current_nodes = [node for node in nodes if node.name[-1] == "A"]
hops = [0] * len(current_nodes)
for direction in itertools.cycle(directions):
    if all(node.name.endswith("Z") for node in current_nodes):
        break
    for i, node in enumerate(current_nodes):
        if node.name.endswith("Z"):
            continue
        current_nodes[i] = node.children[direction]
        hops[i] += 1

print(f"Part 2: {functools.reduce(lcm, hops)}")
