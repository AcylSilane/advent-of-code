"""Solution to Day 2 2024, Advent of Code
Back to Python for today, since it's a little faster to develop in
"""
from __future__ import annotations
from typing import List
import numpy as np


def get_input() -> List[List[int]]:
    """Parses our input from file
    
    Returns:
        The list of reports for the problem
    """
    reports = []
    with open("input.txt", "r") as fp:
        for line in fp:
            reports.append([*map(int, line.strip().split())])
    return reports

def is_safe(report: List[int]) -> bool:
    """Checks if a report is safe.
    
    A report is safe if
        1) It strictly increases or decreases monotonically
        2) The difference between each element is between 1 and 3

    Args:
        report: The list of integers to check

    Returns:
        True if the report is safe, False otherwise
    """
    deltas = np.diff(report)
    is_mono = np.all(deltas > 0) or np.all(deltas < 0)
    is_in_bounds = np.all((np.abs(deltas) >= 1) & (np.abs(deltas) <= 3))
    return is_mono & is_in_bounds

def is_bad(report: List[int]) -> bool:
    """Checks if a report is bad. Convenience function, opposite of is_safe
    
    Returns:
        Inverse of is_safe
    """
    return not is_safe(report)

def problem1(reports: List[List[int]]) -> int:
    """Solves problem 1: How many reports are safe?
    
    Args:
        reports: The list of reports to check

    Returns:
        The number of safe reports
    """
    return sum(map(is_safe, reports))
        
def problem2(reports: List[List[int]]) -> int:
    """Solves problem 2: How many can the Problem Dampener fix?

    A report can be fixed if removing a single level makes it safe
    
    Args:
        reports: The list of reports to check

    Returns:
        The number of safe reports after we're allowed to fix them
    """
    acc = sum(map(is_safe, reports))
    for candidate in filter(is_bad, reports):
        for i in range(len(candidate)):
            if is_safe(candidate[:i] + candidate[i+1:]):
                acc += 1
                break
    return acc

def main():
    """Just a solution runner"""
    puzzle_input = get_input()
    solution1 = problem1(puzzle_input)
    solution2 = problem2(puzzle_input)
    print(f"Solution 1: {solution1}")
    print(f"Solution 2: {solution2}")

if __name__ == "__main__":
    main()