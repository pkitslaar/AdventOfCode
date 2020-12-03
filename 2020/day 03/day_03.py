"""
Advent of Code 2020 - Day 03
Pieter Kitslaar
"""

from pathlib import Path
from functools import reduce

example_map="""\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

"""
Right 1, down 1.
Right 3, down 1. (This is the slope you already checked.)
Right 5, down 1.
Right 7, down 1.
Right 1, down 2.
"""
ALL_SLOPES = [(1,1),(3,1),(5,1),(7,1),(1,2)]

def solve(input_map, step=(3,1)):
    map_grid = input_map.splitlines()
    map_height=len(map_grid)
    map_width=len(map_grid[0])
    x,y=0,0
    step_chars = []
    while y < map_height:
        step_chars.append(map_grid[y][x])
        x = (x + step[0]) % map_width
        y = y + step[1]
    num_trees = sum(1 for c in step_chars if c == '#')
    return num_trees

def test_example():
    num_trees = solve(example_map)
    print('Example Part1:', num_trees)
    assert(7 == num_trees)

    all_trees = [solve(example_map, slope) for slope in ALL_SLOPES]
    all_trees_multiplied = reduce(lambda a,b: a*b, all_trees)
    print('Example Part 2', all_trees_multiplied)
    assert(336 == all_trees_multiplied)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read().strip()

def test_part1():
    real_input = get_input()
    num_trees = solve(real_input)
    assert(262 == num_trees)
    print('Part 1:', num_trees)

    all_trees = [solve(real_input, slope) for slope in ALL_SLOPES]
    all_trees_multiplied = reduce(lambda a,b: a*b, all_trees)
    print('Part 2', all_trees_multiplied)
    assert(2698900776 == all_trees_multiplied)

if __name__ == "__main__":
    test_example()
    test_part1()
    