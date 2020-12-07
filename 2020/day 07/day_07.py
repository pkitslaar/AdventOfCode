"""
Advent of Code 2020 - Day 07
Pieter Kitslaar
"""

from pathlib import Path
from collections import defaultdict

example="""\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

def parse(txt):
    bags = {}
    for line in txt.splitlines():
        line = line[:-1] # strip '.' at end
        containing_bags, contains = line.split('contain')
        container_bag = containing_bags.strip()[:-1] # strip 's' from bags
        container_info = bags.setdefault(container_bag, {})
        if 'no other' in contains:
            pass
        else:
            for child_bag_txt in contains.split(','):
                number_txt, name = child_bag_txt.strip().split(' ',1)
                number = int(number_txt)
                if number > 1:
                    name = name[:-1] # strip 's'
                container_info[name]=number
    return bags

def reverse_loopup(bags, child, result = None):
    if result is None:
        result = set()
    for bag, contains in bags.items():
        if child in contains:
            result.add(bag)
            reverse_loopup(bags, bag, result)
    return result


def test_example():
    bags = parse(example)
    outer_bags = reverse_loopup(bags, 'shiny gold bag')
    assert(4 == len(outer_bags))


def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    bags = parse(get_input())
    outer_bags = reverse_loopup(bags, 'shiny gold bag')
    answer = len(outer_bags)
    assert(289 == answer)
    print('Part 1:', answer)


def contains(bags, outer_bag, multiplicity=1, result = None):
    if result is None:
        result = defaultdict(int)
    for child, number in bags[outer_bag].items():
        result[child]+=number*multiplicity
        contains(bags, child, number*multiplicity, result)
    return result

def test_example_part2a():
    bags = parse(example)
    result = contains(bags, 'shiny gold bag')
    total = sum([v for v in result.values()])
    assert(32 == total)

example2 = """\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""

def test_example_part2b():
    bags = parse(example2)
    result = contains(bags, 'shiny gold bag')
    total = sum([v for v in result.values()])
    assert(126 == total)

def test_part2():
    bags = parse(get_input())
    result = contains(bags, 'shiny gold bag')
    total = sum([v for v in result.values()])
    assert(30055 == total)
    print('Part 2:', total)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example_part2a()
    test_example_part2b()
    test_part2()
            
            