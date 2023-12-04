# Day 2 solution
from typing import Tuple, List, Dict

MAX_POSSIBLE = {
    "red": 12,
    "green": 13,
    "blue": 14
}


def get_id_content(line: str) -> Tuple[str, str]:
    half1, half2 = line.strip().split(":")
    line_id = int(half1.split()[-1])

    # Drop initial space
    line_content = half2[1:].strip()

    return line_id, line_content


def content_to_rbg(line: str) -> List[Dict[str, int]]:
    contents = line.split(";")
    results = []
    for content in contents:
        content_results = {}
        tokens = [*map(str.split, content.strip().split(","))]
        result = {color: int(amount) for amount, color in tokens}
        results.append(result)
    return results


def is_possible(game: List[Dict[str, int]]) -> bool:
    for draw in game:
        for color in ["red", "green", "blue"]:
            if draw.get(color, 0) > MAX_POSSIBLE[color]:
                return False
    return True


def get_power(game: List[Dict[str, int]]) -> int:
    maxima = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    for draw in game:
        for color in ["red", "green", "blue"]:
            maxima[color] = max(maxima[color], draw.get(color, 0))
    power = maxima["red"] * maxima["green"] * maxima["blue"]
    return power


with open("input.txt", "r") as inp:
    part1 = 0
    part2 = 0
    for line in inp:
        line_id, line_content = get_id_content(line)
        game = content_to_rbg(line_content)

        if is_possible(game):
            part1 += line_id
        part2 += get_power(game)

print(f"Part1: {part1}")
print(f"Part2: {part2}")
