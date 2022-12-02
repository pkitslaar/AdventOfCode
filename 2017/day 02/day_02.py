"""
Advent of Code 2017 - Day 02
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

EXAMPLE_DATA = """\
5 1 9 5
7 5 3
2 4 6 8"""

def checksum(d):
    sum = 0
    for line in d.strip().splitlines():
        numbers = list(map(int, line.split()))
        sum += max(numbers) - min(numbers)
    return sum

assert(18 == checksum(EXAMPLE_DATA))

print('PART 1:', checksum(data()))

import itertools

def checksum2(d):
    sum = 0
    for line in d.strip().splitlines():
        numbers = list(map(int, line.split()))
        for pair in itertools.combinations(numbers, 2):
            a, b = divmod(max(pair), min(pair))
            if b == 0:
                sum += a
    return sum

EXAMPLE2_DATA = """\
5 9 2 8
9 4 7 3
3 8 6 5"""

assert(9 == checksum2(EXAMPLE2_DATA))

print('PART 2:', checksum2(data()))