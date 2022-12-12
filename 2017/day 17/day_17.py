"""
Advent of Code 2017 - Day 17
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

from collections import deque
def spinlock(step_size, N=2017, do_print=False):
    buffer = deque()
    for i in range(N+1):
        n_rotations = step_size % len(buffer) if buffer else step_size
        buffer.rotate(-n_rotations-1)
        buffer.appendleft(i)
    return buffer[1]        
    
def spinlock_zeros(step_size, N=2017):
    current_pos = 0
    zero_value = 0
    for i in range(1,N+1):
        current_pos = (current_pos + step_size) % (i)
        if current_pos == 0:
            zero_value = i
        current_pos += 1
    return zero_value

def test_example():
    result = spinlock(3, 2017, do_print=False)
    assert(638 == result)

def test_part1():
    result = spinlock(371, 2017, do_print=False)
    print('PART 1:', result)
    assert(1311 == result)

def test_part2():
    result = spinlock_zeros(371, 50000000)
    print('PART 2:', result)
    assert(39170601 == result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_part2()
