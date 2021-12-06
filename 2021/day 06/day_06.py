"""
Advent of Code 2021 - Day 06
Pieter Kitslaar
"""

from pathlib import Path
from functools import lru_cache

"""
  
  t                   1                   2
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8
            x0+1       x0+1+(1*7)     x0+1+(2*7)   x0+1+(3*7) 
            |             |             |             |
            v             v             v             v
x 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4
            8 7 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5
                          8 7 6 5 4 3 2 1 0 6 5 4 3 2 1 0 6 5
                                        8 7 6 5 4 3 2 1 0 6 5
                                                      8 7 6 5
"""

def add_times(x0, t0, T): 
    """Return the times when new fish are added
    x0 is the days left to new fish at t0
    T is the number of days to look ahead
    """
    return [t0+x0+1+(i*7) for i in range(1+((T-1-t0)-x0)//7)]

# we use the lru_cache since we are calling this method very often
# add most values can be cached
@lru_cache
def evolve_fast(x0, t0, T):
    new_times = add_times(x0, t0, T)
    num_added = 0
    for t in new_times:
        # new fish start with value 8 at time t
        num_added += 1+evolve_fast(8, t, T)
    return num_added

def multi_resolve(numbers, T):
    result = 0
    for n in numbers:
        added = 1+evolve_fast(n, 0, T)
        result += added
    return result

def test_evolve_fast():
    d = [3,4,3,1,2]
    assert  5 == multi_resolve(d,0)
    assert  5 == multi_resolve(d,1)
    assert  6 == multi_resolve(d,2)
    assert  7 == multi_resolve(d,3)
    assert  9 == multi_resolve(d,4)
    assert 10 == multi_resolve(d,5)
    assert 10 == multi_resolve(d,6)
    assert 10 == multi_resolve(d,7)
    assert 10 == multi_resolve(d,8)
    assert 11 == multi_resolve(d,9)
    assert 12 == multi_resolve(d,10)
    assert 26 == multi_resolve(d,18)



def test_example():
    assert 5934 == multi_resolve([3,4,3,1,2], 80)

def get_input():
    input_numbers = []
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    initial = list(map(int, get_input().strip().split(',')))
    result = multi_resolve(initial, 80)
    print('Part 1:', result)
    assert 394994 == result

def test_example2():
    assert 26984457539 == multi_resolve([3,4,3,1,2], 256)

def test_part2():
    initial = list(map(int, get_input().strip().split(',')))
    result = multi_resolve(initial, 256)
    print('Part 2:', result)
    assert 1765974267455 == result

if __name__ == "__main__":
    test_evolve_fast()
    test_example()
    test_part1()
    test_example2()
    test_part2()