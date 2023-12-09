"""
Advent of Code 2023 - Day 09
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def differences(numbers):
    return [b - a for a, b in zip(numbers, numbers[1:])]


def solve(data, part2=False):
    result = 0
    for line in data.splitlines():
        # list of lists
        numbers = [[int(n) for n in line.split()]]
        while any(n != 0 for n in numbers[-1]):
            numbers.append(differences(numbers[-1]))

        # extrapolate
        prev_n = 0
        for nums in reversed(numbers[:-1]):
            prev_n = nums[-1] + prev_n if not part2 else nums[0] - prev_n
        result += prev_n

    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 114


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 1916822650


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 2


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 966


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
