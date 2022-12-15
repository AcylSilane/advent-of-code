from __future__ import annotations
import sys, os
import string

import numpy as np

os.system("cls")
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)
RIGHT = np.array([0, 1])
LEFT = np.array([0, -1])
DOWN = np.array([1, 0])
UP = np.array([-1, 0])


class Node:
    def __init__(self, position: np.array, cost: int, end_position: np.array, heightmap: np.array, parent=None):
        self.position = position
        self.height = heightmap[tuple(self.position)]
        self.cost = cost
        self.end_position = end_position
        self.parent = parent

    def __repr__(self):
        return f"<Node at {id(self)}, x={self.x}, y={self.y}, z={self.z}, total_cost={self.total_cost}>"

    def __eq__(self, other: Node):
        if isinstance(other, Node):
            return all(self.position == other.position)
        else:
            return False

    @property
    def x(self) -> int:
        return self.position[1]

    @property
    def y(self) -> int:
        return self.position[0]

    @property
    def z(self) -> int:
        return ord(self.height)

    @property
    def distance_to_end(self) -> float:
        return np.linalg.norm(self.end_position - self.position)

    def total_cost(self, problem_part: str) -> float:
        if problem_part == "1":
            total_cost = self.cost + self.distance_to_end
        elif problem_part == "2":
            total_cost = self.cost
        return total_cost

    def is_end_node(self, problem_part: str) -> bool:
        if problem_part == "1":
            result = all(self.position == self.end_position)
        elif problem_part == "2":
            result = self.height == "a"
        return result

    def is_neighbor(self, other: Node, problem_part: str) -> bool:
        is_adjacent = (np.linalg.norm(self.position - other.position) == 1) and (other.x >= 0 and other.y >= 0)
        if problem_part == "1":
            is_traversable = (other.z - self.z) <= 1
        elif problem_part == "2":
            is_traversable = (other.z - self.z) >= -1
        return is_adjacent and is_traversable

def draw_current_stage(count, heightmap, closed_nodes, open_nodes):
    print("\033[1;1H")
    print(f"Iter {count}")
    modified_heightmap = heightmap.copy()
    for node in closed_nodes:
        modified_heightmap[node.y, node.x] = "#"
    for node in open_nodes:
        modified_heightmap[node.y, node.x] = "_"
    if open_nodes:
        modified_heightmap[open_nodes[-1].y, open_nodes[-1].x] = "@"
    for row in modified_heightmap:
        print("".join(row))

if __name__ == "__main__":
    with open("input.txt") as inp:
        data = inp.read()
    heightmap = np.array([list(line) for line in data.split()], dtype=str)

    chosen_anim = None
    print("Dear user, do you want Part 1, or Part 2?")
    while not chosen_anim:
        chosen_anim = input(" Please enter 1 or 2: >")
        if chosen_anim not in "12":
            print("No seriously, just press 1 or 2 and then enter.")
            chosen_anim = None
    os.system("cls")


    start_char = "S"
    end_char = "E"
    start_height = "a"
    end_height = "z"
    if chosen_anim == "2":
        start_char, end_char = end_char, start_char
        start_height, end_height = end_height, start_height
    start_y, start_x = np.array(np.where(heightmap == start_char)).ravel()
    end_y, end_x = np.array(np.where(heightmap == end_char)).ravel()



    for y, x, replacement_char in ((start_y, start_x, start_height), (end_y, end_x, end_height)):
        heightmap[y, x] = replacement_char

    start_position = np.array([start_y, start_x])
    end_position = np.array([end_y, end_x])
    start_node = Node(position=start_position,
                      cost=0,
                      end_position=end_position,
                      heightmap=heightmap)

    open_nodes = [start_node]
    closed_nodes = []
    is_complete = False
    count = 0
    while open_nodes:
        count += 1

        # End condition check
        current_node = open_nodes.pop()
        closed_nodes.append(current_node)

        if current_node.is_end_node(problem_part=chosen_anim):
            is_complete = True
            break

        # Build list of neighbors
        for direction in (LEFT, RIGHT, UP, DOWN):
            new_position = current_node.position + direction
            if any(new_position == heightmap.shape):
                continue
            other_node = Node(position=new_position,
                              cost=current_node.cost + 1,
                              end_position=end_position,
                              heightmap=heightmap,
                              parent=current_node)
            if current_node.is_neighbor(other_node, problem_part=chosen_anim):
                if other_node not in (open_nodes + closed_nodes):
                    open_nodes.append(other_node)
                elif other_node in open_nodes:
                    true_node = open_nodes[open_nodes.index(other_node)]
                    true_node.cost = min(true_node.cost, other_node.cost)

        # Set up for next iteration
        open_nodes = sorted(open_nodes, key=lambda node: -node.total_cost(problem_part=chosen_anim))

        # Draw that animation!
        draw_current_stage(count=count, heightmap=heightmap, closed_nodes=closed_nodes, open_nodes=open_nodes)





    if is_complete:
        modified_heightmap = heightmap.copy()
        end_node = closed_nodes[-1]
        current_node = end_node.parent
        parent = current_node.parent

        pathlength = 1
        while parent:
            pathlength += 1
            print("\033[1;1H")
            print(f"Number of iterations: {count}, final path length={pathlength}")
            modified_heightmap[current_node.y, current_node.x] = "░"
            for row in modified_heightmap:
                print("".join(row))
            current_node = parent
            parent = current_node.parent

