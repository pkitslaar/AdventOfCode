"""
Advent of Code 2022 - Day 04
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

EXAMPLE_DATA="""\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

def is_inside(A,b):
    # Check if coord b is inside range A
    #
    #           11111111112222
    #  01345678901234567890123
    #        A[0]-----------A[1]
    #  b<--->                       abs(b-A[0])     =    7
    #   <------------------>      + abs(b-A[1])     = + 22
    #        <------------->      - abs(A[1]-A[0])  = - 15
    #                                               -------
    #                                                   14
    #           11111111112222
    #  01345678901234567890123
    #        A[0]-----------A[1]
    #         <----->b              abs(b-A[0])     =    8
    #                 <----->     + abs(b-A[1])     = +  7
    #         <------------->     - abs(A[1]-A[0])  = - 15
    #                                               -------
    #                                                    0
    d = abs(b-A[0])+abs(b-A[1]) - abs(A[1]-A[0])
    return d == 0

def fully_contained(A,B):
    # check if range B is fully contained in A
    return is_inside(A,B[0]) and is_inside(A,B[1])

def full_overlap(A, B):
    # check if range A and B fully overlap
    # so either A contains B or B contains A
    return fully_contained(A,B) or fully_contained(B,A)
    
def test_fully_contains():
    assert(False == fully_contained((0,3),(5,9)))
    assert(True == fully_contained((0,10),(2,9)))
    assert(False == fully_contained((2,9),(0,10)))
    assert(True == fully_contained((0,10),(9,10)))
    assert(True == fully_contained((0,10),(10,10)))
    assert(False == fully_contained((0,10),(10,11)))

def solve(d, overlap_func=full_overlap):
    num_overlap = 0
    for line in d.strip().splitlines():
        AB = line.split(',')
        A = tuple(map(int,AB[0].split('-')))
        B = tuple(map(int,AB[1].split('-')))
        if overlap_func(A,B):
            num_overlap += 1
    return num_overlap

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(2 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(542 == result)


def fully_contained(A,B):
    # check if range B is fully contained in A
    return is_inside(A,B[0]) and is_inside(A,B[1])

def any_overlap(A, B):
    # check if there is any overlap between A and B
    return is_inside(A,B[0]) or is_inside(A,B[1]) or is_inside(B,A[0]) and is_inside(B,A[1])

def test_example2():
    result = solve(EXAMPLE_DATA, any_overlap)
    assert(4 == result)

def test_part2():
    result = solve(data(), any_overlap)
    print('PART 2:', result)

if __name__ == "__main__":
    test_fully_contains()
    test_example()
    test_part1()
    test_example2()
    test_part2()