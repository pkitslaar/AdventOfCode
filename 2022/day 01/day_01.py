"""
Advent of Code 2022 - Day 01
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

EXAMPLE_DATA = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

from collections import Counter

def parse(d):
    numbers = Counter()
    elf = 1
    for line in d.splitlines():
        if not line:
            elf += 1
        else:
            numbers.update({elf: int(line)})
    return numbers

def solve(d,n=1):
    counts = parse(d)
    return sum(t[1] for t in counts.most_common(n))

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(24000 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(71502 == result)

def test_example2():
    result = solve(EXAMPLE_DATA, 3)
    assert(45000 == result)

def test_part2():
    result = solve(data(), 3)
    print('PART 2:', result)
    assert(208191 == result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()