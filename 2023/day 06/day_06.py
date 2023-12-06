"""
Advent of Code 2023 - Day 06
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
Time:      7  15   30
Distance:  9  40  200
"""

from functools import reduce


def solve(data):
    lines = data.splitlines()
    times = [*map(int, lines[0].split(":")[1].split())]
    distances = [*map(int, lines[1].split(":")[1].split())]

    ways_to_win = []
    for t, d in zip(times, distances):
        num_ways = 0
        for dt in range(t):
            speed = dt
            travelled = (t - dt) * speed
            if travelled > d:
                num_ways += 1
        ways_to_win.append(num_ways)

    result = reduce(lambda x, y: x * y, ways_to_win)
    return result


import math


def solve2(data):
    lines = data.splitlines()
    T = int(lines[0].split(":")[1].replace(" ", ""))
    D = int(lines[1].split(":")[1].replace(" ", ""))
    """
    speed = t
    travelled = (T-t)*speed

    travelled = (T-t)*t
    travelled = T*t - t*t

    win = travelled > D
    win = T*t - t*t > D
    win => T*t - t*t - D > 0
    win => -t^2 + T*t - D > 0
    win => a*t^2 + b*t + c = 0
    a = -1 
    b = T 
    c = -D    
    win => t = (-b +- sqrt(b^2 - 4*a*c)) / (2*a)
    """
    a = -1
    b = T
    c = -D

    DET = b * b - 4 * a * c
    t0 = int((-b + DET**0.5) / (2 * a))
    t1 = int((-b - DET**0.5) / (2 * a))
    result = t1 - t0
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 288


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 781200


def test_example2():
    result = solve2(EXAMPLE_DATA)
    print(f"example 2: {result}")
    assert result == 71503


def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result == 49240091


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
