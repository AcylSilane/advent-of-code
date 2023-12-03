"""day 13 solution"""
import json
import itertools
import functools

import logging
import coloredlogs

coloredlogs.install(level="WARNING", fmt="%(asctime)s %(levelname)s %(message)s")

# These must be 1, 0, or -1 to conform to the functools.cmp_to_key interface
VALID = -1
INDETERMINATE = 0
INVALID = 1

logger = logging.getLogger(__name__)


def is_valid(left, right, indent=0) -> str:
    logger.debug("\t" * indent + f"\t- Compare {left} vs {right}")

    # Case: Exactly one value is an int
    if isinstance(left, int) and isinstance(right, list):
        logger.debug("\t" * indent + f"\t\t- Mixed types; convert left to [{left}] and retry comparison")
        return is_valid([left], right, indent + 1)

    elif isinstance(left, list) and isinstance(right, int):
        logger.debug("\t" * indent + f"\t\t- Mixed types; convert right to [{right}] and retry comparison")
        return is_valid(left, [right], indent + 1)

    # Case: Both values are integers
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            logger.debug("\t" * indent + "\t\t- Left side is smaller, so inputs are in the right order")
            return VALID
        elif left > right:
            logger.debug("\t" * indent + "\t\t- Right side is smaller, so inputs are not in the right order")
            return INVALID
        else:
            return INDETERMINATE

    # Case: both values are lists
    if isinstance(left, list) and isinstance(right, list):
        ptr = 0
        while (ptr < len(left)) and (ptr < len(right)):
            result = is_valid(left[ptr], right[ptr], indent=indent + 1)

            if result in (VALID, INVALID):
                return result

            ptr += 1

        if ptr == len(left):
            if (len(left) == len(right)):
                return INDETERMINATE
            else:
                logger.debug("\t" * indent + "\t\t- Left side ran out of items, so inputs are in the right order.")
                return VALID
        else:
            logger.debug("\t" * indent + "\t\t- Right side ran out of items, so inputs are not in the right order.")
            return INVALID


packet_dict = {}
all_packets = []
if __name__ == "__main__":
    with open("input.txt", "r") as inp:
        file_chunks = itertools.zip_longest(*[iter(inp)] * 3, fillvalue=None)
        for count, (str_packet1, str_packet2, blank) in enumerate(file_chunks, start=1):
            packet1 = json.loads(str_packet1.strip())
            packet2 = json.loads(str_packet2.strip())

            packet_dict[count] = {
                "packet1": packet1,
                "packet2": packet2
            }
            all_packets.extend([packet1, packet2])

    part1 = 0

    for index, packet in packet_dict.items():
        logger.debug(f"== Pair {index} ==")
        result = is_valid(packet["packet1"], packet["packet2"])
        if result == VALID:
            part1 += index

    print(f"Part 1: {part1}")

    sorted_packets = sorted(all_packets + [[[2]], [[6]]], key=functools.cmp_to_key(is_valid))
    # Add 1 because off-by-1 error
    loc1 = sorted_packets.index([[2]]) + 1
    loc2 = sorted_packets.index([[6]]) + 1
    print(f"Part 2: {loc1 * loc2}")
