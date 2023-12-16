"""
Advent of Code 2023 - Day 16
Pieter Kitslaar
"""


def parse(data):
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[x, y] = c
    return grid


DIRECTIONS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
TURNS = {
    ("N", "/"): "E",
    ("N", "\\"): "W",
    ("E", "/"): "N",
    ("E", "\\"): "S",
    ("S", "/"): "W",
    ("S", "\\"): "E",
    ("W", "/"): "S",
    ("W", "\\"): "N",
}

from collections import namedtuple
from heapq import heappush, heappop, heapify

Beam = namedtuple("Beam", "x y direction")


def trace_beam(grid, x=0, y=0, direction="E"):
    start_beam = Beam(x, y, direction)
    to_visit = [(0, start_beam)]
    heapify(to_visit)

    visited = set()

    while to_visit:
        t, current_beam = heappop(to_visit)
        try:
            c = grid[current_beam.x, current_beam.y]
        except KeyError:
            # out of bounds
            continue

        if current_beam in visited:
            continue
        visited.add(current_beam)

        match c, current_beam.direction:
            case ("|", "N") | ("|", "S") | ("-", "E") | ("-", "W") | (".", _):
                # continue in same direction
                n_offset = DIRECTIONS[current_beam.direction]
                next_beam = Beam(
                    current_beam.x + n_offset[0],
                    current_beam.y + n_offset[1],
                    current_beam.direction,
                )
                heappush(to_visit, (t + 1, next_beam))
            case ("|", _) | ("-", _):
                split_dirs = "NS" if current_beam.direction in "EW" else "EW"
                for new_d in split_dirs:
                    n_offset = DIRECTIONS[new_d]
                    next_beam = Beam(
                        current_beam.x + n_offset[0],
                        current_beam.y + n_offset[1],
                        new_d,
                    )
                    heappush(to_visit, (t + 1, next_beam))
            case ("/", _) | ("\\", _):
                new_d = TURNS[current_beam.direction, c]
                n_offset = DIRECTIONS[new_d]
                next_beam = Beam(
                    current_beam.x + n_offset[0], current_beam.y + n_offset[1], new_d
                )
                heappush(to_visit, (t + 1, next_beam))
            case _:
                raise ValueError(f"Unknown situation {c=} {current_beam.direction=}")

    unique_position = set((x, y) for x, y, _ in visited)
    return len(unique_position)


def solve(data, part2=False):
    grid = parse(data)
    if not part2:
        result = trace_beam(grid)
    else:
        max_x = max(x for x, y in grid)
        max_y = max(y for x, y in grid)

        start_options = []
        start_options.extend([(x, 0, "S") for x in range(max_x + 1)])
        start_options.extend([(x, max_y, "N") for x in range(max_x + 1)])
        start_options.extend([(0, y, "E") for y in range(max_y + 1)])
        start_options.extend([(max_x, y, "W") for y in range(max_y + 1)])

        energized = [trace_beam(grid, x, y, d) for x, y, d in start_options]
        result = max(energized)
    return result


def test_example():
    EXAMPLE_DATA = data("example.txt")
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 46


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 7472


def test_example2():
    EXAMPLE_DATA = data("example.txt")
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 51


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 7716


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data(fn="input.txt"):
    with open(THIS_DIR / fn) as f:
        return f.read()
