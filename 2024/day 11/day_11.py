"""
Advent of Code 2024 - Day 11
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
0 1 10 99 999
"""

from functools import lru_cache

def parse(data):
    return list(map(int, data.strip().split()))

def blink(stones):
    new_stones = []
    for s in stones:
        if s == 0:
            new_stones.append(1)
        elif len(str(s)) % 2 == 0:
            s_str = str(s)
            mid = len(s_str)//2
            new_stones.append(int(s_str[:mid]))
            new_stones.append(int(s_str[mid:]))
        else:
            new_stones.append(s*2024)
    return new_stones

def blink_n(stones, n):
    for _ in range(n):
        stones = blink(stones)
    return stones

@lru_cache(maxsize=None) # make sure to cache all the results (e.g. maxsize=None), default is 128
def blink_fast(stone, N):
    if N <= 0:
        return 1
    s_str = str(stone)
    if stone == 0:
        return blink_fast(1, N-1)
    elif len(s_str) % 2 == 0:
        mid = len(s_str)//2
        b_l = blink_fast(int(s_str[:mid]), N-1)
        b_r = blink_fast(int(s_str[mid:]), N-1)
        return  b_l + b_r 
    else:
        return blink_fast(stone*2024, N-1)


def test_blink():
    new_stones = blink(parse(EXAMPLE_DATA))
    assert new_stones == parse("1 2024 1 0 9 9 2021976")

def test_blink_n():
    new_stones = blink_n(parse("125 17"), 6)
    assert new_stones == parse("2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2")

def solve(data, part2=False):
    N = 25 if not part2 else 75
    stones = parse(data)
    new_stones = blink_n(stones, N)
    result = len(new_stones)
    return result

def solve_fast(data, part2=False):
    N = 25 if not part2 else 75
    stones = parse(data)
    result = sum(blink_fast(s, N) for s in stones)
    return result

def test_example():
    result = solve("125 17")
    print(f"example: {result}")
    assert result == 55312
    assert solve_fast("125 17") == 55312


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 222461
    assert solve_fast(data()) == 222461


def test_example2():
    result = solve_fast(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 149161030616311

def test_part2():
    result = solve_fast(data(), part2=True)
    print("Part 2:", result)
    assert result == 264350935776416


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()