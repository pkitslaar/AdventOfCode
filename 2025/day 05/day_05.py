"""
Advent of Code 2025 - Day 05
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""


def solve(data, part2=False):
    result = 0

    ranges = []
    ingredients = []
    for row in data.strip().splitlines():
        if "-" in row:
            start, end = map(int, row.split("-"))
            ranges.append((start, end))
        elif row.isdigit():
            value = int(row)
            ingredients.append(value)

    if not part2:
        for i in ingredients:
            for start, end in ranges:
                if start <= i <= end:
                    result += 1
                    break
        return result

    # part 2
    ranges.sort()
    while True:
        merged_ranges = []
        current_start, current_end = ranges[0]
        for start, end in ranges[1:]:
            if start <= current_end + 1:
                current_end = max(current_end, end)
            else:
                merged_ranges.append((current_start, current_end))
                current_start, current_end = start, end
        merged_ranges.append((current_start, current_end))
        if len(merged_ranges) == len(ranges):
            break
        ranges = merged_ranges

    for r in merged_ranges:
        result += r[1] - r[0] + 1

    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 3


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 744


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 14


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 347468726696961


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
