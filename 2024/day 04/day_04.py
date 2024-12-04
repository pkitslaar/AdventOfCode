"""
Advent of Code 2024 - Day 04
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

# to test the individual functions
TEST_DATA = """\
012
345
678
"""

def horizontal(data, reverse=False):
    for line in data.splitlines():
        yield line if not reverse else line[::-1]

def test_horizontal():
    t = [*horizontal(TEST_DATA)]
    assert t == ['012', '345', '678']
    t = [*horizontal(TEST_DATA, reverse=True)]
    assert t == ['210', '543', '876']

def vertical(data, reverse=False):
    lines = data.splitlines()
    if reverse:
        lines = lines[::-1]
    numX = len(lines[0])
    for i in range(numX):
        yield "".join(line[i] for line in lines)

def test_vertical():
    t = [*vertical(TEST_DATA)]
    assert t == ['036', '147', '258']
    t = [*vertical(TEST_DATA, reverse=True)]
    assert t == ['630', '741', '852']
        
def diagonal(data, reverseY=False, reverseX=False):
    """
      x  012345
    y
    0    012345   
    1    123456   
    2    234567   
    3    345678   
    4    456789   
    5    56789A   

    line: (x,y)
    
    0: (0,0)
    1: (1,0) (0,1)
    2: (2,0) (1,1) (0,2)
    3: (3,0) (2,1) (1,2) (0,3)
    4: (4,0) (3,1) (2,2) (1,3) (0,4)
    5: (5,0) (4,1) (3,2) (2,3) (1,4) (0,5)
    6: (5,1) (4,2) (3,3) (2,4) (1,5)
    7: (5,2) (4,3) (3,4) (2,5)
    8: (5,3) (4,4) (3,5)
    9: (5,4) (4,5)
    A: (5,5)           
    """

    lines = data.splitlines()
    if reverseY:
        lines = [line[::-1] for line in lines]
    numX = len(lines[0])
    numY = len(lines)
    assert numX == numY
    for line_index in range(numX+numY):
        diagonal = []
        # x decreases, y increases
        for x,y in zip(range(line_index,-1,-1), range(line_index+1)):
            if x < numX and y < numY:
                diagonal.append(lines[y][x])
        if diagonal:
            yield "".join(diagonal) if not reverseX else "".join(diagonal[::-1])

def test_diagonal():
    """
    012
    345
    678
    """
    t = [*diagonal(TEST_DATA)]
    assert t == ['0', '13', '246', '57', '8']
    t = [*diagonal(TEST_DATA, reverseX=True)]
    assert t == ['0', '31', '642', '75', '8']
    t = [*diagonal(TEST_DATA, reverseY=True)]
    assert t == ['2', '15', '048', '37', '6']
    t = [*diagonal(TEST_DATA, reverseY=True, reverseX=True)]
    assert t == ['2', '51', '840', '73', '6']

def yield_all(data):
    yield from horizontal(data)
    yield from horizontal(data, reverse=True)
    yield from vertical(data)
    yield from vertical(data, reverse=True)
    yield from diagonal(data)
    yield from diagonal(data, reverseX=True)
    yield from diagonal(data, reverseY=True)
    yield from diagonal(data, reverseY=True, reverseX=True)

import re

XMAX_REGEX = re.compile(r"XMAS")

def solve(data):
    result = 0
    for line in yield_all(data):
        result += sum(1 for _ in XMAX_REGEX.finditer(line))
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 18


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 2644

def solve2(data):
    """
    Grid based approach to find all X shapes in a 3x3 grid
    """
    lines = data.strip().splitlines()
    numX = len(lines[0])
    numY = len(lines)

    grid = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x,y)] = c

    result = 0
    for y in range(1, numY-1):
      for x in range(1, numX-1):
        # center of 3x3 grid
        # should contain 'A'
        if grid[(x,y)] != 'A':
            continue

        # Super simple check for the 4 possible X shapes in neighborhood

        # M . S
        # . A .
        # M . S
        if grid[(x-1,y-1)] == 'M' and grid[(x+1,y+1)] == 'S' and grid[(x-1,y+1)] == 'M' and grid[(x+1,y-1)] == 'S':
            result += 1
        # M . M
        # . A .
        # S . S
        if grid[(x-1,y-1)] == 'M' and grid[(x+1,y+1)] == 'S' and grid[(x-1,y+1)] == 'S' and grid[(x+1,y-1)] == 'M':
            result += 1
        # S . M
        # . A .
        # S . M
        if grid[(x-1,y-1)] == 'S' and grid[(x+1,y+1)] == 'M' and grid[(x-1,y+1)] == 'S' and grid[(x+1,y-1)] == 'M':
            result += 1
        # S . S
        # . A .
        # M . M
        if grid[(x-1,y-1)] == 'S' and grid[(x+1,y+1)] == 'M' and grid[(x-1,y+1)] == 'M' and grid[(x+1,y-1)] == 'S':
            result += 1
    
    return result

def test_example2():
    result = solve2(EXAMPLE_DATA)
    print(f"example 2: {result}")
    assert result == 9

def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result < 1959  
    assert result < 1955 # initially assumed X could also be horizontal or vertical, but it's only diagonal
    assert result == 1952


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()