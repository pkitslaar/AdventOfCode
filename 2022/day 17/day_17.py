"""
Advent of Code 2022 - Day 17
Pieter Kitslaar
"""

from pathlib import Path
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

from tqdm import tqdm

def solve(d, N=2022, part2=False):
    #print(f"N rocks = {len(ROCKS)}")
    #print(f"N dirs = {len(d)}")
    JET_DIRS = d
    jet_index = 0
    JET_TO_X_OFFSET={'>':1,'<':-1}
    prev_combos = {}
    cave = {}
    def hits_other_rock(rock, rock_pos):
        for o_pos in rock.at_position(rock_pos):
            if o_pos in cave:
                return True
        return False

    def print_cave(rock, rock_pos, rock_char='@'):
        if rock_char!='*':
            return
        max_y = highest_rock_y
        rock_in_cave = {}
        if rock:
            rock_in_cave = {p:rock_char for p in rock.at_position(rock_pos)}
            max_y = max([*[p[1] for p in rock_in_cave], max_y ])
        for y in range(max_y,-1,-1):
            for x in range(0,7):
                print(cave.get((x,y),rock_in_cave.get((x,y),'.')), end='')
            print()
        print()
    cave_y_offset = 0
    highest_rock_y = 0
    num_rocks_stopped = 0
    rock_index = 0
    current_rock = None
    current_rock_origin = None
    next_action = "JET" # or FALL
    cycle_items = []
    cycle_values = []
    #with tqdm(total=N, disable=True) as pbar:
    num_cycles_found = 0
    if True:
        while num_rocks_stopped < N:
                
            #print_cave(current_rock, current_rock_origin)

            if not current_rock:
                if part2:
                    if (rock_index, jet_index) in cycle_items:
                        start_cycle = cycle_items.index((rock_index,jet_index))
                        cycle_items = cycle_items[start_cycle:]
                        cycle_values = cycle_values[start_cycle:]
                        num_cycles_found += 1
                        # full cycle available
                        print(f'FULL CYCLE {len(cycle_items)}')
                        prev_v = cycle_values[0]
                        stack_incr_per_block = {}
                        for t,v in zip(cycle_items, cycle_values):
                            stack_incr_per_block[t] = v- prev_v
                            prev_v = v

                        num_remaining = N - num_rocks_stopped
                        num_cycles = num_remaining // len(cycle_items)
                        stack_size_per_cycle = sum(stack_incr_per_block[t] for t in cycle_items)
                        remaining_blocks = num_remaining % len(cycle_items)
                        remaining_size = sum(stack_incr_per_block[t] for t in cycle_items[:remaining_blocks])
                        
                        result = cave_y_offset + highest_rock_y + num_cycles*stack_size_per_cycle + remaining_size
                        print(f"{num_remaining=} {num_cycles=} {remaining_blocks=} {remaining_size=} {highest_rock_y=} {result=}")
                       
                        if num_cycles_found == 1:
                            print('Using result from cycle detection')
                            return result
                        cycle_items = []
                        #return cave_y_offset + highest_rock_y + num_cycles*stack_size_per_cycle + remaining_size
                    cycle_items.append((rock_index, jet_index))
                    cycle_values.append(highest_rock_y)  
                
                    #if (rock_index, jet_index) in prev_combos:
                    #    cycle_items.append((rock_index, jet_index))
                    #    #print('Repeat', (rock_index, jet_index), prev_combos[(rock_index, jet_index)], highest_rock_y)
                    #else:
                    #    if cycle_items:
                    #        cycle_items.append((rock_index, jet_index))
                    #    #print('New   ', (rock_index, jet_index), highest_rock_y)

                    #rev_combos.setdefault((rock_index, jet_index),[]).append(highest_rock_y)
                # new rock appears
                current_rock = ROCKS[rock_index]
                rock_index = (rock_index+1) % len(ROCKS) # setup for next cycle
                current_rock_origin = (2,3+highest_rock_y)
                next_action = "JET"
                #print_cave(current_rock, current_rock_origin, '*')


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
                    #pbar.update(1)
                    cave.update({p:'#' for p in current_rock.at_position(current_rock_origin)})
                    highest_rock_y = max([highest_rock_y, current_rock_origin[1]+current_rock.height+1])
                    current_rock = None # trigger new rock to appear

                    if False: #part2:
                        # prune the cave to reduce memory
                        # find the higehst Y value for each X-pos in the cave
                        # take the minimum of these Y-values.
                        # Anything below this value is no longer relevant
                        max_y_for_x =[]
                        for x in range(7):
                            y_at_x = [p[1] for p in cave if p[0]==x]
                            max_y_for_x.append(max(y_at_x) if y_at_x else -1)
                        lowest_y = max([0,min(max_y_for_x)-4])
                        if lowest_y > 0:
                            cave_y_offset += lowest_y
                            highest_rock_y -= lowest_y
                            cave = {(p[0],p[1]-lowest_y):v for p,v in cave.items() if p[1] >= lowest_y}
            else:
                raise ValueError(f"Unknown action {next_action}")
    return cave_y_offset+highest_rock_y
                

def test_example():
    result_naive = solve(EXAMPLE_DATA, N=20_000)
    print(f"{result_naive=}")
    result_fast = solve(EXAMPLE_DATA, N=20_000, part2=True)
    print(f"naive={result_naive} fast={result_fast}: {result_fast==result_naive}")
    assert(result_naive == result_fast)
    #result = solve(EXAMPLE_DATA, N=2021, part2=True)
    #assert(3068 == result)

def test_part1():
    result =solve(data(), part2=True)
    print('PART 1:', result)
    assert(3147 == result)

PART2_N = 1_000_000_000_000

def test_example2():
    result = solve(EXAMPLE_DATA, N=PART2_N, part2=True)
    assert(1514285714288 == result)

def test_part2():
    for N2 in range(1747,PART2_N):
        result_naive = solve(data(), N=N2, part2=False)
        result_fast = solve(data(), N=N2, part2=True)
        print(f"{N2} naive={result_naive} fast={result_fast}: {result_fast==result_naive}")
        assert(result_naive == result_fast)
    #result = solve(data(), N=PART2_N, part2=True)
    #assert(result < 1992395436241) # was too high
    #assert(result > 1532163742756) # was too low
    #print('PART 2:', result)

if __name__ == "__main__":
    #test_example()
    #test_part1()
    #test_example2()
    test_part2()
