import copy
import re
import string
import enum

states = enum.Enum("states", ["STORE_CRATES", "INIT_CRATES", "MOVE_CRATES"])

state = states.STORE_CRATES
crate_lines = []
stacks_part1 = {}
stack_indices = {}
with open("input.txt", "r") as inp:
    for line in map(str.rstrip, inp):
        # ===========
        # Read Header
        # ===========
        if state == states.STORE_CRATES:
            if line:
                crate_lines.append(line)
            else:
                state = state.INIT_CRATES

        # =================
        # Initialize Stacks
        # =================
        if state == state.INIT_CRATES:
            # Figure out where the crates are
            crate_stacks = crate_lines.pop()
            for index, char in enumerate(crate_stacks):
                if char in string.digits:
                    stacks_part1[char] = []
                    stack_indices[char] = index

            # Populate crates
            for row in reversed(crate_lines):
                for index, location in stack_indices.items():
                    if row[location].strip():
                        stacks_part1[index].append(row[location])

            stacks_part2 = copy.deepcopy(stacks_part1)
            state = states.MOVE_CRATES

        # ==============
        # Run Simulation
        # ==============
        if state == states.MOVE_CRATES and line:
            # Interpret instruction
            move_size = int(re.search(r"(?<=move\s)\d+", line)[0])
            source_stack = re.search(r"(?<=from\s)\d+", line)[0]
            dest_stack = re.search(r"(?<=to\s)\d+", line)[0]

            # Carry out instruction, part 1
            chunk_1 = stacks_part1[source_stack][-move_size:]
            stacks_part1[source_stack] = stacks_part1[source_stack][:-move_size]
            stacks_part1[dest_stack].extend(reversed(chunk_1))

            # Carry out instruction, part 2
            chunk_2 = stacks_part2[source_stack][-move_size:]
            stacks_part2[source_stack] = stacks_part2[source_stack][:-move_size]
            stacks_part2[dest_stack].extend(chunk_2)

# Part 1
print(f"Part 1: {''.join(item[-1] for item in stacks_part1.values())}")
print(f"Part 2: {''.join(item[-1] for item in stacks_part2.values())}")
