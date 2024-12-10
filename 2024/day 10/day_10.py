"""
Advent of Code 2024 - Day 10
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
0123
1234
8765
9876
"""

EXAMPLE_DATA_LARGE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

def parse(data):
    grid = {}
    start_positions = []
    for y, line in enumerate(data.strip().splitlines()):
        for x, c in enumerate(line):
            grid[(x,y)] = int(c) if c != '.' else 10
            if c == '0':
                start_positions.append((x,y))
    return grid, start_positions

from heapq import heapify, heappop, heappush
from collections import defaultdict

def propagate(grid, start_pos):
    q = [(grid[start_pos], start_pos)]
    heapify(q)
    
    end_positions = []
    visited = set()
    previous = defaultdict(list)
    while q:
        height, pos = heappop(q)
        if pos in visited:
            continue
        if grid[pos] == 9:
            end_positions.append(pos)
            continue

        visited.add(pos)
        x,y = pos
        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            new_pos = (x+dx, y+dy)
            if new_pos in grid and grid[new_pos] - height == 1:
                heappush(q, (grid[new_pos], new_pos))
                previous[new_pos].append(pos)
    return end_positions, previous

def solve(data, part2=False):
    grid, start_positions = parse(data)
    
    result = 0
    for start_pos in start_positions:
        end_positions, prev = propagate(grid, start_pos)
        if part2:
            # find all distinct paths to the end_positions
            for end_pos in set(end_positions):
                found_trails = []
                trails = [[end_pos]] # start with one trail at the end
                while trails:
                    t = trails.pop()
                    pos = t[-1]
                    if pos == start_pos:
                        # we found a trail
                        found_trails.append(t)
                    else:
                        # create new trails for all possible previous positions
                        for p in prev[pos]:
                            trails.append(t + [p])
                rating = len(found_trails)
                result += rating
        else:
            # just count the number of distinct end positions
            result += len(set(end_positions))
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 1

   
def test_example_large():
    result = solve(EXAMPLE_DATA_LARGE)
    print(f"example large: {result}")
    assert result == 36  


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 510

EXAMPLE2_DATA = """\
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
"""

def test_example2():
    result = solve(EXAMPLE2_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 3


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 1058


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()