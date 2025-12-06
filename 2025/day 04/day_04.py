"""
Advent of Code 2025 - Day 04
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""

def to_map(data):
    grid = {}
    for y, line in enumerate(data.strip().splitlines()):
        for x, c in enumerate(line):
            if c == '@':
                grid[(x, y)] = c
    return grid

NEIGHBORS = [(0, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)]
assert (len(set(NEIGHBORS)) == len(NEIGHBORS)), "Duplicate neighbor offsets"
assert (len(set(NEIGHBORS)) == 8), "Missing neighbor offsets"

def solve(data, part2=False):
    result = 0
    grid = to_map(data)
    if not part2:
        rolls = rolls_that_can_be_removed(grid)
        result = len(rolls)
    else:
        total_removed = 0
        while True:
            rolls = rolls_that_can_be_removed(grid)
            if not rolls:
                break
            total_removed += len(rolls)
            for roll in rolls:
                del grid[roll]
        result = total_removed
    return result


def rolls_that_can_be_removed(grid):
    rolls = set()
    for (x, y) in grid:
        num_neighbors = 0
        for dx, dy in NEIGHBORS:
            if (x + dx, y + dy) in grid:
                num_neighbors += 1
        if num_neighbors < 4:
            rolls.add((x, y))
    return rolls


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 13


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 1457


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 43


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 8310


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()