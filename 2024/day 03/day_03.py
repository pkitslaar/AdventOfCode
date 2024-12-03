"""
Advent of Code 2024 - Day 03
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

EXAMPLE_DATA2 = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""	

import re
MUL_REGEX = re.compile(r"""mul   # start with mul
                            \(   # open parenthesis
                                (\d{1,3}) # group of 1-3 digits
                                ,  # comma
                                (\d{1,3}) # group of 1-3 digits
                            \) # closing parenthesis
                       """, re.VERBOSE)

DO_REGEX = re.compile(r"do\(\)")
DONT_REGEX  = re.compile(r"don't\(\)")	

def solve(data, part2=False):
    result = 0
    all_matches = [*MUL_REGEX.finditer(data)]
    if part2:
        do = [*DO_REGEX.finditer(data)]
        all_matches.extend(do)
        dont = [*DONT_REGEX.finditer(data)]
        all_matches.extend(dont)
        
        all_matches.sort(key=lambda x: x.span())
        prev_do = True
        new_matches = [] 
        for m in all_matches:
            if m.group() == "do()":
                prev_do = True
            elif m.group() == "don't()":
                prev_do = False
            else:
                if prev_do:
                    new_matches.append(m)
        all_matches = new_matches   


    result = sum(int(m.group(1)) * int(m.group(2)) for m in all_matches)
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 161


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 188741603


def test_example2():
    result = solve(EXAMPLE_DATA2, part2=True)
    print(f"example 2: {result}")
    assert result == 48


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 67269798


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()