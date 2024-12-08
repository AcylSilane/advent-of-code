"""Give it up for day 4!"""

from __future__ import annotations
import sys
import itertools

import numpy as np


def read_input() -> np.ndarray:
    """Reads the input file and returns it as a numpy array."""
    with open("input.txt", "r") as fp:
        lines = [[*line.strip()] for line in fp.readlines()]
        return np.array(lines, dtype=str)


def problem1(data: np.array) -> int:
    """Problem 1. Find XMAS in the word search

    Returns:
        Number of XMAS lines found.
    """
    target = "XMAS"
    num_found = 0

    # U / D / L / R / Diags
    search_vectors = [*map(np.array, itertools.product([-1, 0, 1], repeat=2))]

    # Too lazy to check indices, just pad the board with 0's.
    board = np.pad(data, 1)

    # Do the actual search
    x_coords = zip(*np.where(board == target[0]))
    for position, search_vector in itertools.product(x_coords, search_vectors):
        for index in range(1, len(target)):
            position = tuple(position + search_vector)
            if board[position] != target[index]:
                break
        else:
            num_found += 1
    return num_found


def problem2(data: np.array) -> int:
    """Problem 2. Find the X-MAS in the word search

    Returns:
        Number of X-MAS instances.
    """
    num_found = 0
    board = np.pad(data, 1)

    # These are the facts:
    # - The center of the X is always an "A"
    # - We know MAS is along a line
    # Therefore, what we're really checking is whether both diagonals contain an "S" and an "M"

    a_coords = [*zip(*np.where(board == "A"))]
    for position in a_coords:
        # Indexing by multiple tuples is *painful* in numpy so I'm just doing it by hand
        ur, lr = (position[0]-1, position[1]+1), (position[0]+1, position[1]+1)
        ul, ll = (position[0]-1, position[1]-1), (position[0]+1, position[1]-1)
        word1 = f"{board[ul]}{board[position]}{board[lr]}"
        word2 = f"{board[ur]}{board[position]}{board[ll]}"
        if ((word1 == "MAS" or word1 == "SAM") and (word2 == "MAS" or word2 == "SAM")):
            num_found += 1
    return num_found


def main():
    """Main. It's, well, the main function."""
    board = read_input()

    solution1 = problem1(board)
    solution2 = problem2(board)

    print(f"Solution 1: {solution1}")
    print(f"Solution 2: {solution2}")


if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)
    main()
