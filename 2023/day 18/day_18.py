"""
Advent of Code 2023 - Day 18
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
DIRECTIONS = {"U": (0, -1), "R": (1, 0), "D": (0, 1), "L": (-1, 0)}

from heapq import heappush, heappop, heapify


def solve(data, part2=False):
    """Naive solution. To slow for part 2"""

    dig_grid = {}
    prev_pos = (0, 0)
    for line in data.splitlines():
        direction, length, color = line.split()
        length = int(length)
        if part2:
            direction = "RDLU"[int(color[-2])]
            length = int(color[2:-2], 16)
        offset = DIRECTIONS[direction]
        for _ in range(length):
            x = prev_pos[0] + offset[0]
            y = prev_pos[1] + offset[1]
            dig_grid[x, y] = color
            prev_pos = (x, y)

    min_x = min(x for x, y in dig_grid.keys())
    max_x = max(x for x, y in dig_grid.keys())
    min_y = min(y for x, y in dig_grid.keys())
    max_y = max(y for x, y in dig_grid.keys())

    # fill intertior
    to_visit = [(0, (1, 1))]  # first intertior point
    heapify(to_visit)
    while to_visit:
        t, c_pos = heappop(to_visit)

        assert min_x <= c_pos[0] <= max_x
        assert min_y <= c_pos[1] <= max_y

        if c_pos in dig_grid:
            continue
        dig_grid[c_pos] = "#"
        for offset in DIRECTIONS.values():
            x = c_pos[0] + offset[0]
            y = c_pos[1] + offset[1]
            if (x, y) not in dig_grid:
                heappush(to_visit, (t + 1, (x, y)))
    result = len(dig_grid)
    return result


def solve_fast(data, part2=False):
    dig_edges = []
    prev_pos = (0, 0)
    circumfrence = 0
    for line in data.splitlines():
        direction, length, color = line.split()
        length = int(length)
        if part2:
            direction = "RDLU"[int(color[-2])]
            length = int(color[2:-2], 16)
        circumfrence += length
        offset = DIRECTIONS[direction]

        next_pos = (prev_pos[0] + offset[0] * length, prev_pos[1] + offset[1] * length)
        dig_edges.append((prev_pos, next_pos))
        prev_pos = next_pos

    # area of dig polygon
    area = 0
    for (u, v) in dig_edges:
        area += (u[0] * v[1]) - (v[0] * u[1])
    area = abs(area) // 2

    # we add half the circumference as area because
    # the coordinates in the grid represent the center of the cubes
    result = area + circumfrence // 2 + 1

    return result


def test_example():
    naive_result = solve(EXAMPLE_DATA)
    result = solve_fast(EXAMPLE_DATA)
    assert naive_result == result
    print(f"example: {result}")
    assert result == 62


def test_part1():
    naive_result = solve(data())
    result = solve_fast(data())
    assert naive_result == result
    print("Part 1:", result)
    assert result == 45159


def test_example2():
    result = solve_fast(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 952408144115


def test_part2():
    result = solve_fast(data(), part2=True)
    print("Part 2:", result)
    assert result == 134549294799713


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()
