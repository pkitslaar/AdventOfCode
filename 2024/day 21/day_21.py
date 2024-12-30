"""
Advent of Code 2024 - Day 21
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
029A
980A
179A
456A
379A
"""

DOOR_PAD = """\
789
456
123
 0A
"""

CONTROL_PAD = """\
 ^A
<v>
"""	

def to_grid(pad):
    pad_to_pos = {}
    pos_to_pad = {}
    for y, line in enumerate(pad.splitlines()):
        for x, c in enumerate(line):
            if c == ' ':
                continue
            pad_to_pos[c] = (x, y)
            pos_to_pad[(x, y)] = c
    return pad_to_pos, pos_to_pad

class PadGrid():
    def __init__(self, pad):
        self.pad_to_pos, self.pos_to_pad = to_grid(pad)

DOOR_PAD_GRID = PadGrid(DOOR_PAD)
CONTROL_PAD_GRID = PadGrid(CONTROL_PAD)

from heapq import heappop, heappush


"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+ door pad               0
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

    ^  
    |   robot A                     <, push
    |
    -  Moving this robot arm costs effort. Therfore when finding the path to the next key we need to keep into 
       account the number of direction changes. As keeping moving in the same direction is less costly than changing direction. 

    +---+---+
    | ^ | A |
+---+---+---+ robot A pad           <, A  
| < | v | > |
+---+---+---+

    ^
    |  robot B                    v < < push, > > ^ push
    |
    -  Moving this robot arm costs effort. Therfore when finding the path to the next key we need to keep into 
       account the number of direction changes. As keeping moving in the same direction is less costly than changing direction.

    +---+---+
    | ^ | A |
+---+---+---+  robot B pad        v < < A, > > ^ A
| < | v | > |
+---+---+---+

    ^                            (v)       , (<)   , (<)    (A)
    | robot C                    < v push, < push  , push,  > > ^ push  
    |
    -  Moving this robot arm costs effort. However this key pad is NOT controlled by a robot arm so changing direction is not costly.
                        
    +---+---+
    | ^ | A |                     
+---+---+---+  robot C pad       < v A   , < A     , A   ,  > > ^ A
| < | v | > |
+---+---+---+    

    ^
    | me                                                                                                   < A

"""

DIRECTIONS = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}

# New approach is needed for part2
# This is inspired by looking at some Reddit solutions
# Key point is to keep track of all possible paths and not use the
# "best" path for each robot arm. As this changes depending on the number of robots

def find_grid_paths(grid, from_, to_):
    """
    Find all possible shortest paths from_ to to_ on the grid
    """
    queue = [(0, from_, '')]
    visited = {}
    while queue:
        current_cost, current_pad, steps = heappop(queue)
        if not current_pad in visited or visited[current_pad] >= current_cost:
            visited[current_pad] = current_cost
        else:
            continue
        
        if current_pad == to_:
            yield steps
            continue

        current_pos = grid.pad_to_pos[current_pad]
        for c, (dx, dy) in DIRECTIONS.items():
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            new_pos = (new_x, new_y)
            if new_pos in grid.pos_to_pad:
                new_pad = grid.pos_to_pad[new_pos]
                new_cost = current_cost + 1
                if not new_pad in visited or visited[new_pad] >= new_cost:
                    heappush(queue, (new_cost, new_pad, steps + c))

def create_grid_lookup(grid: PadGrid):
    # lookup table to move a robot arm from one pad to another and press the key
    lookup = {}
    for _from in grid.pad_to_pos:
        for _to in grid.pad_to_pos:
            keys = []
            if _from == _to:
                keys.append('A')
            else:
                for path in find_grid_paths(grid, _from, _to):
                    keys.append(path + 'A')
            lookup[(_from, _to)] = keys
    return lookup

from functools import lru_cache

def solve_fast2(data, part2=False):
    # lookup tables for moving a robot arm from one pad to another and pressing the key
    numpad_lookup = create_grid_lookup(DOOR_PAD_GRID)
    direction_lookup = create_grid_lookup(CONTROL_PAD_GRID)

    ROBOT_DEPTH = 2 if not part2 else 25

    @lru_cache(maxsize=None)
    def shortest_num_moves(moves, level):
        """
        Find the shortest number of moves for the robot arm at level to press all keys in moves.
        At level 0 the robot arm controlled by a human and all keys can be directly pressed.
        """
        if level == 0:
            return len(moves)
        else:
            num = 0
            
            # we know the robot arms always start in position 'A'
            # this is because at the end of each key press all arms have to be in position 'A'
            prev_m = 'A'
            for m in moves:
                all_min_moves = []
                for possible_path in direction_lookup[(prev_m, m)]:
                    all_min_moves.append(shortest_num_moves(possible_path, level - 1))
                prev_m = m
                num += min(all_min_moves)
            return num

    result = 0
    for code in data.strip().splitlines():
        code = code.strip()

        num_moves = 0
        prev_c = 'A'
        for c in code:
            all_min_moves = []
            for possible_path in numpad_lookup[(prev_c, c)]:
                all_min_moves.append(shortest_num_moves(possible_path, ROBOT_DEPTH))
            num_moves += min(all_min_moves)
            prev_c = c
        code_value = int(''.join(c for c in code if c.isnumeric()))
        result += code_value * num_moves
    return result

def test_example():
    result = solve_fast2(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 126384

def test_part1():
    result = solve_fast2(data())
    print("Part 1:", result)
    assert result == 125742
    

def test_part2():
    result = solve_fast2(data(), part2=True)
    print("Part 2:", result)
    assert result == 157055032722640

from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()