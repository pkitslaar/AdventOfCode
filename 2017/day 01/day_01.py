"""
Advent of Code 2017 - Day 01
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

def sum_of_next(digits):
    sum = 0
    for i in range(len(digits)):
        if digits[i-1] == digits[i]:
            sum += int(digits[i-1])
    return sum

assert(3 == sum_of_next('1122'))
assert(0 == sum_of_next('1234'))
assert(9 == sum_of_next('91212129'))

print('PART 1:', sum_of_next(data()))

def sum_of_middle(digits):
    l = len(digits)
    offset = l // 2
    sum = 0
    for i in range(l):
        if digits[i-offset] == digits[i]:
            sum += int(digits[i-offset])
    return sum

assert(6 == sum_of_middle('1212'))
assert(0 == sum_of_middle('1221'))
assert(4 == sum_of_middle('123425'))
assert(12 == sum_of_middle('123123'))
assert(4 == sum_of_middle('12131415'))

print('PART 2:', sum_of_middle(data()))



