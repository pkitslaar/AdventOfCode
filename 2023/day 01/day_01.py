"""
Advent of Code 2023 - Day 01
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

EXAMPLE_DATA = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

import re
# find only digits
DIGIT_RE = re.compile('\d')   

# find digits (e.g. 1,2,3 ) or digit words (e.g. one, two, three)
# The value for normal digits is None so we can test on it later
WORD_VALUES = {'\d': None,
                'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 
               'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'zero': 0}
DIGIT_WORD_RE = re.compile("|".join(f"{dw}" for dw in WORD_VALUES.keys()))
def solve(data, part2=False):
    result = 0
    RE = DIGIT_WORD_RE if part2 else DIGIT_RE
    for l in data.splitlines():
        # start of search
        s = 0
        digit_words = []
        while m := RE.search(l, s):
            digit_words.append(m.group())
            s = m.span()[1]
            # we want overlapping search so for longer matches we 
            # set the search start back one character
            if len(digit_words[-1]) > 1: 
                s -= 1
        digits = [str(WORD_VALUES.get(dw, dw)) for dw in digit_words]
        result += int(digits[0] + digits[-1])
    return result

def test_example():
    result = solve(EXAMPLE_DATA)
    print(f'example: {result}')
    assert result == 142

def test_part1():
    result = solve(data())
    print('Part 1:', result)
    assert result == 55017

EXAMPLE_DATA2 = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""	

def test_example2():
    result = solve(EXAMPLE_DATA2, part2=True)
    print(f'example 2: {result}')
    assert result == 281

def test_part2():
    result = solve(data(), part2=True)
    print('Part 2:', result)
    assert result == 53539
