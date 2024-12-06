"""Day 3 of Advent of Code 2024"""

import re


def parse_input(path: str) -> str:
    """Read the input. Not a huge file, into the memory it goes."""
    with open(path, "r") as file:
        return file.read()


def problem1(data: str) -> int:
    """Problem 1.

    Here we'll find valid multiplication instructions and sum 'em up.

    Args:
        data: The input data.

    Returns:
        The sum of the multiplication instructions.
    """
    acc = 0
    for match in re.finditer(r"mul\((\d+),(\d+)\)", data):
        mul1, mul2 = map(int, match.groups())
        acc += mul1 * mul2
    return acc


def problem2(data: str) -> int:
    """Problem 2.

    Same problem, except now the do/don't instructions can turn on or off the multiplication

    Args:
        data: The input data.

    Returns:
        The sum of the multiplication instructions. But with the new instructions this time.
    """
    is_doing_the_thing = True
    acc = 0
    for operation in re.finditer(
        r"(mul(?=\((\d+),(\d+)\))|do(?=\(\))|don't(?=\(\)))", data
    ):
        match operation.groups()[0]:
            case "mul":
                if is_doing_the_thing:
                    mul1, mul2 = map(int, operation.groups()[1:])
                    acc += mul1 * mul2
            case "do":
                is_doing_the_thing = True
            case "don't":
                is_doing_the_thing = False
            case _:
                raise ValueError(f"Unknown operation: {operation}")
    return acc


def main():
    """Main function."""
    data = parse_input("input.txt")
    solution1 = problem1(data)
    solution2 = problem2(data)

    print(f"Solution 1: {solution1}")
    print(f"Solution 2: {solution2}")


if __name__ == "__main__":
    main()
