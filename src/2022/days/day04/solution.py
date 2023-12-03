# Solution for day 4

def check_status(list1, list2):
    min1, max1 = map(int, list1)
    min2, max2 = map(int, list2)

    if (min2 <= min1 and max1 <= max2) or (min1 <= min2 and max2 <= max1):
        return "fully_engulfed"

    overlap_left, overlap_right = max(min1, min2), min(max1, max2)
    if overlap_right>= overlap_left:
        return "partial_engulf"


    return "no_overlap"


engulfed_count = 0
overlap_count = 0
with open("input.csv", "r") as inp:
    for line in inp:
        elf1, elf2 = line.strip().split(",")
        status = check_status(elf1.split("-"), elf2.split("-"))

        if status == "fully_engulfed":
            engulfed_count += 1
        if status == "partial_engulf" or status == "fully_engulfed":
            overlap_count += 1
        else:
            print(elf1, elf2, "no overlap... noverlap")

print(f"Part 1: {engulfed_count}")
print(f"Part 2: {overlap_count}")
