"""
Advent of Code 2022 - Day 21
Pieter Kitslaar
"""
from pathlib import Path
THIS_DIR = Path(__file__).parent

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

EXAMPLE_DATA="""\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

import re

def parse(d):
    jungle = {}
    next_movements = False
    movements_txt = None
    start_pos = None
    for r, l in enumerate(d.splitlines()):
        if not l:
            next_movements = True
            continue
        if next_movements:
            movements_txt = l
            break
        
        for c, v in enumerate(l):
            if v in ('.','#'):
                if not start_pos:
                    start_pos = (r+1,c+1)
                jungle[(r+1,c+1)]=v
    
    movements = []
    prev_c = None
    for m in re.findall('((\d+)|([RL]))', movements_txt):
        if m[0].isalpha():
            movements.append({'turn': m[0]})
        else:
            movements.append({'steps': int(m[0])})

    return jungle, movements, start_pos

DIRS={
    '>': (0,1),
    '<': (0,-1),
    'v': (1,0),
    '^': (-1,0)
}

TURN_TABLE={
    '>': {'R': 'v', 'L': '^'},
    '<': {'R': '^', 'L': 'v'},
    'v': {'R': '<', 'L': '>'},
    '^': {'R': '>', 'L': '<'},
}
import math
def new_pos_2D(jungle, W, H, new_pos, facing):
    D = DIRS[facing]
    new_pos = (new_pos[0]+D[0], new_pos[1]+D[1])
    while jungle.get(new_pos) is None:
        if 1 <= new_pos[0] <= H and 1<= new_pos[1] <= W:
            new_pos = (new_pos[0]+D[0], new_pos[1]+D[1])
        else:
            if new_pos[0] < 1:
                new_pos = (H,new_pos[1])
            elif new_pos[0] > H:
                new_pos = (1, new_pos[1])
            elif new_pos[1] < 1:
                new_pos = (new_pos[0], W)
            elif new_pos[1] > W:
                new_pos = (new_pos[0], 1)
            else:
                raise ValueError("invalid position")
    return new_pos, facing


def new_pos_3D(jungle, W, H, pos, facing, example=True):
    face_size = max([W//4,H//4])
    D = DIRS[facing]
    new_pos = (pos[0]+D[0], pos[1]+D[1])
    if jungle.get(new_pos):
        return new_pos, facing
    else:
        # Find FACE INDEX
        face_X = math.ceil(pos[1]/face_size)
        face_Y = math.ceil(pos[0]/face_size)
        local_X = pos[1] - (face_X-1)*face_size
        local_Y = pos[0] - (face_Y-1)*face_size
        
        if example:
            face_N = {
                                    (3,1): 1,
            (1,2): 2,   (2,2): 3,   (3,2): 4,
                                    (3,3): 5,   (4,3): 6  
            }[(face_X, face_Y)]
            """
              1  fs 2fs 3fs  4fs = W
              |  |   |   |   |
        1   -         1111
                      1111
                      1111
        fs  -         1111
              222233334444
              222233334444
              222233334444
        2fs - 222233334444
                      55556666
                      55556666
                      55556666
     H =3fs -         55556666
            """
            result = {   
                #  1 < maps to top side of 3 v
                (1, '<'): ((face_size+1, face_size + local_Y), '<'),
                #  1 > maps to right side of 6 <
                (1, '>'): ((H-local_Y,W),'<'),
                # 1 ^ maps to top side of 2 v
                (1, '^'): ((face_size+1, face_size - (local_X-1)),'v'),
                # 2 v maps to bottom side of 5 ^
                (2, 'v'): ((3*face_size - local_X, H), '^'),
                # 3 ^ maps to left side 1 >
                (3, '^'): ((local_X, 2*face_size + 1), '>'),
                # 3 v maps to left side 5 >
                (3, 'v'): ((H-local_X-1, 2*face_size + 1), '>'),
                #  4 > maps to top side of 6 v
                (4, '>'): ((2*face_size + 1, W - (local_Y-1)),'v'),
                # 5 < maps to bottom side 3 ^
                (5, '<'): ((2*face_size, 3*face_size - (local_Y-1)), '^'),
                # 5 V maps to bottom 2 ^
                (5, 'v'): ((2*face_size, face_size - (local_X-1)), '^'),
                #  6 V maps to left side of 2 >
                (6, 'v'): ((2*face_size - (local_X-1), 1),'>'),
            }[(face_N,facing)]
        else:
            face_N = {
                        (2,1): 1,   (3,1): 2,
                        (2,2): 3,   
            (1,3): 4,   (2,3): 5,   
            (1,4): 6  
            }[(face_X, face_Y)]
            """
              1  fs 2fs 3fs  4fs = W
              |  |   |   |   |
           1-     11112222
                  11112222
                  11112222
          fs-     11112222
                  3333
                  3333
                  3333
         2fs-     3333
              44445555
              44445555
              44445555
         3fs- 44445555
              6666
              6666
              6666
       H=4fs- 6666
            """
            result = {   
                #  1 < maps to left side of 4 >
                (1, '<'): ((3*face_size - (local_Y-1), 1), '>'),
                # 1 ^ maps to left side of 6 >
                (1, '^'): ((3*face_size + local_X, 1), '>'),
                
                # 2 ^ maps to bottom side 6 ^
                (2, '^'): ((H, local_X),'^'),
                # 2 > maps to right side 5 <
                (2, '>'): ((3*face_size - (local_Y-1), 2*face_size), '<'),
                # 2 v maps to right side 3 <
                (2, 'v'): ((face_size + local_X, 2*face_size), '<'),

                # 3 < maps to top side 4 v
                (3, '<'): ((2*face_size+1, local_Y), 'v'),
                # 3 > maps to bottom side 2 ^
                (3, '>'): ((face_size, 2*face_size+local_Y),'^'),

                # 4 < maps to left side 1 >
                (4, '<'): ((face_size - (local_Y-1), face_size+1), '>'),
                # 4 ^ maps to left side 3 >
                (4, '^'): ((face_size + local_X, face_size+1), '>'),
                
                # 5 > maps to right side of 2 <
                (5, '>'): ((face_size - (local_Y-1),3*face_size), '<'),
                # 5 v maps to right side of 6 <
                (5, 'v'): ((3*face_size + local_X, face_size), '<'),

                # 6 < maps to 1 top side v
                (6 , '<'): ((1, face_size + local_Y), 'v'),
                # 6 v maps to 2 top side v
                (6, 'v'): ((1, 2*face_size + local_X), 'v'),
                # 6 > maps to 5 bottom side ^
                (6, '>'): ((3*face_size, face_size + local_Y), '^'),
                
            }[(face_N,facing)]
            pass
        assert(result[0] in jungle)
        return result

import functools
new_pos_3D_part2 = functools.partial(new_pos_3D, example=False)

def test_new_pos_3D():
    assert(((4,5),'v') == new_pos_3D({},16,12, (1,9),'<'))

def solve(d, new_pos_func = new_pos_2D):
    jungle, movements, start_pos = parse(d)
    W = max(p[1] for p in jungle)
    H = max(p[0] for p in jungle)

    movement_map = jungle.copy()

    facing = '>'
    pos = start_pos
    
    for m in movements:
        if 'turn' in m:
            turn = m['turn']
            facing = TURN_TABLE[facing][turn]   
            continue


        num_steps = m['steps']
        D = DIRS[facing]
        movement_map[pos] = facing

        new_pos = pos
        prev_pos = pos
        prev_facing = facing
        for _ in range(num_steps):
            new_pos, facing = new_pos_func(jungle, W, H, new_pos, facing)
            v = jungle[new_pos]
            if v == '#':
                # hit wall so step back
                pos = prev_pos
                facing = prev_facing
                break
            pos = new_pos
            assert(v == '.')
            movement_map[pos] = facing
        
            prev_pos = pos
            prev_facing = facing


    movement_map[pos] = 'E'
    
    if False:
        for y in range(1,H+1):
            print(f'{y:3} ',end='')
            for x in range(1,W+1):
                print(movement_map.get((y,x),' '), end='')
            print()

    return 1000*pos[0] + 4*pos[1] + '>v<^'.index(facing)
            

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(6032 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(result == 65368)

def test_example2():
    result = solve(EXAMPLE_DATA, new_pos_func=new_pos_3D)
    assert(5031 == result)

def tets_part2():
    result = solve(data(), new_pos_func=new_pos_3D_part2)
    print('PART 2:', result)
    assert(result == 156166)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    tets_part2()
