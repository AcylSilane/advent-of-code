# Day 4 2023

import tqdm

class Edge:
    def __init__(self, source: int, destination: int, input_range: int):
        self.source = source
        self.destination = destination
        self.input_range = input_range

    @classmethod
    def from_line(cls, line: str):
        destination, source, input_range = line.split()
        return cls(source=int(source),
                   destination=int(destination),
                   input_range=int(input_range))

    def __repr__(self):
        return f"<Map {self.source} -> {self.destination} ({self.input_range})>"

    def is_in_range(self, value: int) -> bool:
        return self.source <= value < (self.source + self.input_range)

    def source_to_destination(self, value: int):
        if self.is_in_range(value):
            offset = value - self.source
            return self.destination + offset
        else:
            raise ValueError(f"{value} is not in range of {self}")

    def all_sources(self):
        return range(self.source, self.source + self.input_range)


class IdentityEdge(Edge):
    def __init__(self):
        super().__init__(0, 0, 0)

    def is_in_range(self, value: int) -> bool:
        return True

    def source_to_destination(self, value: int):
        return value

    def __repr__(self):
        return f"<Identity Edge>"


class Map:
    identity_edge = IdentityEdge()

    def __init__(self, name: str):
        self.name = name
        self.edges = []

    def __repr__(self):
        return f"<Map {self.name}, {len(self.edges)} Edges>"

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def map(self, value: int):
        result = None
        for edge in [*self.edges, self.identity_edge]:
            if edge.is_in_range(value):
                result = edge.source_to_destination(value)
                break
        return result


class MapCollection:
    def __init__(self, maps: list[Map]):
        self.maps = maps

    def propagate(self, value: int, trace: bool = False):
        result = value
        if trace:
            print(f"{result}", end="")
        for map_obj in self.maps:
            result = map_obj.map(result)
            if trace:
                print(f"->{result}", end="")
        if trace:
            print()
        return result


with open("input.txt", "r") as inp:
    seed_tokens = [int(i) for i in inp.readline().split()[1:]]

    is_reading_block = False
    maps = []
    for line in inp:
        if line.strip() == "":
            is_reading_block = False
            current_map = None
            continue

        elif "map" in line:
            is_reading_block = True
            current_map = Map(line.split()[0])
            maps.append(current_map)
            continue

        if is_reading_block:
            current_map.add_edge(Edge.from_line(line))
    map_collection = MapCollection(maps)

# Part 1
part1_locations = [map_collection.propagate(seed) for seed in seed_tokens]
print(f"Part 1: {min(part1_locations)}")


# Part 2
# The more optimal solution is to work with ranges, but I didn't implement that in Part 1, and I'm a little behind on
# this year's puzzles. In the real world I'd refactor it, but I'm doing this in my free time for fun!
# The kinda worse optimization I'll use is to start from the final map and work backwards

class SeedRange:
    def __init__(self, source: int, input_range):
        self.source = source
        self.input_range = input_range

    def __repr__(self):
        return f"<SeedRange {self.source} -({self.input_range})-> {self.source + self.input_range}>"

    def is_in_range(self, value: int) -> bool:
        return self.source <= value < (self.source + self.input_range)


seeds = [SeedRange(seed_tokens[i], seed_tokens[i + 1]) for i in range(0, len(seed_tokens), 2)]

reversed_maps = []
for map_obj in reversed(maps):
    reversed_map = Map(f"Reversed {map_obj.name}")
    for edge in map_obj.edges:
        reversed_edge = Edge(source=edge.destination,
                             destination=edge.source,
                             input_range=edge.input_range)
        reversed_map.add_edge(reversed_edge)
    reversed_maps.append(reversed_map)
reversed_map_collection = MapCollection(reversed_maps)

to_check = -1
is_found = False
pbar = tqdm.tqdm()
while not is_found:
    to_check += 1
    seed = reversed_map_collection.propagate(to_check, trace=False)
    for seed_range in seeds:
        if seed_range.is_in_range(seed):
            is_found = True
    pbar.update(1)
print(f"Part 2: {to_check}")

# Okay this is just a bit of eye candy, but it was fun
# I'm also very surprised that PyGame of all things is the easiest way to play MIDI in Python on Windows
try:
    import pygame
    import tkinter as tk
    import tkinter.messagebox
    pygame.mixer.init()
    midi_file = "C:/Windows/Media/flourish.mid"
    pygame.mixer.music.load(midi_file)

    root = tk.Tk()
    root.withdraw()
    pygame.mixer.music.play()
    tk.messagebox.showinfo("We did it!", f"Part 1: {min(part1_locations)}\nPart 2: {to_check}")
    pygame.mixer.music.stop()

except ImportError:
    pass

