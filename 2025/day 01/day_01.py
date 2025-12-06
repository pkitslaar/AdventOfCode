"""
Advent of Code 2025 - Day 01
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

def num_zero_point(dial_pos, amount):
    if amount < 0:
        # turn left
        if dial_pos + amount > 0:
            return dial_pos + amount, 0
        else:
            n_zero = abs((dial_pos + amount) // 100 )
            if dial_pos == 0:
                n_zero -= 1
            new_dial_pos = (dial_pos + amount) % 100
            if new_dial_pos == 0:
                n_zero += 1
            return new_dial_pos, n_zero
    else:
        # turn right
        if dial_pos + amount < 100:
            return dial_pos + amount, 0
        else:
            n_zero = (dial_pos + amount) // 100
            new_dial_pos = (dial_pos + amount) % 100
            return new_dial_pos, n_zero
    


def test_num_zero_point():
    assert num_zero_point(50, -68) == (82, 1)
    assert num_zero_point(82, -30) == (52, 0)
    assert num_zero_point(52, 48) == (0, 1)
    assert num_zero_point(0, -5) == (95, 0)
    assert num_zero_point(95, 60) == (55, 1)
    assert num_zero_point(55, -55) == (0, 1)
    assert num_zero_point(0, -1) == (99, 0)
    assert num_zero_point(99, -99) == (0, 1)
    assert num_zero_point(0, 14) == (14, 0)
    assert num_zero_point(14, -82) == (32, 1)
    assert num_zero_point(50, 1000) == (50, 10)




def solve(data, part2=False):
    result = 0
    dial_pos = 50
    for line in data.splitlines():
        direction, amount = line[0], int(line[1:])
        if direction == "L":
            amount = -amount
        new_dial_pos, n_zero = num_zero_point(dial_pos, amount)
        dial_pos = new_dial_pos
        if part2:
            result += n_zero
        else:
            if dial_pos == 0:
                result += 1
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 3


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 1023


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 6


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result < 5900
    assert result > 5687
    assert result == 5899


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()