"""
Advent of Code 2021 - Day 25
Pieter Kitslaar
"""

from pathlib import Path

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def parse(txt):
    grid = {}
    for y, line in enumerate(txt.splitlines()):
        for x, v in enumerate(line):
            if v != '.':
                grid[(y,x)] = v
    return {p:v for p,v in sorted(grid.items())}, y+1, x+1

def plot(grid,H,W):
    for y in range(H):
        for x in range(W):
            print(grid.get((y,x),'.'),end="")
        print()

def step(grid, H, W):
    new_grid = {}
    for C in ('>','v'):
        direction = {'>': (0,1), 'v':(1,0)}[C]
        for p,c in grid.items():
            if c == C:
                new_p = (p[0]+direction[0])%(H),(p[1]+direction[1])%(W)
                if grid.get(new_p,'.') == '.':
                    new_grid[new_p] = c
                    new_grid[p]='.'
                else:
                    new_grid[p]=c
            elif C=='>':
                new_grid[p]=c
        grid = new_grid.copy()
    return {p:v for p,v in sorted(new_grid.items()) if v!='.'}

example_simple="""\
...>...
.......
......>
v.....>
......>
.......
..vvv.."""

example_simple_1="""\
..vv>..
.......
>......
v.....>
>......
.......
....v.."""

example_simple_2="""\
....v>.
..vv...
.>.....
......>
v>.....
.......
......."""

example_simple_3="""\
......>
..v.v..
..>v...
>......
..>....
v......
......."""

example_simple_4="""\
>......
..v....
..>.v..
.>.v...
...>...
.......
v......"""


def test_example_simple():
    g,H,W = parse(example_simple)
    # step 1
    g1 = step(g,H,W)
    g1_expected, *_ = parse(example_simple_1)
    assert g1 == g1_expected

     # step 2
    g2 = step(g1,H,W)
    g2_expected, *_ = parse(example_simple_2)
    assert g2 == g2_expected

    # step 3
    g3 = step(g2,H,W)
    g3_expected, *_ = parse(example_simple_3)
    assert g3 == g3_expected

    # step 4
    g4 = step(g3,H,W)
    g4_expected, *_ = parse(example_simple_4)
    assert g4 == g4_expected

example ="""\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""

example_1 = """\
....>.>v.>
v.v>.>v.v.
>v>>..>v..
>>v>v>.>.v
.>v.v...v.
v>>.>vvv..
..v...>>..
vv...>>vv.
>.v.v..v.v"""

def solve1(txt):
    g,H,W = parse(txt)
    steps = 0
    while True:
        g_new = step(g,H,W)
        steps += 1
        if g_new == g:
            break
        g = g_new
    return steps

def test_example():
    #result = solve1(example)
    g, H, W = parse(example)
    g1 = step(g,H,W)
    #plot(g1,H,W)
    g1_expected, *_ = parse(example_1)
    assert g1 == g1_expected

    result = solve1(example)
    assert 58 == result

def test_part1():
    result = solve1(get_input())
    print('Part 1', result)

if __name__ == "__main__":
    test_example_simple()
    test_example()
    test_part1()
