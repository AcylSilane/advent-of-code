"""Solution for day 9"""
from __future__ import annotations
from typing import List
import itertools
import functools
import operator


class History:
    def __init__(self, history: List[List[int]]):
        self.history = history

    @classmethod
    def from_input(cls, input_line: List[int], direction: str = "forward") -> History:
        if direction == "forward":
            history = [input_line]
        elif direction == "backward":
            history = [input_line[::-1]]
        else:
            raise ValueError("Direction must be either 'forward' or 'backward'")
        while not all(val == 0 for val in history[-1]):
            next_line = [b - a for a, b in (itertools.pairwise(history[-1]))]
            history.append(next_line)
        return cls(history)

    @property
    def most_recent_val(self):
        return self.history[0][-1]

    def extrapolate(self) -> History:
        prev_val = 0
        self.history[-1].append(prev_val)
        for sequence in reversed(self.history[:-1]):
            next_val = prev_val + sequence[-1]
            sequence.append(next_val)
            prev_val = next_val
        return self


inputs = []
with open("input.txt", "r") as inp:
    for line in inp:
        inputs.append([int(val) for val in line.strip().split()])

part1_sum = 0
for history in [History.from_input(line) for line in inputs]:
    part1_sum += history.extrapolate().most_recent_val
print(f"Part 1: {part1_sum}")

part2_sum = 0
for history in [History.from_input(line, direction="backward") for line in inputs]:
    part2_sum += history.extrapolate().most_recent_val
print(f"Part 2: {part2_sum}")
