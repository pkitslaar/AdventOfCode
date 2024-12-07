"""
Advent of Code 2024 - Day 07
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

OPERANDS = {'+': int.__add__, '*': int.__mul__}
OPERANDS2 = {'+': int.__add__, '*': int.__mul__, '||': lambda a,b: int(f'{a}{b}')}

from itertools import product


def solve(data, part2=False):
    OPS = OPERANDS2 if part2 else OPERANDS
    matches = []
    for line in data.splitlines():
        test_str, arguments_str = line.split(':')
        test_value = int(test_str)
        arguments = [int(a) for a in arguments_str.split()]

        num_op_positions = len(arguments) - 1
        for ops in product(OPS, repeat=num_op_positions):
            v = arguments[0]
            for op, arg in zip(ops, arguments[1:]):
                v = OPS[op](v, arg)
            if v == test_value:
                matches.append((test_value, arguments, ops))
    return sum(set(test_value for test_value, _, _ in matches))


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 3749


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 6231007345478


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 11387


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 333027885676693


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()