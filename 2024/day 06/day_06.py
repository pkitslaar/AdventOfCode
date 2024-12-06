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

def trace(grid, guard, visit_order=None):
    visit_order = [] if visit_order is None else visit_order
    visited = set(visit_order) 
    
    loop_detected = False
    while guard.pos in grid:
            visited.add(guard)
            visit_order.append(guard)
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
    return visit_order, loop_detected

def solve(data, part2=False):
    grid, guard_start = parse(data)
    visit_order, _ = trace(grid, guard_start)
    if not part2:
        return len({g.pos for g in visit_order})
    
    # part 2
    # try to place obstacles anwhere on the path of the guard
    # avoid the start position of the guard
    tested_positions = {guard_start.pos: False}
    for i, g in enumerate(visit_order):
        if g.pos in tested_positions:
            # skip positions that have already been tested
            continue
        
        # temporarily place obstacle and check if a loop is detected
        # we start the trace from the previous known trace position
        # for performance improvements
        #         
        grid[g.pos] = '#' # place obstacle        
        prev_index = i-1        
        _, loop_detected = trace(grid, visit_order[prev_index], visit_order=visit_order[:prev_index])
        grid[g.pos] = '.' # remove obstacle

        tested_positions[g.pos] = loop_detected

    return sum(1 for v in tested_positions.values() if v)


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
