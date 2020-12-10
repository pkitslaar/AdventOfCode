"""
Advent of Code 2020 - Day 09
Pieter Kitslaar
"""

from pathlib import Path
from itertools import combinations

example="""\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

def parse(txt):
    return [int(i) for i in txt.splitlines()]

def find_mismatch(data, N):
    for i in range(N,len(data)):
        preamble = data[i-N:i]
        value = data[i]
        for a,b in combinations(preamble, 2):
            if a+b == value:
                break
        else: # no break
            return value, i
    return None

def find_contigous_sum(data, value, end_index):
    """
    """
    start_index = end_index - 1
    while start_index > 0:
        if data[end_index] >= value:
            print(start_index, end_index, data[end_index])
            end_index -=1
            start_index = end_index-1
        else:
            current_sum = sum(data[start_index:end_index])
            print(start_index, end_index, current_sum)
            if current_sum == value:
                return start_index, end_index
            elif current_sum > value:
                end_index -= 1
            else: # current_sum < value
                start_index -= 1
    return None, None

def test_example():
    data = parse(example)
    mismatch, _ = find_mismatch(data, 5)
    assert(127 == mismatch)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    data = parse(get_input())
    mismatch, location = find_mismatch(data, 25)
    assert(138879426 == mismatch)
    print('Part 1:', mismatch)
    print(location)

def compute_weakness(txt, N):
    data = parse(txt)
    mismatch, location = find_mismatch(data, N)
    s, e = find_contigous_sum(data, mismatch, location)
    lowest = min(data[s:e])
    highest = max(data[s:e])
    return lowest+highest
    

def test_example_part2():
    weakness = compute_weakness(example, 5)
    assert(62 == weakness)


def test_part2():
    weakness = compute_weakness(get_input(), 25)
    print('Part 2:', weakness)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example_part2()
    test_part2()
