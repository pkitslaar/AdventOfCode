"""
Advent of Code 2024 - Day 16
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

EXAMPLE_DATA_2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

def parse(data):
    lines = data.strip().splitlines()
    grid = {}
    start = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "S":
                start = (x, y)
                c = "."
            grid[(x, y)] = c
    return grid, start

from collections import namedtuple
from heapq import heappop, heappush, heapify

State = namedtuple("State", "cost pos direction prev_state")
DIRECTIONS = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
TURNS = {'>': '^v', '<': 'v^', '^': '<>', 'v': '><'}

def find_optimal_path(grid, start, find_all = False, max_cost = None):
    visited = {}
    explored = {}
    queue = [State(0, start, '>', None)]
    found_states = []
    while queue:
        current = heappop(queue)
        print(current.cost, len(queue))
        if found_states and current.cost > found_states[0].cost:
            break # found all
        c_state = (current.pos, current.direction)  if find_all else current.pos
        visited[c_state] = current.cost
        if grid[current.pos] == "E":
            if not find_all:
                return current.cost
            else:
                found_states.append(current)
                continue
        
        dxy = DIRECTIONS[current.direction]
        n_pos = (current.pos[0] + dxy[0], current.pos[1] + dxy[1])
        n_cost = current.cost + 1
        v_state = (n_pos, current.direction) if find_all else n_pos
        if grid.get(n_pos, "#") != "#" and (v_state not in visited or n_cost <= visited[v_state]):
            heappush(queue, State(n_cost, n_pos, current.direction, current))
            explored[v_state] = n_cost
        for new_direction in TURNS[current.direction]:
            n_dxy = DIRECTIONS[new_direction]
            n_pos = (current.pos[0] + n_dxy[0], current.pos[1] + n_dxy[1])
            n_cost = current.cost + 1000 + 1
            v_state = (n_pos, new_direction) if find_all else n_pos
            if grid.get(n_pos, "#") != "#" and (v_state not in visited or n_cost <= visited[v_state]):
                heappush(queue, State(n_cost, n_pos, new_direction, current))
                explored[v_state] = n_cost
    
    all_positions = set()
    for s in found_states:
        while s is not None:
            all_positions.add(s.pos)
            s = s.prev_state

    return len(all_positions)
        


def solve(data, part2=False):
    grid, start = parse(data)
    min_cost = find_optimal_path(grid, start, find_all=False)
    if not part2:
        return min_cost
    return find_optimal_path(grid, start, find_all=True, max_cost=min_cost)


def test_example_p1_a():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 7036

def test_example_p1_b():
    result = solve(EXAMPLE_DATA_2)
    print(f"example: {result}")
    assert result == 11048

def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 94444


def test_example_p2_a():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 45

def test_example_p2_b():
    result = solve(EXAMPLE_DATA_2, part2=True)
    print(f"example 2: {result}")
    assert result == 64


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result > 458 # to low, apparently this is the solution for another input
    assert result == 502


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()