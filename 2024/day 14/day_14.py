"""
Advent of Code 2024 - Day 14
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

from collections import Counter
from functools import reduce
from math import lcm

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

def print_positions(positions, W, H):   
    print() 
    for y in range(H):
        for x in range(W):
            n = positions[(x, y)]
            print(n if n > 0 else ".", end="")
        print()

def solve(data, W=101, H=103, part2=False):
    result = 0

    robots = []
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        p_str, v_str = line.strip().split(" ")
        p = tuple(map(int, p_str[2:].split(",")))
        v = tuple(map(int, v_str[2:].split(",")))
        robots.append((p, v))
    
    DEBUG = False
    if part2:
        # find the first time when all robots are at different positions
        maxT = W*H # upper bound for the search, not really needed but good to add
        for t in range(1, maxT):
            positionsT = Counter()
            for p, v in robots:
                pT = (p[0] + t * v[0]) % W, (p[1] + t * v[1]) % H
                positionsT[pT] += 1
                if positionsT[pT] > 1:
                    break
            else:
                # no break so all positions are visited max once
                print_positions(positionsT, W, H) # print the tree
                return t
        raise ValueError("No solution found for part 2")

    # part 1
    T = 100
    positionsT = Counter()
    for p, v in robots:
        pT = (p[0] + T * v[0]) % W, (p[1] + T * v[1]) % H
        positionsT[pT] += 1

    if DEBUG:
        print_positions(positionsT, W, H)

    quadrantsT = Counter()
    for p, n in positionsT.items():
        qX = sign(p[0] - W//2)
        qY = sign(p[1] - H//2)
        if qX != 0 and qY != 0:
            quadrantsT[(qX, qY)] += n
    result = reduce(lambda x, y: x * y, quadrantsT.values())
    return result


def test_example():
    result = solve(EXAMPLE_DATA, W=11, H=7)
    print(f"example: {result}")
    assert result == 12


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 229839456


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 7138


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()