"""
Advent of Code 2024 - Day 08
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

def parse(data):
    grid = {}
    for y, line in enumerate(data.strip().splitlines()):
        for x, c in enumerate(line):
            grid[(x,y)] = c
    return grid

from collections import defaultdict
from itertools import combinations

def along_line_in_grid(grid, p, dx, dy):
    x, y = p
    while (x, y) in grid:
        yield (x, y)
        x += dx
        y += dy

def solve(data, part2=False):
    grid = parse(data)

    antennas = defaultdict(list)
    for pos, c in grid.items():
        if c not in '.':
            antennas[c].append(pos)

    antinodes = defaultdict(list)
    for c_name, c_positions in antennas.items():
        for p1, p2 in combinations(c_positions, 2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            if not part2:
                p1_antinode = (p1[0] - dx, p1[1] - dy)
                p2_antinode = (p2[0] + dx, p2[1] + dy)
                antinodes[c_name].extend([p1_antinode, p2_antinode])
            else:
                antinodes[c_name].extend(along_line_in_grid(grid, p1, -dx, -dy))
                antinodes[c_name].extend(along_line_in_grid(grid, p2, dx, dy))

    if False:
        # optional print routing to check locations
        a_grid = grid.copy()
        for c_name, a_positions in antinodes.items():
            for a_pos in a_positions:
                if a_pos in a_grid and a_grid[a_pos] == '.':
                    a_grid[a_pos] = '#'

        H = max(y for x, y in a_grid)
        W = max(x for x, y in a_grid)
        print()
        for y in range(H+1):
            print(''.join(a_grid[(x,y)] for x in range(W+1)))
    
    unique_antinodes = {a_pos for a_posistion in antinodes.values() for a_pos in a_posistion if a_pos in grid}
    result = len(unique_antinodes)
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 14


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 299


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 34


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 1032


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()