"""Simple and easy pure Python solution to day 3"""


def follow_path(path: str) -> set:
    """Calculates the history along a given path """
    position = complex(0, 0)
    history = {position}
    for char in path:
        position += directions[char]
        history.add(position)
    return history


directions = {
    "^": complex(0, 1),
    "v": complex(0, -1),
    ">": complex(1, 0),
    "<": complex(-1, 0),
}

with open("input.txt", "r") as inp:
    path = inp.read().strip()

part1_history = follow_path(path)
print(f"Part 1: {len(part1_history)}")

santa_history = follow_path(path[0::2])
robot_history = follow_path(path[1::2])
part2_history = santa_history.union(robot_history)
print(f"Part 2: {len(part2_history)}")
