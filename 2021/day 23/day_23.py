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
    def __init__(self, burrow, energy=0, y_max = None, room_rows=None):
        self.burrow = burrow
        self.y_max = y_max or max(p[0] for p in self.burrow)
        self.room_rows = room_rows or [*range(2,self.y_max+1)]
        self.energy = energy

    def clone(self):
        return State(self.burrow.copy(), energy=self.energy, y_max=self.y_max, room_rows=self.room_rows)

    def plot(self):
        x_max = max(p[1] for p in self.burrow)
        for y in range(self.y_max+1):
            for x in range(x_max+1):
                print(self.burrow.get((y,x), ' '), sep='',end='')
            print()

    def is_done(self):
        for t, col in ROOMS.items():
            for row in range(2, self.y_max+1):
                if self.burrow[(row,col)] != t:
                    return False
        return True

    def move_options(self):
        amphipods = [(p,v) for p,v in self.burrow.items() if v !='.']
        all_options = []
        for pos, t in amphipods:
            t_room = ROOMS[t]

            if pos[1] == t_room and pos[0]>1 and all(self.burrow[(r,t_room)]==t for r in range(pos[0]+1,self.y_max+1)):
                    # amphi already on correct location
                    continue
            
            if True:
                visited = set()
                front = [pos]
                visited.add(pos)

                while front:
                    current = front.pop()
                    N = [(0,-1),(0,1),(-1,0)] # left, right and up always allowed
                    if current[1] == t_room:
                        N.append((1,0)) # allow to move down in own room
                    for n in N:
                        n_pos = (current[0]+n[0],current[1]+n[1])
                        if n_pos not in visited:
                            n_v = self.burrow.get(n_pos)
                            if n_v == '.':
                                front.append(n_pos)
                                visited.add(n_pos)
                visited.remove(pos)

                if pos[0] > 1: # only give hall way positions as option when currently in a room
                    all_options.extend([((pos,t),p) for p in visited if p[0]==1 and (p[1] not in (3,5,7,9))])

                if pos[0] == 1:
                    # check positions ending up in target room
                    t_room_pos = [p for p in visited if p[1]==t_room and p[0]!=1]
                    if t_room_pos:
                        t_room_pos.sort() # sort based on row and take the highest
                        best_t_room_pos = t_room_pos[-1]
                        
                        allowed = True
                        for r in range(best_t_room_pos[0]+1,self.y_max+1):
                            if self.burrow[(r,best_t_room_pos[1])] != t:
                                allowed = False
                        
                        if allowed:
                            # found best end position in room
                            return [((pos, t), best_t_room_pos)]
                            #all_options.append((pos,best_t_room_pos))


            if False:
                if pos[0] in self.room_rows:
                    # check if the space above is empty
                    above_empty = True
                    for r in range(2,pos[0]):
                        if self.burrow[(r,pos[1])] != '.':
                            above_empty = False
                            break

                    # let's find if we can move out of the room
                    can_move_out = False
                    if above_empty:
                        for r in range(pos[0],self.y_max+1):
                            n_t = self.burrow[(r,pos[1])]
                            if  n_t != '.' and ROOMS[n_t] != pos[1]:
                                # somebody is in the wrong room
                                can_move_out = True
                                break

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
                    for row in range(self.y_max, 1, -1):
                        v_row = self.burrow[(row,target_col)]
                        if v_row == '.':
                            target_row = row
                            break
                        elif v_row != t:
                            # row does not contain same types
                            break

                    for t_pos in [pos]:
                        # if we have an empty slot in our room
                        # we need to know if we can reach it
                        if target_row is not None:
                            direction = [-1,1][target_col > t_pos[1]]
                            can_reach = True
                            for x in range(t_pos[1]+direction,target_row+direction,direction):
                                if self.burrow[(1,x)] != '.':
                                    can_reach = False
                                    break
                            if can_reach:
                                # no break we are able to reach the room
                                options.append((target_row, target_col))
        #return {k:v for k,v  in all_options.items() if v}
        return all_options



def parse(txt):
    burrow = {}
    for y, line in enumerate(txt.splitlines()):
        for x, v in enumerate(line):
            if v not in(' ',"#",''):
                burrow[(y,x)]=v
    return State(burrow)

def plot_options(state):
    for amp, options in state.move_options().items():
        print(amp)
        c= state.clone()
        c.burrow[amp[0]] = '*'
        for op in options:
            c.burrow[op] = amp[1].lower()
        c.plot()
        print()
        print()

done_1="""\
#############
#.......D...#
###A#B#C#.###
  #A#B#C#D#
  #########"""

def test_state():
    e = parse(example)
    assert e.is_done() == False
    #plot_options(e)

    d = parse(done)
    plot_options(d)
    assert d.is_done() == True
    #d_options = d.move_options()
    #assert len(d_options) == 0

import heapq

def solve(state: State):
    best_solution = None
    states  = [state]
    while states:
        new_states = []
        s = states.pop()
        if best_solution and s.energy > best_solution.energy:
            continue
        s_options = s.move_options()
        for (amp_pos, amp_t), op in s_options:
            #for op in options:
                num_steps = abs(op[0]-amp_pos[0])+abs(op[1]-amp_pos[1])
                added_energy = num_steps*T_ENERGY[amp_t]
               
                if not best_solution or ((s.energy+added_energy) < best_solution.energy):
                    new_s : State = s.clone()
                    new_s.burrow[amp_pos]='.'
                    new_s.burrow[op] = amp_t
                    new_s.energy += added_energy

                    if new_s.is_done():
                        print('found solution', new_s.energy, len(states))
                        best_solution = new_s
                    else:
                        new_states.append(new_s)

        states.extend(new_states)
        states.sort(key=lambda s: s.energy)
        if best_solution:
            states = [s for s in states if s.energy < best_solution.energy]
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
    result = solve(parse(example))
    print(result)
    assert 12521 == result


def test_part1():
    result = solve(parse(get_input()))
    print('Part 1', result)
    assert 14546 == result


example_part_2="""\
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########"""

def test_example_part2():
    result = solve(parse(example_part_2))
    print(result)
    assert 12521 == result

part2 = """\
#############
#...........#
###D#A#D#C###
  #D#C#B#A#
  #D#B#A#C#
  #C#A#B#B#
  #########"""

def test_part2():
    result = solve(parse(part2))
    print('Part 2', result)
    assert 42308 == result


if __name__ == "__main__":
    #test_state()
    #print('example')
    #test_example()
    #test_part1()
    #test_example_part2()
    test_part2()