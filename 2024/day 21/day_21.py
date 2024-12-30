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

from collections import namedtuple
from dataclasses import dataclass


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

RobotState = namedtuple('RobotState', 'cost pad_grid current_pad pad_history')

DIRECTIONS = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}

def move_to_and_press(robot_chain, key):
        queue = [robot_chain]
        visited = set()
        while queue:
            current_chain = heappop(queue)
            visited.add(current_chain)

            current = current_chain[0]
            c_pad_grid: PadGrid = current.pad_grid
            c_pad = current.current_pad

            if current.current_pad == key:
                # we are at the key pad we want to press
                if len(current_chain) == 1:
                    # no other robot arms to move
                    # record the press of the key
                    chain_0 = current._replace(
                        cost = current.cost + 1,
                        pad_history = current.pad_history + key
                    )
                    return tuple([chain_0])
                else:
                    # we need to move the other robot arms
                    # to the 'A' pad and press it
                    new_end_chain = move_to_and_press(tuple(current_chain[1:]), 'A')
                    new_cost = current.cost + (new_end_chain[0].cost - current_chain[1].cost)
                    new_robot_chain_0 = current._replace(
                        cost = new_cost,
                        pad_history = current.pad_history + 'A'
                    )
                    return tuple([new_robot_chain_0, *new_end_chain])

            if len(current_chain) == 1:
                # no other robot arms to move
                # can "move" to the key pad instantly
                chain_0 = current._replace(
                    current_pad = key,
                )
                heappush(queue, tuple([chain_0]))
            else:

                for c, (dx, dy) in DIRECTIONS.items():
                    current_x, current_y = c_pad_grid.pad_to_pos[c_pad]
                    new_x, new_y = current_x + dx, current_y + dy
                    new_pos = (new_x, new_y)
                    if new_pos in c_pad_grid.pos_to_pad:
                        new_pad = c_pad_grid.pos_to_pad[new_pos]
                        # to move to this new pad we need to move the other robot arms
                        # by pressing the direction key 'c'
                        new_end_chain = move_to_and_press(tuple(current_chain[1:]), c)
                        new_cost = current.cost + (new_end_chain[0].cost - current_chain[1].cost)
                        new_robot_chain_0 = current._replace(
                            cost = new_cost,
                            current_pad = new_pad,
                            pad_history = current.pad_history + c
                        )
                        new_chain = tuple([new_robot_chain_0, *new_end_chain])
                        if new_chain not in visited:
                            heappush(queue, new_chain)

           


def solve(data, part2=False):
    result = 0
    NUM_ROBOTS = 3 if not part2 else 4

    for code in data.strip().splitlines():
        code = code.strip()

        robot_chain = tuple([RobotState(0, DOOR_PAD_GRID, 'A', '')] + 
                            [RobotState(0, CONTROL_PAD_GRID, 'A', '') for _ in range(NUM_ROBOTS)])
        
        for c in code:
            robot_chain = move_to_and_press(robot_chain, c)
 
        num_pushed = len(robot_chain[-1].pad_history)
        code_value = int(''.join(c for c in code if c.isnumeric()))
        result += code_value * num_pushed

    return result

def find_path(pad_grid, _from, _to, move_path_func):
    queue = [(
        0,      # cost 
        _from,  # current pad
        ['A'],     # previous directions
    )
    ]
    visited = {}
    while queue:
        current_cost, current_pad, prev_dirs = heappop(queue)
        if not current_pad in visited or visited[current_pad][0] > current_cost:
            visited[current_pad] = (current_cost, prev_dirs)
        
        if current_pad == _to:
            continue
        
        current_pos = pad_grid.pad_to_pos[current_pad]
        for c, (dx, dy) in DIRECTIONS.items():
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            new_pos = (new_x, new_y)
            if new_pos in pad_grid.pos_to_pad:
                new_dirs = prev_dirs + [c]
                new_cost = current_cost +  move_path_func(new_dirs)
                new_pad = pad_grid.pos_to_pad[new_pos]
                if not new_pad in visited or visited[new_pad][0] > new_cost:
                    heappush(queue, (new_cost, new_pad, new_dirs))
    return visited[_to]

def solve_fast(data, part2=False):
    result = 0
    NUM_ROBOTS = 2 if not part2 else 25

    # we can make lookup tables for the best moves for each robot
    # the first lookup is for the robot we are controlling
    robot_lookups = []
    robots = [CONTROL_PAD_GRID for _ in range(NUM_ROBOTS)] + [DOOR_PAD_GRID]
    for i, robot_grid in enumerate(robots):
        this_lookup = {}
        if i == 0:
            for _from in robot_grid.pad_to_pos:
                for _to in robot_grid.pad_to_pos:
                    if _from == _to:
                        continue
                    # find the shortest path from _from to _to
                    path_len, prev_dirs = find_path(robot_grid, _from, _to, lambda c_dirs: 1)
                    this_lookup[(_from, _to)] =  (path_len, prev_dirs[-1])
        else:
            for _from in robot_grid.pad_to_pos:
                for _to in robot_grid.pad_to_pos:
                    if _from == _to:
                        continue
                    # find the shortest path from _from to _to
                    def move_path_func(c_dirs):
                        c_from = c_dirs[-2]
                        c_to = c_dirs[-1]
                        if c_from == c_to:
                            return 1
                        return robot_lookups[i-1][(c_from, c_to)][0] + 1
                    move_path_len, prev_dirs = find_path(robot_grid, _from, _to, move_path_func)
                    if prev_dirs[-1] != 'A':
                        push_path_len, _ = robot_lookups[i-1][(prev_dirs[-1], 'A')]
                    this_lookup[(_from, _to)] =  (move_path_len + push_path_len, prev_dirs[-1])
        robot_lookups.append(this_lookup)

    for code in data.strip().splitlines():
        code = code.strip()

        full_path_len = 0

        prev_c = 'A'
        for c in code:
            move_path_len = robot_lookups[-1][(prev_c, c)][0] + 1
            full_path_len += move_path_len
            prev_c = c
        
        num_pushed = full_path_len
        code_value = int(''.join(c for c in code if c.isnumeric()))
        result += code_value * num_pushed

    return result


def test_example():
    result = solve_fast(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 126384


def test_part1():
    result = solve_fast(data())
    print("Part 1:", result)
    assert result < 128918
    assert result == 125742

def test_part2():
    result = solve_fast(data(), part2=True)
    print("Part 2:", result)
    assert result < 189678562616954
    assert result > 75714616077620
    


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()