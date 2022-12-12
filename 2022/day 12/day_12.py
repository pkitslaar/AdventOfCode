"""
Advent of Code 2022 - Day 12
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

import math

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

EXAMPLE_DATA="""\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""   

def parse(d):
    grid = []
    S = None
    S_ord = ord('S')
    E = None
    E_ord = ord('E')
    for row_i, line in enumerate(d.strip().splitlines()):
        row = [ord(c) for c in line]
        if not S and S_ord in row:
            S = (row_i, row.index(S_ord))
        if not E and E_ord in row:
            E = (row_i, row.index(E_ord))
        grid.append(row)
    grid[S[0]][S[1]] = ord('a')
    grid[E[0]][E[1]] = ord('z')
    return grid, S, E

import heapq

def solve(d, part2=False):
    grid, S, E = parse(d)
    H = len(grid)
    W = len(grid[0])
    arrival_times = [[-1]*W for _ in range(H)]

    # PART 1 starts from S
    # PART 2 starts from E
    to_visit = [(0,S)] if not part2 else [(0,E)]
    visited = set()
    while to_visit:
        current = heapq.heappop(to_visit)
        c_time, c_pos = current
        c_height = grid[c_pos[0]][c_pos[1]]
        if not c_pos in visited:
            visited.add(c_pos)
            arrival_times[c_pos[0]][c_pos[1]] = c_time
            if not part2:
                # In PART 1 we stop when reaching E
                # PART 2 we keep on going until all positions that can
                # be reached have been visited.
                if c_pos == E:
                    print(f'Found E in {c_time} steps')
                    return c_time
            for N in [(1,0),(-1,0),(0,1),(0,-1)]:
                n_pos = (c_pos[0]+N[0], c_pos[1]+N[1])
                if not n_pos in visited:
                    if ((n_pos[0] >= 0) and (n_pos[0] < H) and 
                        (n_pos[1]>=0) and (n_pos[1]<W)):
                        n_height = grid[n_pos[0]][n_pos[1]]
                        n_time = arrival_times[n_pos[0]][n_pos[1]]
                        if not part2:
                            # maximum one step up
                            if n_height - c_height <= 1:
                                heapq.heappush(to_visit, (c_time+1, n_pos))
                        else:
                            # maximum one step down
                            if c_height - n_height <= 1:
                                heapq.heappush(to_visit, (c_time+1, n_pos))
    # PART 2
    # Find 'a' positions in the grid that were visited (e.g. arrival_time > -1)
    # and find the one reached in the fewest number of steps
    assert(part2)
    a_steps = []
    for row_i, row in enumerate(grid):
        for col_i, c in enumerate(row):
            if c == ord('a'):
                a_steps.append(arrival_times[row_i][col_i])
    return min(s for s in a_steps if s>-1)



def test_example():
    result = solve(EXAMPLE_DATA)
    assert(31 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(440 == result)

def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    assert(29 == result)

def test_part2():
    result = solve(data(), part2=True)
    print('PART 2:', result)
    assert(439 == result)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()



    
