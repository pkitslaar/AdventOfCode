"""
Advent of Code 2022 - Day 09
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

import math

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

EXAMPLE_DATA="""\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

# coords Y,X
DIRECTIONS = {'R': (0,1), 'L': (0,-1), 'U':(1,0), 'D':(-1,0)}

def solve(d, n_knots=1):
    H = [0, 0]
    KNOTS = [[0, 0] for _ in range(n_knots)]
    head_visited = set([tuple(H)])
    tail_visited = set([tuple(KNOTS[-1])])
    for line in d.strip().splitlines():
        direction, num_steps_str = line.split()
        num_steps = int(num_steps_str)
        for _ in range(num_steps):
            step_dir = DIRECTIONS[direction] 
            H[0] += step_dir[0]
            H[1] += step_dir[1]
            head_visited.add(tuple(H))

            prev_knot = H
            for knot in KNOTS:
                if distance := math.sqrt((prev_knot[0]-knot[0])**2+(prev_knot[1]-knot[1])**2) >= 2:
                    # more than 1 steps away
                    Y_diff = prev_knot[0]-knot[0]
                    X_diff = prev_knot[1]-knot[1]
                    if abs(X_diff) == 0:
                        knot[0] += 1 if Y_diff > 0 else -1
                    elif abs(Y_diff) == 0:
                        knot[1] += 1 if X_diff > 0 else -1
                    else:
                        knot[0] += 1 if Y_diff > 0 else -1
                        knot[1] += 1 if X_diff > 0 else -1
                prev_knot = knot
            tail_visited.add(tuple(KNOTS[-1]))
    return len(tail_visited)

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(13 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(6266 == result)

def test_example2():
    result = solve(EXAMPLE_DATA, n_knots=9)
    assert(1 == result)

def test_part2():
    result = solve(data(),n_knots=9)
    print('PART 2:', result)
    assert(2369 == result)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()



