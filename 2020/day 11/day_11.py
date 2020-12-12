"""
Advent of Code 2020 - Day 11
Pieter Kitslaar
"""

from pathlib import Path
from collections import Counter
from itertools import chain

example="""\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

NEIGHBORS = {
    #        x   y
    'N':   ( 0, -1),
    'NE':  ( 1, -1),
    'E':   ( 1,  0),
    'SE':  ( 1,  1),
    'S':   ( 0,  1),
    'SW':  (-1,  1),
    'W':   (-1,  0),
    'NW':  (-1, -1)
}

def parse(txt):
    return [list(line) for line in txt.splitlines()]

def get_neighbors(data, x, y):
    w, h = len(data[0]), len(data)
    neighbors = []
    for x_offset, y_offset in NEIGHBORS.values():
        X = x+x_offset
        Y = y+y_offset
        if 0 <= Y <h and 0<=X<w:
            neighbors.append(data[Y][X])
    return neighbors

def next_generation(data):
    w, h = len(data[0]), len(data)
    new_map = [row[:] for row in data]
    for y in range(h):
        for x in range(w):
            value = data[y][x]
            if value == '.':
                pass
            else:
                neighbors = Counter(get_neighbors(data, x, y))
                if value == 'L' and neighbors['#'] == 0:
                    value = '#'
                elif value == '#' and neighbors['#'] >= 4:
                    value = 'L'
            new_map[y][x] = value
    return new_map

def print_map(data):
    for row in data:
        print("".join(row))       

def interate_until_stable(data, rule=next_generation):
    prev_map = None
    current_map = data
    num_iterations = 0
    while prev_map != current_map:
        next_map = rule(current_map)  
        prev_map = current_map
        current_map = next_map
        num_iterations += 1
    return num_iterations, current_map   


def test_example():
    data = parse(example)
    num_iterations, stable_map = interate_until_stable(data)
    total_counts = Counter(chain(*stable_map))
    assert(total_counts['#'] == 37)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    data = parse(get_input())
    num_iterations, stable_map = interate_until_stable(data)
    total_counts = Counter(chain(*stable_map))
    answer = total_counts['#']
    print('Part 1:', answer)
    assert(2316 == answer)

def first_neighbors(data, x, y):
    w, h = len(data[0]), len(data)
    first_visible_neighbors = []
    for x_offset, y_offset in NEIGHBORS.values():
        step = 1
        while True:
            X=x+step*x_offset
            Y=y+step*y_offset
            step+=1
            if 0<=Y<h and 0<=X<w:
                if data[Y][X] != '.':
                    first_visible_neighbors.append(data[Y][X])
                    break
            else:
                break
    return first_visible_neighbors

def next_generation_part2(data):
    w, h = len(data[0]), len(data)
    new_map = [row[:] for row in data]
    for y in range(h):
        for x in range(w):
            value = data[y][x]
            if value == '.':
                pass
            else:
                neighbors = Counter(first_neighbors(data, x, y))
                if value == 'L' and neighbors['#'] == 0:
                    value = '#'
                elif value == '#' and neighbors['#'] >= 5:
                    value = 'L'
            new_map[y][x] = value
    return new_map

def test_example_part2():
    data = parse(example)
    num_iterations, stable_map = interate_until_stable(data, next_generation_part2)
    total_counts = Counter(chain(*stable_map))
    assert(26 == total_counts['#'])

def test_part2():
    data = parse(get_input())
    num_iterations, stable_map = interate_until_stable(data, next_generation_part2)
    total_counts = Counter(chain(*stable_map))
    answer = total_counts['#']
    print('Part 2:', answer)
    assert(2128 == answer)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example_part2()
    test_part2()
