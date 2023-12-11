"""
Advent of Code 2023 - Day 11
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

EXAMPLE_DATA_EXPANDED = """\
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
"""

from bisect import bisect_right


def parse(data):
    initial_galaxies = []
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                initial_galaxies.append((x, y))
    return initial_galaxies


def solve(data, expansion_factor=2):
    initial_galaxies = parse(data)
    x_coords = set([x for x, y in initial_galaxies])
    y_coords = set([y for x, y in initial_galaxies])
    # find the bounding box of the initial galaxies
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    # find empty rows
    empty_rows = list(set(range(min_y, max_y + 1)) - y_coords)
    empty_rows.sort()
    # find empty columns
    empty_cols = list(set(range(min_x, max_x + 1)) - x_coords)
    empty_cols.sort()

    expanded_galaxies = []
    for x, y in initial_galaxies:
        # find number of empty rows to the left
        n_empty_rows = bisect_right(empty_rows, y)
        # find number of empty columns to the left
        n_empty_cols = bisect_right(empty_cols, x)
        new_galaxy = (
            x + n_empty_cols * (expansion_factor - 1),
            y + n_empty_rows * (expansion_factor - 1),
        )
        expanded_galaxies.append(new_galaxy)

    result = 0
    for i, g1 in enumerate(expanded_galaxies):
        for g2 in expanded_galaxies[i + 1 :]:
            distance = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
            result += distance
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 374


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 9647174


def test_example2():
    assert 1030 == solve(EXAMPLE_DATA, expansion_factor=10)
    assert 8410 == solve(EXAMPLE_DATA, expansion_factor=100)


def test_part2():
    result = solve(data(), expansion_factor=1000000)
    print("Part 2:", result)
    assert result == 377318892554


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
