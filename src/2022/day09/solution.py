"""Solution to Day 9"""
from __future__ import annotations
from typing import Literal
import numpy as np


def chebyshev_distance(point1: np.array, point2: np.array) -> int:
    """Returns the Chebychev distance between two points"""
    return np.abs(point2 - point1).max()


class Knot:
    def __init__(self):
        self.position = np.zeros(2, dtype=np.int32)  # X, Y
        self.visited_positions = set()
        self.subscribers = []

    def __repr__(self):
        return f"<Knot at {id(self)}, position={self.position}, subscribers={self.subscribers}"

    def register_subscriber(self, subscriber: Knot):
        self.subscribers.append(subscriber)

    @property
    def x(self) -> int:
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position[0] = value

    @property
    def y(self) -> int:
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position[1] = value

    def move(self, direction: Literal["R", "L", "U", "D"], distance: int):
        delta = np.array([0, 0])  # Initialize, just to keep linter from complaining
        match direction:
            case "R":
                delta = np.array([1, 0])
            case "L":
                delta = np.array([-1, 0])
            case "U":
                delta = np.array([0, 1])
            case "D":
                delta = np.array([0, -1])

        for _ in range(distance):
            self.position += delta
            for subscriber in self.subscribers:
                subscriber.follow(self)

    def follow(self, leader: Knot) -> None:
        if chebyshev_distance(self.position, leader.position) > 1:
            self.y += np.clip(leader.y - self.y, -1, 1)
            self.x += np.clip(leader.x - self.x, -1, 1)
        assert chebyshev_distance(self.position, leader.position) <= 1
        self.visited_positions.add(str(self.position))
        for subscriber in self.subscribers:
            subscriber.follow(self)


if __name__ == "__main__":
    # =================
    # Initialize Part 1
    # =================
    head_part1 = Knot()
    tail_part1 = Knot()
    head_part1.register_subscriber(tail_part1)

    # =================
    # Initialize Part 2
    # =================
    head_part2 = Knot()
    prev = head_part2

    for _ in range(9):
        tail_part2 = Knot()
        prev.register_subscriber(tail_part2)
        prev = tail_part2
    # ==============
    # Run Simulation
    # ==============
    with open("input.txt", "r") as inp:
        for line in inp:
            move_direction, move_distance = line.strip().split()
            move_distance = int(move_distance)

            head_part1.move(direction=move_direction, distance=move_distance)
            head_part2.move(direction=move_direction, distance=move_distance)

    print(f"Part 1: {len(tail_part1.visited_positions)}")

    print(f"Part 2: {len(tail_part2.visited_positions)}")




