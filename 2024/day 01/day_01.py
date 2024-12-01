"""
Advent of Code 2024 - Day 01
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
3   4
4   3
2   5
1   3
3   9
3   3
"""

from collections import Counter

def solve(data, part2=False):
    left, right = [], []
    for line in data.splitlines():
        a, b = map(int, line.split())
        left.append(a)
        right.append(b)

    if not part2:
        distances = []
        for pl, lr in zip(sorted(left), sorted(right)):
            distances.append(abs(lr - pl))
        result = sum(distances)
    else:
        right_counts = Counter(right)
        result = sum(l*right_counts[l] for l in left)
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 11


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 1938424


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 31


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == -1


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()