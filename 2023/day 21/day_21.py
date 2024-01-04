"""
Advent of Code 2023 - Day 21
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

from heapq import heappush, heappop, heapify
from collections import defaultdict


def parse(data):
    grid = {}
    start = None
    for y, line in enumerate(data.splitlines()):
        if line.strip():
            for x, c in enumerate(line.strip()):
                if c == "S":
                    start = (x, y)
                    c = "."
                grid[(x, y)] = c
    return grid, start


def solve(data, N=6, part2=False):
    grid, start = parse(data)
    max_y = max(y for x, y in grid)
    mod_y = max_y + 1
    max_x = max(x for x, y in grid)
    mod_x = max_x + 1

    visited_steps = defaultdict(dict)
    to_visit = [(0, start)]
    heapify(to_visit)

    sub_limit = 0 if not part2 else 4
    while to_visit:
        steps, current = heappop(to_visit)

        orig_pos = current[0] % (mod_x), current[1] % (mod_y)
        sub_key = current[0] // (mod_x), current[1] // (mod_y)
        if not sub_key in visited_steps[orig_pos]:
            visited_steps[orig_pos][sub_key] = steps
        else:
            continue

        if abs(sub_key[0]) > sub_limit or abs(sub_key[1]) > sub_limit:
            continue

        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            new = (current[0] + dx, current[1] + dy)
            test_pos = new if not part2 else (new[0] % (mod_x), new[1] % (mod_y))
            if grid.get(test_pos, "#") == "#":
                continue

            heappush(to_visit, (steps + 1, new))

    result_new = 0
    for orig_pos in visited_steps:
        # For each position in the original map we find it can also be reached
        # in all the possible copies of the map in all directions.
        # We search on the perimeter of an expanding "square" around the original map.
        radius = 0
        min_n = 0  # used to stop the radius growth if the minim_n reached is too large
        pos_results = 0
        while (
            min_n <= N or radius <= sub_limit
        ):  # always search at least sub_limit radii to prevent too soon stopping
            min_n = N + 1
            for y in range(-radius, radius + 1):
                for x in range(-radius, radius + 1):
                    if abs(x) == radius or abs(y) == radius:
                        if radius > sub_limit:
                            # we assume above this the pattern repeats
                            # and the number of steps is increased linearly for each
                            # repeat map copy direction
                            x_base = min(sub_limit, x) if x > 0 else max(-sub_limit, x)
                            y_base = min(sub_limit, y) if y > 0 else max(-sub_limit, y)
                            n_base = visited_steps[orig_pos][x_base, y_base]
                            n = (
                                n_base
                                + mod_x * abs(x - x_base)
                                + mod_y * abs(y - y_base)
                            )
                        else:
                            # we can direclty query the number of steps for this position
                            n = visited_steps[orig_pos][x, y]
                        min_n = min(min_n, n)
                        if n <= N and (N - n) % 2 == 0:
                            pos_results += 1
            radius += 1
        result_new += pos_results

    return result_new


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 16


def test_part1():
    result = solve(data(), N=64)
    print("Part 1:", result)
    assert result == 3814


def test_example2():
    """
    General solution to the example input.
    For the actual input this is too slow and a more "analytical" solution is needed.
    See test_part2 below.
    """
    assert 16 == solve(EXAMPLE_DATA, N=6, part2=True)
    assert 50 == solve(EXAMPLE_DATA, N=10, part2=True)
    assert 1594 == solve(EXAMPLE_DATA, N=50, part2=True)
    assert 6536 == solve(EXAMPLE_DATA, N=100, part2=True)
    assert 167004 == solve(EXAMPLE_DATA, N=500, part2=True)
    assert 668697 == solve(EXAMPLE_DATA, N=1000, part2=True)


def test_part2():
    """
    The solution below where we compute the quadratic equation from three points
    is derived from the following Reddit comment: https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keays65/

    This solution only works for the particular input of day 21 which has a diamond shaped pattern.
    This causes the solution to be a quadratic equation.
    This does not work for the more general input in the example.

    The basic solve function is still used to compute the first 3 values.
    And this one I derived myself, although is is probably not the most efficient way.
    """
    N = 26501365
    width = 131
    remainder = N % width
    v1 = solve(data(), N=remainder, part2=True)
    v2 = solve(data(), N=remainder + width, part2=True)
    v3 = solve(data(), N=remainder + 2 * width, part2=True)

    # * Lagrange's Interpolation formula for ax^2 + bx + c with x=[0,1,2] and y=[y0,y1,y2] we have
    # *   f(x) = (x^2-3x+2) * y0/2 - (x^2-2x)*y1 + (x^2-x) * y2/2
    # * so the coefficients are:
    # * a = y0/2 - y1 + y2/2
    # * b = -3*y0/2 + 2*y1 - y2/2
    # * c = y0

    # Rule for making a quadratic equation from three points for 0, 1 and 2.
    # my $a = ($v1 - 2*$v2 + $v3) / 2;
    # my $b = (-3*$v1 + 4*$v2 - $v3) / 2;
    # my $c = $v1;
    # my $n = int($steps / $width);
    # my $result = $a * $n * $n + $b * $n + $c;

    a = (v1 - 2 * v2 + v3) / 2
    b = (-3 * v1 + 4 * v2 - v3) / 2
    c = v1
    n = int(N / width)
    print(f"Equation: {a} n^2 + {b} n + {c}, with n = {n}")

    result = int(a * n * n + b * n + c)
    print("Part 2:", result)
    assert result == 632257949158206


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
