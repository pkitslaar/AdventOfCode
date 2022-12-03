"""
Advent of Code 2022 - Day 03
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

EXAMPLE_DATA="""\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

def priority(item):
    if item.isupper():
        return ord(item) - 65 + 27
    return ord(item) - 96

def test_priority():
    assert(1 == priority('a'))
    assert(26 == priority('z'))
    assert(27 == priority('A'))
    assert(52 == priority('Z'))

def solve(d):
    total = 0
    for rucksack in d.strip().splitlines():
        N = len(rucksack)
        first, second = rucksack[:N//2], rucksack[N//2:]
        common_items = set(first).intersection(second)
        assert(len(common_items)==1)
        total += sum(map(priority, common_items))
    return total
     
        
def test_example():
    result = solve(EXAMPLE_DATA)
    assert(157 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)

from itertools import islice

def solve2(d):
    total = 0
    all_rucksask = list(d.strip().splitlines())
    for i_group in range(0, len(all_rucksask), 3):
        group_sacks = all_rucksask[i_group:i_group+3]
        common = set(group_sacks[0])
        for sack in group_sacks[1:]:
            common.intersection_update(set(sack))
        total += sum(map(priority, common))
    return total

def test_example2():
    result = solve2(EXAMPLE_DATA)
    assert(70 == result)

def test_part2():
    result = solve2(data())
    print('PART 2:', result)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()