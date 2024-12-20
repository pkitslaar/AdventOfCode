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

def all_cheat_pairs(grid, T=2):
    for (x, y), c in grid.items():
        if c == '.':
            for dx in range(-T, T+1):
                for dy in range(-T, T+1):
                    t = abs(dx) + abs(dy)
                    if t > T or t <= 0:
                        continue    
                    end_p = (x+dx, y+dy)
                    if end_p in grid and grid[end_p] == '.':                        
                        yield (x, y), end_p, t
                        

from heapq import heappop, heappush

def fastest_path(grid, S, E):
    queue = [(0, S)]
    visited = {}
    while queue:
        cost, pos = heappop(queue)
        visited[pos] = cost
        if pos == E:
            return visited
        for dx, dy in [(0, 1), (1, 0),(0, -1), (-1, 0)]:
            new_pos = (pos[0]+dx, pos[1]+dy)
            new_cost = cost + 1
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

def solve(data, min_saving, part2=False):
    grid, S, E = parse(data)
    arrival_times = fastest_path(grid, S, E)

    cheat_pair_saving = {}
    for cp_start, cp_end, cp_t in all_cheat_pairs(grid, T= 2 if not part2 else 20):
        #if DEBUG:
        #    print_grid(grid, cheat_pair)
        normal_start_time = arrival_times[cp_start]
        normal_end_time = arrival_times[cp_end]
        normal_duration = normal_end_time - normal_start_time
        
        cheat_saving = normal_duration - cp_t 
        cheat_pair_saving[(cp_start, cp_end)] = cheat_saving
    
    time_savings = Counter()
    for _, saving in cheat_pair_saving.items():
        time_savings[saving] += 1
    result = sum(n for t, n in time_savings.items() if t >= min_saving)
    return result


def test_example():
    result = solve(EXAMPLE_DATA, 64)
    print(f"example: {result}")
    assert result == 1


def test_part1():
    result = solve(data(), min_saving=100)
    print("Part 1:", result)
    assert result == 1296


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True, min_saving=76)
    print(f"example 2: {result}")
    assert result == 3


def test_part2():
    result = solve(data(), part2=True, min_saving=100)
    print("Part 2:", result)
    assert result == 977665


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