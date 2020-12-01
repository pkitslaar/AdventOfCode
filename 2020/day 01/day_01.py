"""
Advent of Code 2020 - Day 01
Pieter Kitslaar
"""
from pathlib import Path
from itertools import combinations
from functools import reduce

test_input = """\
1721
979
366
299
675
1456"""

def solve(numbers, num_values):
    for values in combinations(numbers,num_values):
        if sum(values) == 2020:
            return reduce(lambda a,b: a*b, values)

def test_example():
    test_numbers = list(map(int, test_input.splitlines()))
    assert( 514579 == solve(test_numbers, 2))
    assert( 241861950 == solve(test_numbers, 3))
    

def get_input():
    input_numbers = []
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        for l in f:
            input_numbers.append(int(l.strip()))
    return input_numbers

def test_part1():
    answer = solve(get_input(),2)
    assert(713184 == answer)
    print('Part 1:', answer) 

def test_part2():
    answer = solve(get_input(),3)
    assert(261244452 == answer)
    print('Part 2:', answer) 

if __name__ == "__main__":
    test_example()
    test_part1()
    test_part2()