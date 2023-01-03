"""
Advent of Code 2022 - Day 17
Pieter Kitslaar
"""

from pathlib import Path
from turtle import st
THIS_DIR = Path(__file__).parent


def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read().strip()

class Rock:
    def __init__(self, offsets):
        self.offsets = offsets
        self.width = max(o[0] for o in self.offsets)
        self.height = max(o[1] for o in self.offsets)
    
    def at_position(self, pos):
        for o in self.offsets:
            yield (o[0]+pos[0], o[1]+pos[1])


ROCKS=[*map(Rock,[
    #     x=0
    #      v
    # y=0  ####
    ((0,0),(1,0),(2,0),(3,0)),

    #     x=0
    #      v
    # y=2  .#.
    #      ###
    # y=0  .#.
    (      (1,2),
    (0,1), (1,1), (2,1),
           (1,0)
    ),

    #     x=0
    #      v
    # y=2  ..#
    #      ..#
    # y=0  ###
    (             (2,2),
                  (2,1),
    (0,0), (1,0), (2,0)
    ),

    #     x=0
    #      v
    # y=3  #
    #      #
    #      #
    # y=0  #
    ((0,3),
     (0,2),
     (0,1), 
     (0,0),
    ),

    #     x=0
    #      v
    # y=1  ##
    # y=0  ##
    ((0,1),(1,1),
     (0,0),(1,0),
    ),
])]

EXAMPLE_DATA="""\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""


def solve(d, N=2022, fast=False):
    JET_DIRS = d
    jet_index = 0
    JET_TO_X_OFFSET={'>':1,'<':-1}

    cave = {}
    def hits_other_rock(rock, rock_pos):
        for o_pos in rock.at_position(rock_pos):
            if o_pos in cave:
                return True
        return False

    def print_cave(rock, rock_pos, rock_char='*'):
        if rock_char!='*':
            return
        max_y = highest_rock_y
        rock_in_cave = {}
        if rock:
            rock_in_cave = {p:rock_char for p in rock.at_position(rock_pos)}
            max_y = max([*[p[1] for p in rock_in_cave], max_y ])
        for y in range(max_y,-1,-1):
            print(f"{y:4} ", end='')
            for x in range(0,7):
                print(cave.get((x,y),rock_in_cave.get((x,y),'.')), end='')
            print()
        print()

    highest_rock_y = 0
    num_rocks_stopped = 0
    rock_index = 0
    current_rock = None
    current_rock_origin = None

    next_action = "JET" # or FALL

    # for fast solution with cycle detection
    cycle_items = []
    cycle_values = []
    num_cycles_found = 0
    
    if True:
        while num_rocks_stopped < N:
                
            if not current_rock:
                if fast:
                    top_layer = ''.join([cave.get((x,highest_rock_y-1),'.') for x in range(7)])
                    current_state = (rock_index, jet_index, top_layer)
                    if top_layer.count('#') == 4 and current_state in cycle_items:
                        start_cycle = cycle_items.index(current_state)
                        cycle_items = cycle_items[start_cycle:] + [current_state]
                        new_cycle_values = cycle_values[start_cycle:] + [highest_rock_y]

                        # full cycle available
                        prev_v = cycle_values[start_cycle]
                        stack_incr_per_block = []
                        for v in new_cycle_values[1:]:
                            stack_incr_per_block.append(v- prev_v)
                            prev_v = v

                        num_remaining = N - num_rocks_stopped
                        num_cycles = num_remaining // len(stack_incr_per_block)
                        stack_size_per_cycle = sum(v for v in stack_incr_per_block)
                        remaining_blocks = num_remaining % len(stack_incr_per_block)
                        remaining_size = sum(v for v in stack_incr_per_block[:remaining_blocks])
                        result = highest_rock_y + num_cycles*stack_size_per_cycle + remaining_size
                        return result
                        
                    cycle_items.append((rock_index, jet_index, top_layer))
                    cycle_values.append(highest_rock_y)  

                # new rock appears
                current_rock = ROCKS[rock_index]
                rock_index = (rock_index+1) % len(ROCKS) # setup for next cycle
                current_rock_origin = (2,3+highest_rock_y)
                next_action = "JET"


            if next_action == "JET":
                jet_dir = JET_DIRS[jet_index]
                #print(next_action, jet_dir, jet_index)

                jet_index = (jet_index+1) % len(JET_DIRS) # cycle to new jet for next round
                next_action = "FALL"


                x_offset = JET_TO_X_OFFSET[jet_dir]
                new_rock_origin = (current_rock_origin[0]+x_offset, current_rock_origin[1])
                if new_rock_origin[0] < 0 or new_rock_origin[0]+current_rock.width > 6:
                    # hit the wall
                    pass
                elif hits_other_rock(current_rock, new_rock_origin):
                    # hit other rock
                    pass
                else:
                    # all OK update the position
                    current_rock_origin = new_rock_origin
            elif next_action == "FALL":
                #print(next_action)
                next_action = "JET" 

                new_rock_origin = (current_rock_origin[0], current_rock_origin[1]-1)
                stopped = False
                if new_rock_origin[1] < 0:
                    # hit the floor
                    stopped = True
                elif hits_other_rock(current_rock, new_rock_origin):
                    stopped = True
                else:
                    current_rock_origin = new_rock_origin
                
                if stopped:
                    num_rocks_stopped += 1
                    cave.update({p:'#' for p in current_rock.at_position(current_rock_origin)})
                    highest_rock_y = max(p[1] for p,v in cave.items() if v=='#') +1#[highest_rock_y, current_rock_origin[1]+current_rock.height+1])
                    current_rock = None # trigger new rock to appear
            else:
                raise ValueError(f"Unknown action {next_action}")
    return highest_rock_y
                

def test_example():
    result = solve(EXAMPLE_DATA, N=2022, fast=True)
    assert(3068 == result)

def test_part1():
    result =solve(data(), fast=True)
    print('PART 1:', result)
    assert(3147 == result)

PART2_N = 1_000_000_000_000

def test_example2():
    result = solve(EXAMPLE_DATA, N=PART2_N, fast=True)
    assert(1514285714288 == result)

def test_part2():
    result = solve(data(), N=PART2_N, fast=True)
    print('PART 2:', result)
    assert(1532163742758 == result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()