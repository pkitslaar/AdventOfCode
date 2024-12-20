"""
Advent of Code 2024 - Day 20
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

def parse(data):
    grid = {}
    S, E = None, None
    for y, line in enumerate(data.strip().splitlines()):
        for x, c in enumerate(line):
            if c == 'S':
                S = (x, y)
                c = '.'
            if c == 'E':
                E = (x, y)
                c = '.'
            grid[(x, y)] = c
    return grid, S, E

def all_cheat_pairs(grid):
    pairs = {}
    for (x, y), c in grid.items():
        if c == '.':
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                end_p = (x+2*dx, y+2*dy)
                if end_p in grid and grid[end_p] == '.':
                    mid_p = (x+dx, y+dy)
                    if grid[mid_p] == '#':
                        # no need to cheat if the mid point is not a wall
                        pairs[((x, y), mid_p)] = end_p
    return pairs

from heapq import heappop, heappush

def fastest_path(grid, S, E, cheat_pair=None):
    queue = [(0, S)]
    visited = set()
    while queue:
        cost, pos = heappop(queue)
        if pos == E:
            return cost
        if pos in visited:
            continue
        visited.add(pos)
        for dx, dy in [(0, 1), (1, 0),(0, -1), (-1, 0)]:
            new_pos = (pos[0]+dx, pos[1]+dy)
            new_cost = cost + 1
            is_cheat = (pos, new_pos) == cheat_pair
            if is_cheat:
                new_pos = (new_pos[0]+dx, new_pos[1]+dy)
                new_cost = cost + 2
            if new_pos in grid and grid[new_pos] != '#' and new_pos not in visited:
                heappush(queue, (new_cost, new_pos))
    return None

from collections import Counter

def print_grid(grid, cheat_pair = None):
    g_copy = grid.copy()
    if cheat_pair:
        (x, y), (mx, my) = cheat_pair
        dx, dy = mx-x, my-y
        g_copy[(mx, my)] = '1'
        g_copy[(mx+dx, my+dy)] = '2'
    max_x = max(x for x, y in g_copy)
    max_y = max(y for x, y in g_copy)
    print()
    print(cheat_pair)
    for y in range(max_y+1):
        print(''.join(g_copy.get((x, y), '#') for x in range(max_x+1)))

DEBUG = False
from tqdm import tqdm

def solve(data, min_saving, part2=False):
    grid, S, E = parse(data)
    base_time = fastest_path(grid, S, E)
    cheat_pair_time = {}
    cheat_pairs = all_cheat_pairs(grid)
    for cheat_pair in tqdm(cheat_pairs):
        if DEBUG:
            print_grid(grid, cheat_pair)

        result = fastest_path(grid, S, E, cheat_pair=cheat_pair)
        if DEBUG:
            print(result, base_time - result)
        if result is not None:
            cheat_pair_time[cheat_pair] = result
    
    time_savings = Counter()
    for _, time in cheat_pair_time.items():
        time_savings[base_time - time] += 1
    result = sum(n for t, n in time_savings.items() if t >= min_saving)
    return result


def test_example():
    result = solve(EXAMPLE_DATA, 64)
    print(f"example: {result}")
    assert result == 1


def test_part1():
    result = solve(data(), min_saving=100)
    print("Part 1:", result)
    assert result == -1


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == -1


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == -1


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
    

if __name__ == "__main__":
    #test_example()
    test_part1()
    #test_example2()
    #test_part2()
    #print("done")