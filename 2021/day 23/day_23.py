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

ROOMS = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
T_ENERGY={'A':1, 'B': 10, 'C': 100, 'D': 1000}

class State:
    def __init__(self, burrow, energy=0, y_max = None, room_rows=None):
        self.burrow = burrow
        self.y_max = y_max or max(p[0] for p in self.burrow)
        self.room_rows = room_rows or [*range(2,self.y_max+1)]
        self.energy = energy

    def to_tuple(self):
        return tuple([*self.burrow.items(),self.energy])

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __eq__(self, __o: object) -> bool:
        return self.to_tuple()==__o.to_tuple()

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
                        return [((pos, t), best_t_room_pos)]
        return all_options

def parse(txt):
    burrow = {}
    for y, line in enumerate(txt.splitlines()):
        for x, v in enumerate(line):
            if v not in(' ',"#",''):
                burrow[(y,x)]=v
    return State(burrow)

done="""\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########"""

def test_state():
    e = parse(example)
    assert e.is_done() == False

    d = parse(done)
    assert d.is_done() == True

def solve(state: State):
    best_solution = None
    visisted = set()
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
                        if not new_s in visisted:
                            #heapq.heappush(states, new_s)
                            new_states.append(new_s)
                            visisted.add(new_s)

        states.extend(new_states)
        states.sort(key=lambda s: s.energy)
        if best_solution:
            states = [s for s in states if s.energy < best_solution.energy]
        #print(len(states))
    return best_solution.energy

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
    assert 44169 == result

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
    test_state()
    test_example()
    test_part1()
    test_example_part2()
    test_part2()