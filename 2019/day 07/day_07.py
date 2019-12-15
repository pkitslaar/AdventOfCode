
import sys
from pathlib import Path
d5_dir = Path(__file__).parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))

from day_05 import run, txt_values

def test_intcode_basic():
    for in_, out_ in [("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),]:
        assert(txt_values(out_) == run(txt_values(in_))[1])


class Amp:
    def __init__(self, program, initial_values = None):
        self.program = program[:]
        self.position = 0
        self.outputs = []
        self.values = []
        if initial_values:
            self.values.extend(initial_values)

    def add_value(self, add_v):
        self.values.append(add_v)
    
    def __call__(self):
        v = self.values.pop(0)
        return v
    
    def run(self, output_cb=None):
        self.position, self.program, self.outputs = run(
            self.program, 
            input_v=self, 
            output_cb=output_cb, 
            current_pos=self.position)
        return self.outputs
    
    
def run_amp(program_code, inputs, output_cb=None):
    _, output = run(program_code[:], input_v=inputs, output_cb=output_cb)
    return output[-1]


def check_thrusters(program_code, phase_settings, feedback=False):
    amp_a = Amp(program_code, [phase_settings[0], 0])
    amp_b = Amp(program_code, [phase_settings[1]])
    amp_c = Amp(program_code, [phase_settings[2]])
    amp_d = Amp(program_code, [phase_settings[3]])
    amp_e = Amp(program_code, [phase_settings[4]])

    output_e = []
    prev_amp_a_in = None
    while True:
        amp_a.run(output_cb=amp_b.add_value)
        amp_b.run(output_cb=amp_c.add_value)
        amp_c.run(output_cb=amp_d.add_value)
        amp_d.run(output_cb=amp_e.add_value)
        amp_e.run(output_cb=amp_a.add_value if feedback else output_e.append)
        if feedback:
            if amp_a.values == prev_amp_a_in:
                break
            prev_amp_a_in = amp_a.values[:] 
        else:
            break
    return amp_a.values[-1] if feedback else output_e[0]


from itertools import permutations
def find_max(program_code):
    outputs = []
    for phase_settings in permutations(range(5), 5):
        v = check_thrusters(program_code, phase_settings)
        outputs.append((v,phase_settings))
    outputs.sort()
    return outputs[-1] if outputs else None


def test_ex1():
    ex1 = txt_values('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0')
    assert(43210 == check_thrusters(ex1, (4,3,2,1,0)))
    ex1_max = find_max(ex1)
    assert(43210 == ex1_max[0])
    assert((4,3,2,1,0) == ex1_max[1])

def test_ex2():
    ex2 = txt_values('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0')
    assert(54321 == check_thrusters(ex2, (0,1,2,3,4)))
    ex2_max = find_max(ex2)
    assert(54321 == ex2_max[0])
    assert((0,1,2,3,4) == ex2_max[1])

def test_ex3():
    ex3 = txt_values('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0')
    assert(65210 == check_thrusters(ex3, (1,0,4,3,2)))
    ex3_max = find_max(ex3)
    assert(65210 == ex3_max[0])
    assert((1,0,4,3,2) == ex3_max[1])

def find_max_feedback(program_code):
    outputs = []
    for phase_settings in permutations(range(5,10), 5):
        v = check_thrusters(program_code, phase_settings, True)
        outputs.append((v,phase_settings))
    outputs.sort()
    return outputs[-1] if outputs else None

def main():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        data = txt_values(f.read())

    part1_sol = find_max(data)
    print('Part 1', part1_sol[0])
    assert(67023 == part1_sol[0])

    part2_sol = find_max_feedback(data)
    print('Part 2', part2_sol[0])
    assert(7818398 == part2_sol[0])

if __name__ == "__main__":
    main()



