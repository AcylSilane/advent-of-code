"""Day 5! Probably a better way to do this, but I'm a little bit behind on these"""

from __future__ import annotations
from collections import defaultdict
from typing import List, Tuple, Set, Dict, TypeVar

T = TypeVar("T")


def read_input() -> List[Tuple[int, int], List[List[str]]]:
    """Reads the input, same as always"""
    with open("input.txt", "r") as fp:
        updates = []
        rules = []
        for line in fp:
            if "|" in line:
                # We're getting a page order rule
                x, y = (*map(int, line.strip().split("|")),)
                rules.append((x, y))
            elif line.strip():
                updates.append([*map(int, line.strip().split(","))])
    return rules, updates


def is_in_order(rules: List[Tuple[int, int]], update: List[int]) -> bool:
    """Checks whether the pages follow the rules

    Maybe there's a better way to do this

    Args:
        rules: List of rules
        update: List of pages

    Returns:
        Whether every rule is valid
    """
    for index, page in enumerate(update):
        pages_start = min(index+1, len(update)-1)
        remaining_pages = update[pages_start:]
        # print(f"Page: {page}, Remaining: {remaining_pages}")
        for req_before, req_after in rules:
            # print(f"\t...Checking {req_before} -> {req_after}", end="...")
            if (page == req_after) and (req_before in remaining_pages):
                # print("FAIL")
                return False
            # print("OK")
    return True


def get_median_element(seq: List[T]) -> T:
    """Gets the median element from a sequence"""
    index = len(seq) // 2
    return seq[index]


def problem1(
    rules: List[Tuple[int, int]], updates: List[List[int]]
) -> int:
    """Problem 1 - Are the pages in the right order?

    Args:
        ordering: Dictionary mapping rules to pages that come after
        rev_ordering: Dictionary mapping rules to pages that come before
        updates: Page updates we're checking

    Returns:

    """
    result = 0
    for update in updates:
        if is_in_order(rules, update):
            result += get_median_element(update)
    return result


def fix_update(rules: List[Tuple[int, int]], update: List[int]) -> List[int]:
    """Fixes the update so that it follows the rules

    Args:
        rules: List of rules
        update: List of pages

    Returns:
        Fixed list of pages
    """
    is_fixing = True
    while is_fixing:
        is_changed = False
        for index, page in enumerate(update):
            pages_start = min(index+1, len(update)-1)
            remaining_pages = update[pages_start:]
            for req_before, req_after in rules:
                if (page == req_after) and (req_before in remaining_pages):
                    # We need to swap the pages
                    after_index = update.index(req_before)
                    update[index] = req_before
                    update[after_index] = req_after
                    is_changed = True
                    break
            if is_changed:
                break
        else:
            is_fixing = False
    return update


def problem2(
        rules: List[Tuple[int, int]], updates: List[List[int]]
) -> int:
    """Problem 2 - What about if we fix them?"

    Args:
        rules: List of rules
        updates: List of updates

    Returns:
        Sum of the median elements of the fixed updates
    """
    result = 0
    for update in updates:
        if not is_in_order(rules, update):
            fixed_update = fix_update(rules, update)
            result += get_median_element(fixed_update)
    return result


def main():
    """Main solution"""
    rules, updates = read_input()
    solution1 = problem1(rules, updates)
    solution2 = problem2(rules, updates)

    print(f"Solution 1: {solution1}")
    print(f"Solution 2: {solution2}")


if __name__ == "__main__":
    main()
