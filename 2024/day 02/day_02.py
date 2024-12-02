"""
Advent of Code 2024 - Day 02
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

def is_safe(levels):
    diff = [r-l for l, r in zip(levels, levels[1:])]
    abs_diff = [abs(d) for d in diff]
    is_safe = True
    if min(abs_diff) < 1 or max(abs_diff) > 3:
        # unsafe
        is_safe = False
    else:    
        signs = {d/d2 for d, d2 in zip(diff, abs_diff)}
        if len(signs) > 1:
            is_safe = False
    return is_safe


def solve(data, part2=False):
    num_safe = 0
    for line in data.splitlines():
        levels = list(map(int, line.split()))
        if is_safe(levels):
                num_safe += 1
        else:
            if part2:
                for i in range(len(levels)):
                    t_levels = levels[:i] + levels[i+1:]
                    if is_safe(t_levels):
                        num_safe += 1
                        break
    result = num_safe
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 2


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 269


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 4


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result > 320 # initially missed exccluding last element
    assert result == 337


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()