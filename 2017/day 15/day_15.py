"""
Advent of Code 2017 - Day 15
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

FACTOR_A = 16807
FACTOR_B = 48271
DIVISOR = 2147483647
N = 40_000_000
N2 = 5_000_000

def gen(prev_v, factor):
    """    
    """
    while True: 
        next_v = (prev_v*factor) % DIVISOR
        yield next_v
        prev_v = next_v

EXAMPLE="""\
--Gen. A--  --Gen. B--
   1092455   430625591
1181022009  1233683848
 245556042  1431495498
1744312007   137874439
1352636452   285222916"""
import itertools

def test_gen():
    a = [v for v in itertools.islice(gen(65, FACTOR_A),5)]
    b = [v for v in itertools.islice(gen(8921, FACTOR_B),5)]    
    lines = list(EXAMPLE.strip().splitlines())
    for va, vb, line in zip(a, b, lines[1:]):
        assert(va == int(line.strip().split()[0].strip()))
        assert(vb == int(line.strip().split()[1].strip()))


def solve(genA, genB,n=N):
    """
    pA*fA^(i) % d
    """
    matches = 0
    for va, vb in itertools.islice(zip(genA, genB),n):
        if va % 65536 == vb % 65536:
            matches += 1
    return matches

def test_example():
    result = solve(gen(65,FACTOR_A), gen(8921,FACTOR_B))
    assert(588 == result)

def parse(d):
    values = []
    for line in d.splitlines():
        values.append(int(line.split()[-1]))
    return values

def test_part1():
    pA, pB = parse(data())
    result = solve(gen(pA, FACTOR_A), gen(pB, FACTOR_B))
    print('PART 1:', result)
    assert(609 == result)

def gen2(prev_v, factor, multiple_check):
    """    
    """
    while True: 
        next_v = (prev_v*factor) % DIVISOR
        if next_v % multiple_check == 0:
            yield next_v
        prev_v = next_v

def test_part2():
    pA, pB = parse(data())
    result = solve(gen2(pA, FACTOR_A, 4), gen2(pB, FACTOR_B, 8), N2)
    print('PART 2:', result)
    assert(253 == result)

if __name__ == "__main__":
    test_gen()
    test_example()
    test_part1()
    test_part2()