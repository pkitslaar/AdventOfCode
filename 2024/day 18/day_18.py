"""
Advent of Code 2024 - Day 18
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

def parse(data, WH, N):
    grid = {}
    for i, line in enumerate(data.strip().splitlines()):
        if N > -1 and i >= N:
            break
        x,y = map(int, line.split(','))
        assert 0 <= x < WH
        assert 0 <= y < WH
        grid[(x,y)] = '#'
    if N > -1:
        assert len(grid) == N  
    return grid

from heapq import heappop, heappush
from collections import namedtuple

State = namedtuple("State", "cost steps pos prev")

def solve(data, WH, N, part2=False):
    
    start = (0,0)
    end = (WH-1, WH-1)
    grid = parse(data, WH, N)

    def dist_end(pos):
        return (pos[0]-end[0])**2 + (pos[1]-end[1])**2

    queue = [State(dist_end(start), 0, start, None)]
    visited = {}    
    while queue:
        #print(len(queue))
        current = heappop(queue)
        if not current.pos in visited:
            visited[current.pos] = current
        else:
            if visited[current.pos].steps <= current.steps:
                continue
            visited[current.pos] = current

        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            new_pos = (current.pos[0]+dx, current.pos[1]+dy)
            if 0 <= new_pos[0] < WH and 0 <= new_pos[1] < WH:
                if grid.get(new_pos,'.') != '#' and (new_pos not in visited or visited[new_pos].steps > current.steps+1):
                    heappush(queue, State(dist_end(new_pos), current.steps+1, new_pos, current))

    result = visited[end].steps if end in visited else -1
    return result


def test_example():
    result = solve(EXAMPLE_DATA, WH=7, N=12)
    print(f"example: {result}")
    assert result == 22


def test_part1():
    result = solve(data(), WH=71, N=1024)
    print("Part 1:", result)
    assert result == 288

def solve2(data, WH):
    grid = parse(data, WH, N=-1)
    num_bytes = len(grid)

    # find the first byte that is not reachable
    # using binary search    
    lo, hi = 0, num_bytes
    while lo < hi:
        mid = (lo + hi) // 2        
        if solve(data, WH, mid) > -1:
            lo = mid + 1
        else:
            hi = mid
    
    return data.strip().splitlines()[lo-1]
    

def test_example2():
    result = solve2(EXAMPLE_DATA, WH=7)
    print(f"example 2: {result}")
    assert result == "6,1"


def test_part2():
    result = solve2(data(), WH=71)
    print("Part 2:", result)
    assert result == "52,5"


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()