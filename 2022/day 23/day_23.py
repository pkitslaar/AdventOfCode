"""
Advent of Code 2022 - Day 23
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

EXAMPLE_SMALL="""\
.....
..##.
..#..
.....
..##.
....."""

EXAMPLE_DATA="""\
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#.."""

DIRECTIONS = {
    'NW': (-1, -1),
    'N':  ( 0, -1),
    'NE': ( 1, -1),
    'E':  ( 1,  0),
    'SE': ( 1,  1),
    'S':  ( 0,  1),
    'SW': (-1,  1),
    'W':  (-1,  0),
}

def print_grove(grove):
    X = [p[0] for p in grove]
    Y = [p[1] for p in grove]
    for y in range(min(Y), max(Y)+1):
        for x in range(min(X), max(X)+1):
            print(grove.get((x,y),'.'), end='')
        print()
    print()

def empty_spaces(grove):
    X = [p[0] for p in grove]
    Y = [p[1] for p in grove]
    num_empty = 0
    for y in range(min(Y), max(Y)+1):
        for x in range(min(X), max(X)+1):
            if grove.get((x,y)) is None:
                num_empty+=1
    return num_empty

def solve(d, N_round=None):
    grove = {}
    for y,l in enumerate(d.splitlines()):
        for x, v in enumerate(l):
            if v == '#':
                grove[(x,y)]='#'

    MOVE_DIRS = [
        (('N', 'NE', 'NW'),'N'),
        (('S', 'SE', 'SW'),'S'),
        (('W', 'NW', 'SW'),'W'),
        (('E', 'NE', 'SE'),'E')
    ]

    needs_move= True
    round = 0
    while needs_move:
        needs_move = False

        if round == N_round:
            return empty_spaces(grove)

        # First half
        proposed_to_move = {}
        for elf in grove:
            neighborhs = {D_NAME for D_NAME, D in DIRECTIONS.items() if grove.get((elf[0]+D[0], elf[1]+D[1]))}
            if len(neighborhs):
                needs_move = True
                for check_dirs, propose_step in MOVE_DIRS:
                    if all(cd not in neighborhs for cd in check_dirs):
                        # all of the directions are empty
                        propose_dir = DIRECTIONS[propose_step]
                        p_position = (elf[0]+propose_dir[0], elf[1]+propose_dir[1])
                        proposed_to_move.setdefault(p_position,[]).append(elf)
                        break
        
        # send half
        # Check if any position was proposed by a single elf
        for propesed_pos, elfs in proposed_to_move.items():
            if len(elfs) == 1:
                elf = elfs[0]
                del grove[elf]
                grove[propesed_pos]='#'
        
        #print_grove(grove)

        # rotate the MOVE_DIRS for the next round
        MOVE_DIRS.append(MOVE_DIRS.pop(0))

        round += 1
    
    #print_grove(grove)
    return round
    

def test_small():
    solve(EXAMPLE_SMALL)

def test_example():
    result = solve(EXAMPLE_DATA, N_round=10)
    assert(110 == result)

def test_part1():
    result = solve(data(), N_round=10)
    print('PART 1:', result)
    assert(4075 == result)

def test_example2():
    result = solve(EXAMPLE_DATA)
    assert(20 == result)

def test_part2():
    result = solve(data())
    print('PART 2:', result)
    assert(950 == result)


if __name__ == "__main__":
    test_small()
    test_example()
    test_part1()
    test_example2()
    test_part2()