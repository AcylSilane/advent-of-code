# Day 3 2023 solution
from __future__ import annotations
from typing import List
import numpy as np
import enum


class Coordinate:
    """An XY pair"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<Coordinate x={self.x} y={self.y}>"

    def __add__(self, other: Coordinate):
        x = self.x + other.x
        y = self.y + other.y
        return Coordinate(x, y)

    def __sub__(self, other: Coordinate):
        x = self.x - other.x
        y = self.y - other.y
        return Coordinate(x, y)

    def __eq__(self, other: Coordinate):
        return (other.x == self.x) and (other.y == self.y)


DIRECTIONS = [
    Coordinate(-1, 0),  # Left
    Coordinate(-1, 1),  # Left Up
    Coordinate(0, 1),  # Up
    Coordinate(1, 1),  # Right Up
    Coordinate(1, 0),  # Right
    Coordinate(1, -1),  # Right Down
    Coordinate(0, -1),  # Down
    Coordinate(-1, -1)  # Left Down
]


class Symbol:
    """A symbol in the puzzle"""

    def __init__(self, value: str, coord: Coordinate):
        self.value = value
        self.coord = coord

    def __repr__(self):
        return f"<Symbol value={self.value} coord={self.coord}>"

    def gear_ratio(self, schematic_numbers: List[SchematicNumber]):
        if self.value != "*":
            return 0
        candidates = [self.coord + direction
                      for direction in DIRECTIONS]

        adjacent_numbers = []
        for schematic_number in schematic_numbers:
            is_done = False
            if is_done:
                continue

            for coord in schematic_number.coords:
                if is_done:
                    continue

                for candidate in candidates:
                    if candidate == coord:
                        adjacent_numbers.append(schematic_number)
                        is_done = True
                        break

        if len(adjacent_numbers) == 2:
            return adjacent_numbers[0].value * adjacent_numbers[1].value
        return 0


class SchematicNumber:
    """A number in this puzzle"""

    def __init__(self, value: int, coords: List[Coordinate]):
        self.value = value
        self.coords = coords

    def __repr__(self):
        return f"<SchematicNumber value={self.value} coords={self.coords}>"

    def is_valid(self, symbols: List[Symbol]) -> bool:
        # Construct the list of coordinates to check
        candidates = [coord + direction
                      for coord in self.coords
                      for direction in DIRECTIONS]
        # Then see if any contain symbols
        return any(coord == symbol.coord for coord in candidates for symbol in symbols)


# =======
# Part 1
# =======
with open("input.txt", "r") as inp:
    data = np.array([list(line.strip()) for line in inp.readlines()])

shape_y, shape_x = data.shape

schematic_numbers = []
symbols = []

coordinates = []
number_chars = ""
is_reading_number = False
for y, row in enumerate(data):
    for x, value in enumerate(row):
        if value in "0123456789":
            is_reading_number = True
            number_chars += value
            coordinates.append(Coordinate(x, y))
        elif is_reading_number:
            schematic_numbers.append(SchematicNumber(int(number_chars), coordinates))
            number_chars = ""
            coordinates = []
            is_reading_number = False
        if value not in ".0123456789":
            symbols.append(Symbol(value, Coordinate(x, y)))
            is_reading_number = False

schematic_total = sum([number.value for number in schematic_numbers if number.is_valid(symbols=symbols)])
print(f"Part 1: {schematic_total}")

# ======
# Part 2
# ======

gear_candidates = [symbol for symbol in symbols if symbol.value == "*"]
ratio_total = sum([gear_candidate.gear_ratio(schematic_numbers) for gear_candidate in gear_candidates])
print(f"Part 2: {ratio_total}")
