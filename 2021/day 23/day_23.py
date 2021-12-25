"""
Advent of Code 2021 - Day 23
Pieter Kitslaar
"""

from pathlib import Path

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

example="""\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""

example_1="""\
#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########"""

example_2="""\
#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########"""

done="""\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""

def dist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

ROOMS = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
T_ENERGY={'A':1, 'B': 10, 'C': 100, 'D': 1000}


class State:
    def __init__(self, burrow, energy=0):
        self.burrow = burrow
        self.energy = energy
        self.theoretical_best_energy = 0
        self.update_min_energy_to_done()

    def clone(self):
        return State(self.burrow.copy(), self.energy)

    def plot(self):
        y_max = max(p[0] for p in self.burrow)
        x_max = max(p[1] for p in self.burrow)
        for y in range(y_max+1):
            for x in range(x_max+1):
                print(self.burrow.get((y,x), ' '), sep='',end='')
            print()

    def is_done(self):
        for t, col in ROOMS.items():
            if self.burrow[(2,col)] != t:
                return False
        return True

    def update_min_energy_to_done(self):
        min_energy = 0
        pos_per_t = {}
        amphipods = [(p,v) for p,v in self.burrow.items() if v !='.']
        for p,t in amphipods:
            pos_per_t.setdefault(t,[]).append(p)
        for t, p in pos_per_t.items():
            required_col = ROOMS[t]
            distances = [(dist(p[i],(r,required_col)),i,r) for i in (0,1) for r in (2,3)]
            distances.sort(key = lambda t: t[0])
            closest = distances[0]
            closest_d, c_i, c_r  = closest
            other_d = [d for d in distances if d[1]!=c_i and d[2]!=c_r][0][0]
            min_energy += closest_d*T_ENERGY[t]
            min_energy += other_d*T_ENERGY[t]
        self.theoretical_best_energy = self.energy + min_energy

    def move_options(self):
        amphipods = [(p,v) for p,v in self.burrow.items() if v !='.']
        all_options = {}
        for pos, t in amphipods:
            options = all_options[(pos,t)] = []

            if pos[0] in (2,3):
                # in a room, lets find an option in the hall way
                in_wrong_room = pos[1] != ROOMS[t] 

                # let's find if we can move out of the room
                can_move_out = False
                if pos[0] == 3 and in_wrong_room:
                    # lowest position and we are in the wrong room
                    if self.burrow[(2,pos[1])] == '.':
                        # position above is empty
                        can_move_out=True
                elif pos[0] == 2:
                    neighbor_type = self.burrow[(3,pos[1])]
                    neighbor_in_wrong_room = ROOMS[neighbor_type] != pos[1]
                    if in_wrong_room or neighbor_in_wrong_room:
                        can_move_out = True
                
                if can_move_out:
                    # we can move out of the room
                    # let's see where we can move to in the hall way

                    # search to right
                    for x in range(pos[1],11+1):
                        if self.burrow[(1,x)] != '.':
                            break
                        elif x not in (3,5,7,9):
                            options.append((1,x))

                    # search to left
                    for x in range(pos[1],0,-1):
                        if self.burrow[(1,x)] != '.':
                            break
                        elif x not in (3,5,7,9):
                            options.append((1,x))
            else:
                # in the hall way
                # only option is to move to its own room
                target_col = ROOMS[t]
                target_row = None

                # find target room position
                upper_pos = (2,target_col)
                upper_v = self.burrow[upper_pos]
                lower_pos = (3,target_col)
                lower_v = self.burrow[lower_pos]
                if upper_v == '.':
                    if lower_v == '.':
                        target_row=3
                    elif lower_v == t:
                        target_row=2
                
                # if we have an empty slot in our room
                # we need to know if we can reach it
                if target_row is not None:
                    direction = [-1,1][target_col > pos[1]]
                    can_reach = True
                    for x in range(pos[1]+direction,target_row+direction,direction):
                        if self.burrow[(1,x)] != '.':
                            can_reach = False
                            break
                    if can_reach:
                        # no break we are able to reach the room
                        options.append((target_row, target_col))
        return {k:v for k,v  in all_options.items() if v}



def parse(txt):
    burrow = {}
    for y, line in enumerate(txt.splitlines()):
        for x, v in enumerate(line):
            if v not in(' ',"#",''):
                burrow[(y,x)]=v
    return State(burrow)

def test_state():
    e = parse(example)
    assert e.is_done() == False
    
    d = parse(done)
    assert d.is_done() == True
    d_options = d.move_options()
    assert len(d_options) == 0

def solve(state: State):
    state.update_min_energy_to_done()
    best_solution = None
    states  = [state]
    while states:
        new_states = []
        s = states.pop()
        if best_solution and s.energy > best_solution.energy:
            continue
        s_options = s.move_options()
        for (amp_pos, amp_t), options in s_options.items():
            for op in options:
                num_steps = abs(op[0]-amp_pos[0])+abs(op[1]-amp_pos[1])
                added_energy = num_steps*T_ENERGY[amp_t]
                new_s : State = s.clone()
                new_s.burrow[amp_pos]='.'
                new_s.burrow[op] = amp_t
                new_s.energy += added_energy
                new_s.update_min_energy_to_done()
                if not best_solution or (new_s.theoretical_best_energy < best_solution.energy):
                    if new_s.is_done():
                        print('found solution', new_s.energy)
                        best_solution = new_s
                        #s.plot()
                    else:
                        new_states.append(new_s)

        states.extend(new_states)
        states.sort(key=lambda s: s.theoretical_best_energy)
        if best_solution:
            states = [s for s in states if s.theoretical_best_energy < best_solution.energy]
        #print(len(states))
    return best_solution.energy

example_3="""\
#############
#.....D.D.A.#
###.#B#C#.###
  #A#B#C#.#
  #########
"""

example_b="""\
#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########"""
def test_example():
    e= parse(example)
    #e.energy = 3510#+2003
    solve(e)

    #solve(parse(example_1))

    #solve(parse(example_2))

def test_part1():
    result = solve(parse(get_input()))
    print('Part 1', result)
    assert 14546 == result


if __name__ == "__main__":
    #test_state()
    #test_example()
    test_part1()