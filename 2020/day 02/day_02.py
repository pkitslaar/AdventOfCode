"""
Advent of Code 2020 - Day 02
Pieter Kitslaar
"""
from pathlib import Path
from collections import Counter

test_input = """\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""

def check_valid(line, new_policy=False):
    min_max, char_raw, passwd_raw = line.split(" ",2)
    
    min_value, max_value = map(int, min_max.split('-'))
    char = char_raw[0]
    passwd = passwd_raw.strip()
    
    if not new_policy:
        passwd_char_count = Counter(passwd)
        char_count = passwd_char_count[char]
        return min_value <= char_count <= max_value
    else:
        a = passwd[min_value-1]
        b = passwd[max_value-1]
        return (a == char) ^ (b == char) # xor

def test_example():
    assert(2 == sum([check_valid(l, False) for l in test_input.splitlines()]))
    assert(1 == sum([check_valid(l, True) for l in test_input.splitlines()]))

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        for l in f:
            yield l.strip()

def test_part1():
    num_valid = sum([check_valid(l) for l in get_input()])
    assert(378 == num_valid)
    print('Part 1:', num_valid)

def test_part2():
    num_valid = sum([check_valid(l, True) for l in get_input()])
    assert(280 == num_valid)
    print('Part 2:', num_valid)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_part2()
