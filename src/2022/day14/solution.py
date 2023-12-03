"""Day 14 solution"""
from __future__ import annotations

from typing import List, Tuple, Optional, Set
from functools import cached_property
import sys, os
import time
import numpy as np

np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

EMPTY_TILE = "·"
WALL_TILE = "#"
SAND_TILE = "O"
SAND_TRAIL = "~"
END_TILE = "="

T_Coord = Tuple[int, int]
T_Path = List[T_Coord]


class Wall:
    def __init__(self, anchors: T_Path):
        self.anchors = anchors
        self._positions: Set[T_Coord] = set()

    @classmethod
    def from_path(cls, path: T_Path) -> Wall:
        instance = cls(positions=path)
        return instance

    @cached_property
    def positions(self) -> T_Path:
        prev_anchor = None
        for current_anchor in self.anchors:
            self._positions.add(current_anchor)
            if prev_anchor is None:
                prev_anchor = current_anchor
                continue
            self.create_between(prev_anchor, current_anchor)
            prev_anchor = current_anchor
        return list(self._positions)

    def create_between(self, point1, point2) -> None:
        delta_x = abs(point1[0] - point2[0])
        delta_y = abs(point1[1] - point2[1])
        start_x = min(point1[0], point2[0])
        start_y = min(point1[1], point2[1])

        for x in range(start_x, start_x + delta_x):
            self._positions.add((x, start_y))
        for y in range(start_y, start_y + delta_y):
            self._positions.add((start_x, y))


class Sand:
    def __init__(self, position: T_Coord, grid: Grid, sand_inlet: SandInlet,
                 is_checking_spawner=False):
        self.prev_position = position
        self.position = position
        self.grid = grid
        self.sand_inlet = sand_inlet
        self.is_at_rest = False
        self.is_checking_spawner = is_checking_spawner

        self.has_reached_bottom = False
        self.has_reached_spawner = False

        self.update_grid()

    def update_grid(self):
        self.grid.set_position(self.prev_position, SAND_TRAIL)
        self.grid.set_position(self.position, SAND_TILE)

    def is_tile_clear(self, direction):
        if direction == "D":
            position_to_check = (self.position[0], self.position[1] + 1)
        elif direction == "DL":
            position_to_check = (self.position[0] - 1, self.position[1] + 1)
        elif direction == "DR":
            position_to_check = (self.position[0] + 1, self.position[1] + 1)

        tile_below = self.grid.get_position(position_to_check)
        if tile_below in (WALL_TILE, SAND_TILE):
            return False
        elif tile_below == END_TILE:
            self.has_reached_bottom = True
            return False
        else:
            return True

    def step(self):
        if self.is_at_rest or self.has_reached_spawner:
            return

        self.prev_position = self.position
        if self.is_tile_clear(direction="D"):
            self.position = (self.position[0], self.position[1] + 1)
        elif self.is_tile_clear(direction="DL"):
            self.position = (self.position[0] - 1, self.position[1] + 1)
        elif self.is_tile_clear(direction="DR"):
            self.position = (self.position[0] + 1, self.position[1] + 1)
        else:
            self.is_at_rest = True
            if self.position == self.sand_inlet.position:
                self.has_reached_spawner = True

        self.update_grid()


class SandInlet:
    def __init__(self, grid: Grid, position: T_Coord = (500, 0)):
        self.position: T_Coord = position
        self.sand_counter = 0
        self.grid = grid
        self.has_reached_bottom = False

    def dispense(self, grid: Grid):
        new_sand = Sand(position=self.grid.find_spawnpoint(), grid=grid, sand_inlet=self,
                        is_checking_spawner=self.has_reached_bottom)
        self.sand_counter += 1
        return new_sand


class Grid:
    def __init__(self, window_size: Tuple[T_Coord, T_Coord]):
        self.window_down_left = window_size[0]
        self.window_up_right = window_size[1]

        # All points are positive
        shape_x, shape_y = self.window_up_right
        shape_x += 2048  # Padding for part 2
        self.grid = np.full(shape=[shape_y, shape_x], fill_value=EMPTY_TILE, dtype=str)
        self.grid[-1] = END_TILE

        self.walls = []
        self.sand_inlet = SandInlet(grid=self, position=(500, 0))

        self.steady_state_sand_count = None

    def get_position(self, position: T_Coord):
        x, y = position
        return self.grid[y, x]

    def set_position(self, position: T_Coord, char: str):
        x, y = position
        self.grid[y, x] = char

    def find_spawnpoint(self) -> T_Coord:
        for y, row in reversed(list(enumerate(self.grid))):
            for x, char in enumerate(row):
                if char == SAND_TRAIL:
                    position = (x, y)
                    return position
        return self.sand_inlet.position

    @classmethod
    def from_instructions(cls, instructions: List[T_Path], sand_inlet_coord: Optional[T_Coord] = None) -> Grid:
        window_size = cls.get_window_size(instructions)
        instance = cls(window_size=window_size)

        for path in instructions:
            instance.add_wall(Wall(path))

        return instance

    @staticmethod
    def get_window_size(instructions: List[T_Path],
                        sand_inlet_coord: Optional[T_Coord] = (500, 0),
                        window_padding: int = 3) -> Tuple[T_Coord, T_Coord]:
        """Returns the window size for the based on the instructions. The window size will be expanded, if needed, to
        include the sand inlet's coordinates.

        Args:
            instructions (List[T_Path]) List of paths to be generated
            sand_inlet_coord (Optional[T_Coord]): Coordinate where sand flows in. Defaults to [500,0] if none provided
            window_padding (int): How muchh excess to add to the grid

        Returns:
            A tuple one coordinate for the lower left and one for the upper right of the bounding box
        """

        min_x, min_y = np.inf, np.inf
        max_x, max_y = -np.inf, -np.inf
        for path in instructions:
            for (x, y) in path:
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)

        sand_inlet_x, sand_inlet_y = sand_inlet_coord
        min_x, max_x = min(min_x, sand_inlet_x), max(max_x, sand_inlet_x)
        min_y, max_y = min(min_y, sand_inlet_y), max(max_y, sand_inlet_y)

        # And finally add some padding
        max_x, max_y = max_x + window_padding, max_y + window_padding
        min_x, min_y = max(0, min_x - window_padding), max(0, min_y - window_padding)

        return (min_x, min_y), (max_x, max_y)

    def add_wall(self, wall: Wall):
        self.walls.append(wall)
        for (x, y) in wall.positions:
            self.grid[y, x] = WALL_TILE

    @property
    def current_window(self):
        min_x, min_y = self.window_down_left
        max_x, max_y = self.window_up_right

        return self.grid[min_y:max_y + 1, min_x:max_x + 1]

    def update_window(self, coords: T_Coord):
        current_min_x, current_min_y = self.window_down_left
        current_max_x, current_max_y = self.window_up_right
        other_x, other_y = coords

        min_y, max_y = current_min_y, current_max_y
        min_x = min(current_min_x, other_x)
        max_x = max(current_max_x, other_x)

        self.window_up_right = (max_x, max_y)
        self.window_down_left = (min_x, min_y)

    def __str__(self) -> str:
        result = "\n".join("".join(row) for row in self.current_window)
        return result

    def run_simulation(self):
        is_end_reached = False

        while not is_end_reached:

            # Fixes a graphhics bug where the lines get updated out of order. Not sure why that happens, but a
            # screen clear clears that up
            if self.sand_inlet.sand_counter % 500 == 0:
                os.system("cls")

            sand = self.sand_inlet.dispense(self)
            while not (sand.is_at_rest or sand.has_reached_spawner):
                sand.step()
                self.update_window(sand.position)

                self.draw_frame()
                print(f"Sand coordinate: {sand.position}")

                if self.steady_state_sand_count is None and sand.has_reached_bottom:
                    self.steady_state_sand_count = self.sand_inlet.sand_counter - 1
                if sand.has_reached_spawner:
                    self.final_sand_count = self.sand_inlet.sand_counter
                    is_end_reached = True

    def draw_frame(self):
        print("\033[1;1H")
        print(f"Grains Dispensed: {self.sand_inlet.sand_counter}")
        print(str(self))


if __name__ == "__main__":
    raw_instructions = []
    with open("input.txt", "r") as inp:
        for line in inp:
            raw_line = line.strip().split(" -> ")
            raw_path = [tuple([int(coord) for coord in instruction.split(",")]) for instruction in raw_line]
            raw_instructions.append(raw_path)

    os.system("cls")
    grid = Grid.from_instructions(raw_instructions)
    grid.run_simulation()

    print(f"Part 1: {grid.steady_state_sand_count}")
    print(f"Part 2: {grid.final_sand_count}")
