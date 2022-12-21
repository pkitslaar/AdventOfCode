"""
Advent of Code 2022 - Day 20
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read().strip()

EXAMPLE_DATA="""\
1
2
-3
3
-2
0
4"""

from collections import deque

def solve(d, n_mixes=1, multiplier = 1):
    raw_numbers = [(i,j*multiplier) for i,j in enumerate(map(int, d.splitlines()))]
    
    numbers = deque(raw_numbers)
    N = len(numbers)       
    for _ in range(n_mixes):
        for i in range(N):
            # rotate until we find the number we need to move
            while numbers[0][0] != i:
                numbers.rotate(-1)
            j,v_orig = numbers[0]
            if v_orig == 0:
                continue
            # remove the number
            numbers.popleft()  

            # compute the number of rotations
            # we use N-1 since we removed the current number from the list              
            v = v_orig % (N-1)                
            numbers.rotate(-v)            
            
            # add the number back in the list
            numbers.appendleft((i,v_orig))        

    # get zero at the front
    while numbers[0][1] != 0:
        numbers.rotate(-1)

    unmixed = [t[1] for t in numbers]
    
    total = 0
    for i in (1000,2000,3000):
        i_mod = i % N
        total += unmixed[i_mod]
    return total

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(3 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(result == 3700)

def solve2(d):
    return solve(d, n_mixes=10, multiplier=811589153)

def test_example2():
    result = solve2(EXAMPLE_DATA)
    assert(result == 1623178306)

def test_part2():
    result = solve2(data())
    print('PART 2:', result)
    assert(result == 10626948369382)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()