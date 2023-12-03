# Advent of code 2022

# File is small, let's just read it all into memory
with open("input.csv", "r") as inp:
    data = inp.read().split("\n\n")
totals = [sum(map(int, str.split(entry))) for entry in data]

# Highest
print(sorted(totals)[-1])

# Sum of first 3
print(sum(sorted(totals)[-3:]))
