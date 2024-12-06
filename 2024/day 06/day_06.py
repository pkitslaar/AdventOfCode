"""
Advent of Code 2024 - Day 06
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

from collections import namedtuple

Guard = namedtuple('Guard', 'pos direction')

def parse(data):
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c not in '.#':
                guard_start = Guard(pos=(x, y), direction=c)
                c = '.'
            grid[(x,y)] = c
    return grid, guard_start

DIRECIONS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
TURN_RIGHT = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

def trace(grid, guard):
    visited = set()
    loop_detected = False
    while guard.pos in grid:
            visited.add(guard)
            x, y = guard.pos
            dx, dy = DIRECIONS[guard.direction]
            next_pos = (x+dx, y+dy)
            next_dir = guard.direction
            if grid.get(next_pos, '.') == '#':
                # turn right
                next_dir = TURN_RIGHT[guard.direction]
                next_pos = (x, y)
            guard = Guard(pos=next_pos, direction=next_dir)
            if guard in visited:
                loop_detected = True
                break
    return visited, loop_detected

def solve(data, part2=False):
    grid, guard_start = parse(data)
    visited, _ = trace(grid, guard_start)
    if not part2:
        return len({g.pos for g in visited})
    
    # part 2
    # try to place obstacles anwhere on the path of the guard
    # avoid the start position of the guard
    loop_obstacle_positions = set()
    for g in visited:
        if g.pos == guard_start.pos:
            continue
        if g.pos in loop_obstacle_positions:
            # skip positions that are already part of a "previous" loop
            continue

        # temporarily place obstacle and check if a loop is detected
        # this is a bit brute force, but it works
        # better might be to do some backtracking so the inital
        # trace does not need to be repeated
        grid[g.pos] = '#' # place obstacle
        _, loop_detected = trace(grid, guard_start)
        grid[g.pos] = '.' # remove obstacle

        if loop_detected:
            loop_obstacle_positions.add(g.pos)
    return len(loop_obstacle_positions)


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 41


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 4778


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 6


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 1618


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
