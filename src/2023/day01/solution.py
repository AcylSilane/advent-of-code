# 2023, day 1 solution
import re

digit_map = {**{str(i): str(i) for i in range(10)},
             **{v: str(i) for i, v in enumerate(
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"])}}

with open("input.txt") as inp:
    total1 = 0
    total2 = 0

    for line in inp:
        matches1 = re.findall(f"({'|'.join(str(i) for i in range(10))})", line)
        matches2 = re.findall(f"(?=({'|'.join(digit_map.keys())}))", line)
        print(f"Line: {line.strip()}\nMatches: {matches2}")

        total1 += int(matches1[0] + matches1[-1])
        total2 += int(digit_map[matches2[0]] + digit_map[matches2[-1]])


print(total1)
print(total2)
