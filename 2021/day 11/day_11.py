"""
Advent of Code 2021 - Day 11
Pieter Kitslaar
"""

from pathlib import Path


example = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

example_small = """\
11111
19991
19191
19991
11111"""

def parse(txt):
    grid = {}
    for y, line in enumerate(txt.splitlines()):
        for x, energy in enumerate(line):
            grid[(x,y)] = int(energy)
    return grid

NEIGHBORS = [
    (-1,1), (-1,0), (-1,-1),
    ( 0,1),         ( 0,-1),
    ( 1,1), ( 1, 0),( 1,-1)
]

def step(grid, N=10):
    # first increase all
    for pos in grid:
        grid[pos] += 1
    #plot(grid,N)
    flashed = set()
    find_new_flashed = True
    while find_new_flashed:
        find_new_flashed = False
        new_grid = grid.copy()
        for p, e in grid.items():
            if e > 9:
                flashed.add(p)
                new_grid[p] = 0
                for n in NEIGHBORS:
                    n_pos = (p[0]+n[0], p[1]+n[1])
                    if n_pos in grid and not n_pos in flashed:
                        new_grid[n_pos] += 1
        grid = new_grid
        find_new_flashed = any(e > 9 for e in grid.values())
        #plot(grid,N)

    result = len(flashed)
    return result, grid

def plot(grid, N=10):
    for y in range(N):
        for x in range(N):
            v = grid[(x,y)]
            print('*' if v > 9 else v, end="")
        print()

def test_example_small():
    g = parse(example_small)
    f1, g = step(g,5)
    assert 9 == f1
    f2, g = step(g, 5)
    assert f2 == 0

def solve1(grid, num_steps, N=10):
    total_flashed = 0
    for i in range(num_steps):
        result, grid = step(grid, N)
        total_flashed += result
    return total_flashed

def test_example():
    result = solve1(parse(example), 100)
    assert 1656 == result


def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    result = solve1(parse(get_input()), 100)
    print('Part 1', result)
    assert 1679 == result

def solve2(grid):
    num_steps = 0
    while True:
        num_steps += 1
        num_flashed, grid = step(grid)
        if num_flashed == len(grid):
            return num_steps
            
def test_example2():
    result = solve2(parse(example))
    assert 195 == result

def test_part2():
    result = solve2(parse(get_input()))
    print('Part 2', result)
    assert 519 == result


if __name__ == "__main__":
    test_example_small()
    test_example()
    test_part1()
    test_example2()
    test_part2()