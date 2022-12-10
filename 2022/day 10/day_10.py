"""
Advent of Code 2022 - Day 10
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

import math

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()


def run_cpu(d):
    regX = 1
    cycle = 1
    for line in d.strip().splitlines():
        if line == 'noop':
            yield cycle, regX
            cycle += 1

        elif line.startswith('addx'):
            add_value = int(line.split()[-1])
            for i in range(2):
                yield cycle, regX
                cycle += 1
            regX += add_value
    yield cycle, regX
            #yield cycle, regX

def solve(d):
    signal_strength = 0
    for cycle, regX in run_cpu(d):
        if (cycle - 20) % 40 == 0:
            this_strength = cycle*regX
            signal_strength += this_strength
    return signal_strength

EXAMPLE_SMALL = """\
noop
addx 3
addx -5"""

def test_example_small():
    solve(EXAMPLE_SMALL)

def test_example():
    result = solve(data('example.txt'))
    assert(13140 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(14040 == result)

def solve2(d):
    crt = [['.']*40 for _ in range(6)]
    for cycle, regX in run_cpu(d):
        y_pos = (cycle-1) // 40
        x_pos = (cycle-1) % 40
        if abs(x_pos - regX) < 2:
            crt[y_pos][x_pos] = '#'
    for row in crt:
        print(''.join(row))

def test_example2():
    solve2(data('example.txt'))

def test_part2():
    solve2(data())

if __name__ == "__main__":
    test_example_small()
    test_example()
    test_part1()
    test_example2()
    print()
    test_part2()
