import collections

with open("input.txt", "r") as inp:
    line = inp.read()

window_part1 = collections.deque(maxlen=4)
window_part2 = collections.deque(maxlen=14)

is_searching_part1 = True
for index, char in enumerate(line, start=1):
    window_part1.append(char)
    window_part2.append(char)

    if is_searching_part1 and (len(window_part1) == 4) and (len(window_part1) == len(set(window_part1))):
        is_searching_part1 = False
        print(f"Part 1: {window_part1} at {index}")

    if (len(window_part2) == 14) and (len(window_part2) == len(set(window_part2))):
        print(f"Part 2: {window_part2} at {index}")
        break
