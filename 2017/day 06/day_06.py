"""
Advent of Code 2017 - Day 06
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

EXAMPLE_DATA = "0 2 7 0"

def redistribute(d):
    banks = list(map(int, d.strip().split()))
    L = len(banks)

    seen = {tuple(banks): 0}
    cycles = 0
    while True:
        cycles += 1
        max_blocks = max(banks)
        max_index = banks.index(max_blocks)
        num_to_distribute = max_blocks
        banks[max_index] = 0
        current = max_index
        while num_to_distribute:
            current = (current + 1) % L
            banks[current] += 1
            num_to_distribute -= 1
        signature = tuple(banks)
        if signature in seen:
            break
        else:
            seen[signature] = cycles
    return cycles, cycles - seen[signature]


def test_example():
    result, loop_size = redistribute(EXAMPLE_DATA)
    assert(5 == result)
    assert(4 == loop_size)

def part1():
    result, loop_size = redistribute(data())
    print('PART 1:', result)
    print('PART 2:', loop_size)



if __name__ == "__main__":
    test_example()
    part1()
