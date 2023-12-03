import string

priority = dict(zip(string.ascii_letters, range(1, 53)))

total1 = 0
total2 = 0
group = []
with open("input.csv") as inp:
    for raw_line in inp:
        # Split string in half
        line = raw_line.strip()
        group.append(line)
        midpoint = len(line) // 2
        compartment1, compartment2 = set(line[:midpoint]), set(line[midpoint:])

        # Calculate priority for part 1
        duplicate = compartment1.intersection(compartment2).pop()
        total1 += priority[duplicate]

        # Handle part 2
        if len(group) == 3:
            bags = map(set, group)
            total2 += priority[set.intersection(*bags).pop()]
            group = []

print(f"Part 1: {total1}")
print(f"Part 2: {total2}")
