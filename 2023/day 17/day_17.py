"""
Advent of Code 2023 - Day 17
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


def parse(data):
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            grid[x, y] = c
    return grid


from collections import namedtuple
from heapq import heappush, heappop, heapify

Crucible = namedtuple("Crucible", "heat_loss x y directions")

DIRECTIONS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
OPPOSITE = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
}


def solve(data, part2=False):
    grid = parse(data)
    end_pos = max(grid.keys())

    to_visit = [
        Crucible(0, 0, 0, "E"),
    ]
    heapify(to_visit)

    visited = {}
    while to_visit:
        current = heappop(to_visit)

        try:
            prev_visit = visited[current.x, current.y, current.directions]
            if prev_visit.heat_loss <= current.heat_loss:
                # we already visited this position with less heat loss
                continue
        except KeyError:
            pass

        visited[current.x, current.y, current.directions] = current
        if current.x == end_pos[0] and current.y == end_pos[1]:
            if not part2 or len(current.directions) >= 4:
                break
            else:
                continue

        min_dirs = 4 if part2 else 1
        max_dirs = 10 if part2 else 3

        # find next directions
        next_directions = [
            d for d in DIRECTIONS if d != OPPOSITE[current.directions[-1]]
        ]
        for d in next_directions:
            # see if we can continue in this direction
            # we can only continue for max_dirs steps in the same direction
            if len(current.directions) == max_dirs:
                if current.directions[-1] == d:
                    # cannot continue in same direction
                    continue

            if part2 and len(current.directions) < min_dirs:
                if current.directions[-1] != d:
                    # cannot only continue in same direction
                    continue

            # see if the direction is valid
            n_offset = DIRECTIONS[d]
            next_x = current.x + n_offset[0]
            next_y = current.y + n_offset[1]
            try:
                next_c = grid[next_x, next_y]
            except KeyError:
                # out of bounds
                continue

            next_crucible = Crucible(
                current.heat_loss + int(next_c),
                next_x,
                next_y,
                # add direction if same else start new
                current.directions + d if current.directions[-1] == d else d,
            )
            heappush(to_visit, next_crucible)

    return current.heat_loss


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 102


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 1013


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 94


EXAMPLE_DATA2 = """\
111111111111
999999999991
999999999991
999999999991
999999999991
"""


def test_example2b():
    result = solve(EXAMPLE_DATA2, part2=True)
    print(f"example 2b: {result}")
    assert result == 71


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 1215


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read().strip()


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_example2b()
    test_part2()
