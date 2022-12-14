"""
Advent of Code 2017 - Day 19
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

EXAMPLE_DATA = """\
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ """

def add(a,b):
    return (a[0]+b[0], a[1]+b[1])

def valid_new_dir(prev_dir, new_dir):
    if prev_dir[0] == 0:
        return prev_dir[1] != -new_dir[1]
    elif prev_dir[1] == 0:
        return prev_dir[0] != -prev_dir[0]
    else:
        raise ValueError(f"invalid dir {prev_dir}")

def valid_new_dirs(prev_dir):
    valid = [prev_dir]
    if prev_dir[0] == 0:
        valid.extend([(1,0),(-1,0)])
    elif prev_dir[1]==0:
        valid.extend([(0,1),(0,-1)])
    else:
        raise ValueError(f"invalid dir {prev_dir}")
    return valid



from collections import deque

def solve(d, draw=False):
    grid = {}
    START_POINT = None
    for y, r in enumerate(d.splitlines()):
        for x,c in enumerate(r):
            if c!=' ':
                if c=='|' and not START_POINT:
                    START_POINT=(y,x)
                grid[(y,x)]=c
    
    
 

    path = [START_POINT]
    prev_dir = (1,0)
    DIRS = [(1,0),(0,1),(-1,0),(0,-1)]
    found_end = False
    if draw:
        import turtle
        turtle.up()
        turtle.goto(path[0][1], -path[0][0])
        turtle.down()
    while not found_end:
        # try direction starting at prev_dir
        possible_new_pos = []
        for di, D in enumerate(valid_new_dirs(prev_dir)):
            if valid_new_dir(prev_dir, D):
                next_pos = add(path[-1], D)
                if next_pos in grid:
                    possible_new_pos.append((next_pos in path, di, next_pos, D))
        possible_new_pos.sort()
        if not possible_new_pos:
            found_end = True
        else:
            path.append(possible_new_pos[0][2])
            if draw:
                turtle.goto(path[-1][1], -path[-1][0])
            prev_dir = possible_new_pos[0][3]
    
            
    return ''.join([grid[p] for p in path if grid[p].isalpha()]), len(path)

def test_example():
    result, num_steps = solve(EXAMPLE_DATA)
    assert('ABCDEF' == result)
    assert(38 == num_steps)

def test_solution():
    result, num_steps = solve(data(), draw=False)
    print('PART 1:', result)
    assert('GSXDIPWTU' == result)
    print('PART 2:', num_steps)
    assert(16100 == num_steps)

if __name__ == "__main__":
    test_example()
    test_solution()