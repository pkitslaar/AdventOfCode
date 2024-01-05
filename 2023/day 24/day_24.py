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
        # assert func(x0) == y0
        # assert func(x0 + v0) == y0 + v1
        s_functions[s] = (A, b)

    final_collisions = {}
    for s1, s2 in combinations([*s_functions.keys()], 2):
        # y1 = s1A + s1b * x
        s1A, s1b = s_functions[s1]
        # y2 = s2A + s2b * x
        s2A, s2b = s_functions[s2]

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
                    final_collisions[(s1.name, s2.name)] = (
                        CollisionType.collision,
                        x,
                        y,
                    )

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


import numpy as np


def solve2(data):
    """
    Based on equation derivations from
    https://github.com/jmd-dk/advent-of-code/blob/main/2023/solution/24/solve.py

        for two hailstones i and j yields
            + P[0]*(v_j[1] - v_i[1])
            - P[1]*(v_j[0] - v_i[0])
            + V[1]*(p_j[0] - p_i[0])
            - V[0]*(p_j[1] - p_i[1])
            =
            - p_i[0]*v_i[1]
            + p_i[1]*v_i[0]
            + p_j[0]*v_j[1]
            - p_j[1]*v_j[0]
        From symmetry we get corresponding equations for ([1], [2]) and ([2], [0]).
        These are 3 linear equations in 6 unknowns. Adding a third hailstone, k,
        we can extend the system of equations with three similar equations from
        e.g. (j, k).

    I redid the derivation on paper (so I did put in some effort) and got the same equations.

    I next filled in the matrix using an used numpy to solve the linear equations.
    GitHub COPILOT did help with writing out the repetative code to fill the matrix.
    """
    stones = parse(data)

    # Use the numpy library to solve the linear equations

    # The equations are linear in the unknowns, so we can use numpy to solve them
    # The unknowns are the position and velocity of the first stone

    A = np.zeros((6, 6))
    # Columns are
    # P[0] P[1] P[2] V[0] V[1] V[2]
    b = np.zeros((6, 1))
    for i, (s1, s2) in enumerate([(stones[0], stones[1]), (stones[0], stones[2])]):
        # for X, Y
        #       + P[0]*(v_j[1] - v_i[1]) - P[1]*(v_j[0] - v_i[0]) + V[1]*(p_j[0] - p_i[0]) - V[0]*(p_j[1] - p_i[1])
        # =     - p_i[0]*v_i[1] + p_i[1]*v_i[0] + p_j[0]*v_j[1] - p_j[1]*v_j[0]
        P0 = s2.velocity[1] - s1.velocity[1]
        P1 = s1.velocity[0] - s2.velocity[0]
        V1 = s2.position[0] - s1.position[0]
        V0 = s1.position[1] - s2.position[1]
        b_xy = (
            -s1.position[0] * s1.velocity[1]
            + s1.position[1] * s1.velocity[0]
            + s2.position[0] * s2.velocity[1]
            - s2.position[1] * s2.velocity[0]
        )
        A[3 * i, :] = [P0, P1, 0, V0, V1, 0]
        b[3 * i, :] = b_xy

        # for Y, Z
        #       + P[1]*(v_j[2] - v_i[2]) - P[2]*(v_j[1] - v_i[1]) + V[2]*(p_j[1] - p_i[1]) - V[1]*(p_j[2] - p_i[2])
        # =     - p_i[1]*v_i[2] + p_i[2]*v_i[1] + p_j[1]*v_j[2] - p_j[2]*v_j[1]
        P1 = s2.velocity[2] - s1.velocity[2]
        P2 = s1.velocity[1] - s2.velocity[1]
        V2 = s2.position[1] - s1.position[1]
        V1 = s1.position[2] - s2.position[2]
        b_yz = (
            -s1.position[1] * s1.velocity[2]
            + s1.position[2] * s1.velocity[1]
            + s2.position[1] * s2.velocity[2]
            - s2.position[2] * s2.velocity[1]
        )
        A[3 * i + 1, :] = [0, P1, P2, 0, V1, V2]
        b[3 * i + 1, :] = b_yz

        # for Z, X
        #       + P[2]*(v_j[0] - v_i[0]) - P[0]*(v_j[2] - v_i[2]) + V[0]*(p_j[2] - p_i[2]) - V[2]*(p_j[0] - p_i[0])
        # =     - p_i[2]*v_i[0] + p_i[0]*v_i[2] + p_j[2]*v_j[0] - p_j[0]*v_j[2]
        P2 = s2.velocity[0] - s1.velocity[0]
        P0 = s1.velocity[2] - s2.velocity[2]
        V0 = s2.position[2] - s1.position[2]
        V2 = s1.position[0] - s2.position[0]
        b_zx = (
            -s1.position[2] * s1.velocity[0]
            + s1.position[0] * s1.velocity[2]
            + s2.position[2] * s2.velocity[0]
            - s2.position[0] * s2.velocity[2]
        )
        A[3 * i + 2, :] = [P0, 0, P2, V0, 0, V2]
        b[3 * i + 2, :] = b_zx

    x = np.linalg.solve(A, b).flatten()
    result = round(sum(x[:3]))  # add the position values
    return result


import sympy as sp


def solve2_sympy(data):
    """
    Taken from https://github.com/mgtezak/Advent_of_Code/blob/master/2023/Day_24.py

    This was used to obtain the initial solution for Part 2.
    I next re-wrote the solution using numpy to solve the linear equations.
    """
    stones = parse(data)

    unknowns = sp.symbols("x y z dx dy dz t1 t2 t3")
    x, y, z, dx, dy, dz, *time = unknowns

    equations = []  # build system of 9 equations with 9 unknowns
    for t, h in zip(time, stones[:3]):
        equations.append(sp.Eq(x + t * dx, h.position[0] + t * h.velocity[0]))
        equations.append(sp.Eq(y + t * dy, h.position[1] + t * h.velocity[1]))
        equations.append(sp.Eq(z + t * dz, h.position[2] + t * h.velocity[2]))

    solution = sp.solve(equations, unknowns).pop()
    return int(sum(solution[:3]))


def test_example2():
    result = solve2(EXAMPLE_DATA)
    print(f"example 2: {result}")
    assert result == 47


def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result == 781390555762385


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
