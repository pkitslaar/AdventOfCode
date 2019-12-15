import math
import re
MOON_RE = re.compile('<x=(.+), y=(.+), z=(.+)>')

class Moon:
    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = velocity
    
    def total_energy(self):
        return sum(map(abs, self.pos)) * sum(map(abs, self.velocity))

    def __repr__(self):
        return "pos=<x={0[0]}, y={0[1]}, z={0[2]}>, vel=<x={1[0]}, y={1[1]}, z={1[2]}>".format(self.pos, self.velocity)
    
    def state(self):
        return tuple([tuple(self.pos), tuple(self.velocity)])

def parse_moons(txt):
    moons = []
    for l in txt.strip().splitlines():
        if (m := MOON_RE.match(l)) is not None:
            moons.append(Moon(pos = list(map(int, m.groups())), velocity=[0,0,0]))
        else:
            raise ValueError(l)
    return moons

def print_moons(moons):
    for m in moons:
        print(m)
    print()

def apply_gravity(moons, axes=(0,1,2)):
    for M in moons:
        for m in moons:
            if m != M:
                for axis in axes:
                    M.velocity[axis] += int(math.copysign(1, pos_diff)) if (pos_diff := m.pos[axis] - M.pos[axis]) != 0 else 0
    return moons

def apply_velocity(moons, axes=(0,1,2)):
    for m in moons:
        for axis in axes:
            m.pos[axis] += m.velocity[axis]
    return moons

def get_axis_state(moons, axis):
    if axis>-1:
        return tuple([(m.pos[axis],m.velocity[axis]) for m in moons])
    else:
        return tuple([m.state() for m in moons])


def find_period(data, axis):
    moons = parse_moons(data)
    step = 0
    previous_states = {}
    previous_states[get_axis_state(moons, axis)] = step
    while True:
        step += 1
        apply_gravity(moons, (axis,))
        apply_velocity(moons, (axis,))
        new_state = get_axis_state(moons, axis)
        
        if new_state in previous_states:
            prev_step = previous_states[new_state]
            print(new_state, prev_step, step)
            print(f'Found repeat after {step} previous state was at step {prev_step}')
            return step - prev_step
            break
        previous_states[new_state] = step

def find_repeats(data):
    x_repeat = find_period(data, 0)
    y_repeat = find_period(data, 1)
    z_repeat = find_period(data, 2)
    i=0
    while True:
        i+=1
        steps = x_repeat*i
        if steps % y_repeat == 0 and steps % z_repeat == 0:
            print('Found', steps)
            return steps

ex1 = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>)"""

def test_ex1():
    print('ex1 repeats:', find_repeats(ex1))

ex2 = """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
def test_ex2():
    print('ex2 repeats:', find_repeats(ex2))

def main():
    from pathlib import Path
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        puzzle_data = f.read()
        puzzle_moons = parse_moons(puzzle_data)

    for i in range(1000):
        apply_gravity(puzzle_moons)
        apply_velocity(puzzle_moons)
    part1_sol = sum([m.total_energy() for m in puzzle_moons])
    print('Part 1:', part1_sol)
    assert(6849 == part1_sol)

    part2_solution = find_repeats(puzzle_data)
    print('Part 2', part2_solution)
    assert(356658899375688 == part2_solution)

if __name__ == "__main__":
    main()