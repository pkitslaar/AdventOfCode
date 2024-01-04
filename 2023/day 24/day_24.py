"""
Advent of Code 2023 - Day 24
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

from collections import namedtuple

Position = namedtuple("Position", "x y z")
Velocity = namedtuple("Velocity", "x y z")
HailStone = namedtuple("HailStone", "name position velocity")

from enum import Enum

class CollisionType(Enum):
    never = 0
    collision = 1
    always = 2

TimeRange = namedtuple("TimeRange", "t0 t1")
#CollisionTT = namedtuple("CollisionTT", "type t0 t1")


# equation to in one dimension to find the time of collision
# x0(t) = x0 + v0*t
# x1(t) = x1 + v1*t
# x0(t) == x1(t)
# x0 + v0*t == x1 + v1*t
# t = (x0 - x1) / (v1 - v0)

def find_collision(hs1, hs2, dimension):
    x0, v0 = hs1.position[dimension], hs1.velocity[dimension]
    x1, v1 = hs2.position[dimension], hs2.velocity[dimension]
    if v0 == v1:
        if x0 == x1:
            return (CollisionType.always, 0, 0)
        else:
            return (CollisionType.never, 0, 0)
    t = (x0 - x1) / (v1 - v0)
    return (CollisionType.collision, t, x0 + v0 * t)

from itertools import combinations
from collections import defaultdict

LETTERS = "ABCDEFGHIJ"

def parse(data):
    stones = []
    for i, line in enumerate(data.splitlines()):
        name = "".join([LETTERS[int(d)] for d in str(i)])
        p, v = line.split(" @ ")
        p = Position(*map(float, p.split(", ")))
        v = Velocity(*map(float, v.split(", ")))
        stones.append(HailStone(name, p, v))
    return stones

def solve(data, min_pos=7, max_pos=27, part2=False):
    stones = parse(data)
   
    # convert stone posisions x(t), y(t) to y(x) = f(x)
    s_functions = {}
    for s in stones:
        # x(t) = x0 + v0 * t
        # t = (x - x0) / v0
        # y(t) = y0 + v1 * t
        # y(x) = y0 + v1 * ((x - x0) / v0)
        # y(x) = y0 + v1 * ((x / v0) - (x0 / v0))
        # y(x) = y0 + v1 * (x / v0) - v1 * (x0 / v0)
        # y(x) = y0 - v1 * (x0 / v0) + (v1 / v0)*x
        # y(x) = A + B * x
        x0, y0 = s.position[:2]
        v0, v1 = s.velocity[:2]

        A = y0 - v1 * (x0 / v0)
        b = v1 / v0
        func = lambda x: A + b * x
        #assert func(x0) == y0
        #assert func(x0 + v0) == y0 + v1
        s_functions[s] = (A, b, func)


    final_collisions = {}
    for s1, s2 in combinations([*s_functions.keys()], 2):
        # y1 = s1A + s1b * x
        s1A, s1b, s1_f = s_functions[s1]
        # y2 = s2A + s2b * x
        s2A, s2b, s2_f = s_functions[s2]

        # find intersection
        # s1A + s1b * x == s2A + s2b * x
        # s1A - s2A == (s2b - s1b) * x
        # x = (s1A - s2A) / (s2b - s1b)
        if s1b == s2b:
            if s1A == s2A:
                final_collisions[(s1.name, s2.name)] = (CollisionType.always, 0, 0)
            else:
                continue
        else:
            x = (s2A - s1A) / (s1b - s2b)
            t0 = (x - s1.position[0]) / s1.velocity[0]
            if t0 < 0:
                continue
            t1 = (x - s2.position[0]) / s2.velocity[0]
            if t1 < 0:
                continue
            if x >= min_pos and x <= max_pos:
                y = s1A + s1b * x
                if y >= min_pos and y <= max_pos:
                    final_collisions[(s1.name, s2.name)] = (CollisionType.collision, x, y)
         
    result = len(final_collisions)
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 2


def test_part1():
    min_pos = 200000000000000
    max_pos = 400000000000000
    result = solve(data(), min_pos=min_pos, max_pos=max_pos)
    print("Part 1:", result)
    assert result > 10359
    assert result < 600369
    assert result < 37901
    assert result == 16589

def solve2(data):
    stones = parse(data)

    # x y z vx vy vz 
    
    result = 0
    return result

def test_example2():
    result = solve2(EXAMPLE_DATA)
    print(f"example 2: {result}")
    assert result == -1


def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result == -1


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()