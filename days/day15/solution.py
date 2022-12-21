"""Day 15 solution"""
from __future__ import annotations
from typing import Tuple
import re
import shapely.geometry, shapely.ops

import numpy as np


# np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)


def parse(line) -> Tuple[int, int, int, int]:
    sensor_x, sensor_y, beacon_x, beacon_y = map(int, re.findall(r"(?<=[x,y]=)(-?\d+)", line))
    return sensor_x, sensor_y, beacon_x, beacon_y


def calculate_line_overlap(sensors, radii, overlapping_beacons, target_y):
    overlap_potential = (radii - abs(sensors[:, 0] - target_y))
    overlap_mask = overlap_potential > 0
    bounds = np.vstack([sensors[:, 1][overlap_mask] - overlap_potential[overlap_mask],
                        sensors[:, 1][overlap_mask] + overlap_potential[overlap_mask]]).T
    min_x, max_x = bounds.min(), bounds.max()

    result = 0
    test_range = np.arange(min_x, max_x + 1)
    for (y, x) in overlapping_beacons:
        if (y == target_y) and x in range(min_x, max_x + 1):
            result -= 1

    leq = np.less_equal.outer(bounds[:, 0], test_range).any(axis=0)
    geq = np.greater_equal.outer(bounds[:, 1], test_range).any(axis=0)
    result += (leq & geq).sum()
    return result


def get_points_outside_radius(sensor: Tuple[int, int], radius: int):
    x, y = sensor
    y_U = np.arange(y, y + radius + 2)
    x_R = np.arange(x, x + radius + 2)
    y_D = np.arange(y - radius - 1, y + 1)
    x_L = np.arange(x - radius - 1, x + 1)

    points = np.vstack([
        np.vstack([y_U[::-1], x_R]).T,  # UR
        np.vstack([y_U, x_L]).T,  # UL
        np.vstack([y_D, x_R]).T,  # DR
        np.vstack([y_D[::-1], x_L]).T  # DL
    ])
    return points


if __name__ == "__main__":
    TARGET_Y = 10  # 2000000
    LIMIT = 4000000

    sensors = []
    beacons = []
    radii = []
    overlapping_beacons = set()
    with open("input.txt", "r") as inp:
        for line in inp:
            sensor_x, sensor_y, beacon_x, beacon_y = parse(line)
            radii.append(abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y))
            sensors.append((sensor_y, sensor_x))
            beacons.append((beacon_y, beacon_x))
            if beacon_y == TARGET_Y:
                overlapping_beacons.add((beacon_y, beacon_x))

    radii = np.array(radii)
    beacons = np.array(list(set(beacons)))
    sensors = np.array(sensors)

    # part 1
    overlap_count = calculate_line_overlap(sensors, radii, overlapping_beacons, target_y=TARGET_Y)
    print(f"Part 1: {overlap_count}")

    # part 2
    # tried this a few ways, couldn't get a good solution. Shapely seems like the most relevant library
    # within the Python ecosystem
    bounding_box = shapely.geometry.Polygon([
        [0, 0], [LIMIT, 0], [LIMIT, LIMIT], [0, LIMIT]
    ])
    beacon_overlap = shapely.ops.unary_union([shapely.geometry.Polygon([
        [x + radius, y], [x, y - radius], [x - radius, y], [x, y + radius]
    ]) for (y, x), radius in zip(sensors, radii)])

    possible_points = bounding_box.difference(beacon_overlap)

    part2_x = (possible_points.bounds[0] + 1) * LIMIT
    part2_y = (possible_points.bounds[1] + 1)
    print(f"Part 2: {int(part2_x + part2_y)}")
