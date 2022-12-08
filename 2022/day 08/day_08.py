"""
Advent of Code 2022 - Day 08
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

EXAMPLE_DATA="""\
30373
25512
65332
33549
35390"""

import numpy as np

def solve(d):
    grid = np.array([[*map(int,row)] for row in d.strip().splitlines()])
    h, w = grid.shape
    interior_visible = set()
    for y in range(1,h-1):
        for x in range(1,w-1):
            this_v = grid[y,x]
            visible_from = []
            if ((np.max(grid[:y,x]) < this_v)):
                visible_from.append('TOP')
            if (np.max(grid[y+1:,x]) < this_v):
                visible_from.append('BOTTOM')
            if (np.max(grid[y,:x]) < this_v):
                visible_from.append('LEFT')
            if (np.max(grid[y,x+1:]) < this_v):
                visible_from.append('RIGHT')
            if visible_from:
                interior_visible.add((y,x))
    total_visible = len(interior_visible) + 2*w+2*h-4
    return total_visible, interior_visible

def test_example():
    result, _ = solve(EXAMPLE_DATA)
    assert(21 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)

def scenic_scores(d):
    _, interior_visible = solve(d)
    grid = np.array([[*map(int,row)] for row in d.strip().splitlines()])
    h, w = grid.shape
    scores = np.zeros_like(grid)
    for y, x in interior_visible:
            this_v = grid[y,x]
            views = []
            TOP_TREES = grid[:y,x][::-1]
            BOTTOM_TREES = grid[y+1:,x]
            LEFT_TREES = grid[y,:x][::-1]
            RIGHT_TREES = grid[y,x+1:]
            for trees in (TOP_TREES, BOTTOM_TREES, LEFT_TREES, RIGHT_TREES):
                visible = 0
                for n in trees:
                    visible += 1
                    if n >= this_v:
                        break
                if visible:
                    views.append(visible)
            scores[y,x] = np.prod(views) if views else 0
    return np.max(scores)

def test_example2():
    result = scenic_scores(EXAMPLE_DATA)
    assert(8 == result)

def test_part2():
    result = scenic_scores(data())
    print('PART 2:', result)
    assert(180000 == result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()

