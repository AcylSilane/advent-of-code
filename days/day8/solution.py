from typing import Literal
import sys

import numpy as np

np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

T_Direction = Literal["left", "right", "up", "down"]


# If I had to refactor this, would probably be more efficient to just use the scenic score function or something,
# having it return if a tree can see an edge. The part 2 requirement wasn't revealed until after part 1 was done!
def calc_vision_mask(height_map: np.array, direction: T_Direction = "left") -> np.array:
    """Calculates whether a tree can be seen when looking from the left side of the matrix.

    A tree can be seen if it is higher than all the others before it.

    Args:
        height_map (np.array): The matrix of interest
        direction (str): Direction the observer looks from. Must be "left", "right", "up", or "down"

    Returns:
        A boolean array with the same shape as the matrix. True entries are visible. False entries are not visible.
    """
    # Tuple format is {"Direction": transform}
    # All four transforms are their own inverse
    transforms = {
        "left": lambda matrix: matrix,
        "right": lambda matrix: np.flip(matrix, axis=1),
        "up": lambda matrix: matrix.transpose(),
        "down": lambda matrix: np.flip(matrix.transpose())
    }
    transform_fun = transforms[direction]

    transformed_heightmap = transform_fun(height_map)
    transformed_local_vision = np.zeros(shape=transformed_heightmap.shape, dtype=bool)
    for y, row in enumerate(transformed_heightmap):
        local_maximum = -np.inf
        for x, height in enumerate(row):
            if height > local_maximum:
                local_maximum = height
                transformed_local_vision[y, x] = True

    local_vision = transform_fun(transformed_local_vision)
    return local_vision


def calculate_scenic_score(ceiling: int, height_vector: np.array):
    count = 0  # Reference-before-assignment safeguard. Shouldn't get into this state, but putting it here anyway
    for count, height in enumerate(height_vector, 1):
        if height >= ceiling:
            break
    return count


def calculate_all_scenic_scores(height_map: np.array) -> np.array:
    """Calculates a map of scenic scores.

    For each of the 4 cardinal directions, we calculate the number of trees visible in that direction.
    - We stop if the tree is greater than or equal to the height of the current tree
    - We stop if we reach an edge
    - A tree is visible if its height is less than the maximum height seen so far.

    Args:
        height_map (np.array): Height map

    Returns:
        An array containingg all scenic scores.
    """
    scores = np.zeros(shape=height_map.shape)

    y_lim, x_lim = height_map.shape

    for y, row in enumerate(height_map):
        for x, height in enumerate(row):
            if y == 0 or x == 0 or x == x_lim - 1 or y == y_lim - 1:
                scores[y, x] = 0
            else:
                scores[y, x] = 1  # Multiplication identity; the scores will be nonzero
                col = height_map[:, x]
                left = row[:x][::-1]
                right = row[x + 1:]
                up = col[:y][::-1]
                down = col[y + 1:]
                for vector in (left, right, up, down):
                    scores[y, x] *= calculate_scenic_score(height, vector)

    return scores


if __name__ == "__main__":
    # Read data
    with open("input.txt", "r") as inp:
        data = np.array([[int(char) for char in line.strip()] for line in inp])

    vision = np.zeros(shape=data.shape, dtype=bool)
    for direction in ("left", "right", "up", "down"):
        vision |= calc_vision_mask(height_map=data, direction=direction)

    print(f"Part 1: {vision.sum()}")

    print(f"Part 2: {calculate_all_scenic_scores(data).astype(int).max()}")
