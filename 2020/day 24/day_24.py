"""
Advent of Code 2020 - Day 24
Pieter Kitslaar
"""

import re
from pathlib import Path

"""
Grid is defined by 3 coordinates (r,g,b) see: hex_coordinates.gif 
(taken from https://stackoverflow.com/q/2459402)

This means each tile has a neighbors at the following offsets
"""
OFFSET = {
        #  r   g   b
    'e': ( 1, -1,  0),
   'se': ( 1,  0, -1),
   'sw': ( 0,  1, -1),
    'w': (-1,  1,  0),
   'nw': (-1,  0,  1),
   'ne': ( 0, -1,  1)
}


STEP_RE = re.compile('|'.join(OFFSET.keys()))

def parse_steps(txt):
    offset = 0
    matches = []
    while m:=STEP_RE.search(txt, pos=offset):
        matches.append(m.group(0))
        offset += len(matches[-1])
    return matches

def test_step_regex():
    assert(['e', 'se', 'ne', 'e'] == parse_steps('esenee'))

example="""\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

WHITE, BLACK = range(2)

def flip_tiles(txt):
    grid = {(0,0,0): WHITE}
    for line in txt.splitlines():
        pos = [0,0,0]
        for direction in parse_steps(line):
            step = OFFSET[direction]
            pos = tuple([p+o for p,o in zip(pos, step)])
        current_tile = grid.get(pos, WHITE)
        grid[pos] = WHITE if current_tile == BLACK else BLACK
    return grid

def num_black_tiles(grid):
    return sum(1 for c in grid.values() if c == BLACK)

def test_example():
    grid = flip_tiles(example)
    num_black = num_black_tiles(grid)
    assert(10 == num_black)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def num_black_tiles(grid):
    return sum(1 for c in grid.values() if c == BLACK)

def test_puzzle():
    grid = flip_tiles(get_input())     
    num_black = num_black_tiles(grid)
    print('Part 1:', num_black)

def extended_grid_positions(grid):
    positions = set()
    for pos in grid:
        positions.add(pos)
        for step in OFFSET.values():
            neighbor_pos = tuple([p+s for p,s in zip(pos,step)])
            positions.add(neighbor_pos)
    return positions

def flip_day(grid):
    new_grid = {}
    for pos in extended_grid_positions(grid):
        color = grid.get(pos, WHITE)

        neighbors = {}
        for step in OFFSET.values():
            neighbor_pos = tuple([p+s for p,s in zip(pos,step)])
            try:
                neighbors[neighbor_pos] = grid[neighbor_pos]
            except:
                pass
        num_black = num_black_tiles(neighbors)
        new_color = color
        if color == BLACK and (num_black == 0 or num_black > 2):
            new_color = WHITE
        elif color == WHITE and (num_black == 2):
            new_color = BLACK

        if new_color == BLACK:
            new_grid[pos] = new_color
    return new_grid

def flip_n_days(grid, n):
    for _ in range(n):
        grid = flip_day(grid)
    return grid

def test_example_part2():
    grid = flip_tiles(example)
    for day, expected_black in enumerate([15, 12, 25, 14]):
        grid = flip_day(grid)
        num_black = num_black_tiles(grid)
        #print('Day', day+1, ':', num_black)
        assert(expected_black == num_black)
    
    grid = flip_tiles(example)
    grid = flip_n_days(grid,100)
    num_black = num_black_tiles(grid)
    assert(2208 == num_black)


def test_puzzle2():
    grid = flip_tiles(get_input())
    grid = flip_n_days(grid, 100)
    num_black = num_black_tiles(grid)
    print('Part 2:', num_black)


if __name__ == "__main__":
    test_step_regex()
    test_example()
    test_puzzle()
    test_example_part2()
    test_puzzle2()