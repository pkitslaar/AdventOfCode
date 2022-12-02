"""
Advent of Code 2017 - Day 05
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

EXAMPLE_DATA = """\
0
3
0
1
-3"""

def solve(d, part2=False):
    instructions = list(map(int, d.splitlines()))
    L = len(instructions)
    i = 0
    steps = 0
    while i < L:
        steps += 1
        offset = instructions[i]
        if part2:
            if offset >= 3:
                instructions[i] -= 1
            else:
                instructions[i] += 1    
        else:
            instructions[i] += 1
        i += offset
    return steps

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(5 == result)

def part1():
    result = solve(data())
    print('PART 1:', result)
    assert(381680 == result)

def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    assert(10 == result)

def part2():
    result = solve(data(), part2=True)
    print('PART 2:', result)
    assert(29717847 == result)


if __name__ == "__main__":
    test_example()
    part1()
    test_example2()
    part2()
