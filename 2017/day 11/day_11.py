"""
Advent of Code 2017 - Day 11
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

# Using cube coordinates
# https://www.redblobgames.com/grids/hexagons/#distances-cube
DIRECTION_TO_OFFSET = {
    #       q,  r,  s
    'n':  ( 0, -1,  1),
    'nw': (-1,  0,  1),
    'ne': ( 1, -1,  0),
    'sw': (-1,  1,  0),
    'se': ( 1,  0, -1),
    's':  ( 0,  1, -1)
}

def distance(pos):
    return (abs(pos[0])+abs(pos[1])+abs(pos[2])) // 2


def solve(d):
    pos = [0,0,0]
    max_dist = 0
    for d in d.strip().split(','):
        offset = DIRECTION_TO_OFFSET[d]
        pos[0] += offset[0]
        pos[1] += offset[1]
        pos[2] += offset[2]
        max_dist = max([max_dist, distance(pos)])
    return distance(pos), max_dist

def test_example():
    assert(3 == solve('ne,ne,ne')[0])
    assert(0 == solve('ne,ne,sw,sw')[0])
    assert(2 == solve('ne,ne,s,s')[0])
    assert(3 == solve('se,sw,se,sw,sw')[0])

def test_solution():
    result, result2 = solve(data())
    print('PART 1:', result)
    assert(650 == result)
    print('PART 2:', result2)
    assert(1465 == result2)


if __name__  == "__main__":
    test_example()
    test_solution()