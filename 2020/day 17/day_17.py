"""
Advent of Code 2020 - Day 17
Pieter Kitslaar
"""

from pathlib import Path
from itertools import chain

example = """\
.#.
..#
###"""

def txt_to_grid(txt):
    grid = set()
    w=0
    z=0
    for y, row in enumerate(txt.splitlines()):
        for x, cell in enumerate(row):
            if cell == '#':
                grid.add((w,z,y,x))
    return grid

def neighbors(p, use_W=False):
    W,Z,Y,X = p
    w_range = range(W-1,W+2) if use_W else [W]
    for w in w_range:
        for z in range(Z-1,Z+2):
            for y in range(Y-1,Y+2):
                for x in range(X-1,X+2):
                    n_p = w,z,y,x
                    if n_p != p:
                        yield n_p
                    

def cycle(grid, use_W=False):
    new_grid = set()
    search_points = set(chain(*(neighbors(p, use_W) for p in grid))).union(grid)
    for p in search_points:
        num_active_neighbors = sum(1 for n in neighbors(p, use_W) if n in grid)
        if p in grid:
            # currently active
            if num_active_neighbors in (2,3):
                new_grid.add(p)
        else:
            # currently not active
            if num_active_neighbors == 3:
                new_grid.add(p)
    return new_grid

def plot_grid(g):
    W,Z,Y,X = zip(*g)
    for w in range(min(W),max(W)+1):
        for z in range(min(Z),max(Z)+1):
            print("z=",z,'w=',w)
            for y in range(min(Y),max(Y)+1):
                print(''.join(['#' if (z,y,x) in g else '.' for x in range(min(X),max(X)+1)]))
            print()


def test_example():
    g = txt_to_grid(example)
    for i in range(6):
        g = cycle(g)
    assert(112 == len(g))

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    g = txt_to_grid(get_input())
    for i in range(6):
        g = cycle(g)
    answer = len(g)
    print('Part 1:', answer)

def test_example_part2():
    g = txt_to_grid(example)
    for i in range(6):
        g = cycle(g, use_W=True)
    assert(848 == len(g))

def test_part2():
    g = txt_to_grid(get_input())
    for i in range(6):
        g = cycle(g, use_W=True)
    answer = len(g)
    print('Part 2:', answer)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example_part2()
    test_part2()