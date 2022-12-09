from typing import Literal
import sys

import numpy as np

np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

T_Direction = Literal["left", "right", "up", "down"]


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


if __name__ == "__main__":
    # Read data
    with open("input.txt", "r") as inp:
        data = np.array([[int(char) for char in line.strip()] for line in inp])

    vision = np.zeros(shape=data.shape, dtype=bool)
    for direction in ("left", "right", "up", "down"):
        vision |= calc_vision_mask(height_map=data, direction=direction)

    print(vision.astype(np.int32))

    print(f"Part 1: {vision.sum()}")
