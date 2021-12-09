"""
Advent of Code 2021 - Day 09
Pieter Kitslaar
"""

from pathlib import Path
import collections

example = """\
2199943210
3987894921
9856789892
8767896789
9899965678"""

def parse(txt):
    heightmap = {}
    for y, row in enumerate(txt.splitlines()):
        heightmap[y] = {}
        for x, height in enumerate(row):
            heightmap[y][x]=int(height)
    return heightmap

NEIGHBORS = [(-1,0),(0,1),(1,0),(0,-1)]

def low_points(heightmap):
    H = len(heightmap)
    W = len(heightmap[0])

    for y in range(H):
        for x in range(W):
            current = heightmap[y][x]
            adjacent = []
            for dy, dx in NEIGHBORS:
                try:
                    adjacent.append(heightmap[y+dy][x+dx])
                except KeyError:
                    pass
            if all(current < adj for adj in adjacent):
                yield current, (y, x)

def solve1(txt):
    risk = 0
    for low_p, _ in low_points(parse(txt)):
        risk += low_p + 1
    return risk

def test_example():
    result = solve1(example)
    assert 15 == result

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    result = solve1(get_input())
    print('Part1 :', result)
    assert 448 == result

def flood(heightmap, low_p):
    bassin = set()
    front = collections.deque()
    front.append(low_p)
    while front:
        current_y, current_x = front.pop()
        try:
            current_value = heightmap[current_y][current_x]
        except KeyError:
            current_value = 10 # outside map

        if current_value < 9:
            bassin.add((current_y, current_x))
            for dy, dx in NEIGHBORS:
                new_y = current_y + dy
                new_x = current_x + dx
                if (new_y, new_x) not in bassin:
                    front.append((new_y, new_x))
    return bassin

def test_flood():
    hm = parse(example)
    assert 3 == len(flood(hm, (0,1)))

def solve2(txt):
    hm = parse(txt)
    bassins = []
    for _, low_p in low_points(hm):
        bassins.append(flood(hm, low_p))
    bassins.sort(key = lambda b: len(b))
    largest = [len(b) for b in bassins[::-1]][:3]
    return largest[0]*largest[1]*largest[2]

def test_example2():
    result = solve2(example)
    assert 1134 == result

def test_part2():
    result = solve2(get_input())
    print('Part 2:', result)
    assert 1417248 == result

if __name__ == "__main__":
    test_example()
    test_part1()
    test_flood()
    test_example2()
    test_part2()