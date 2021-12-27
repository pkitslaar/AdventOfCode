"""
Advent of Code 2021 - Day 24
Pieter Kitslaar
"""

from pathlib import Path
import json

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def parse(txt):
    program = []
    for line in txt.splitlines():
        program.append(tuple(line.split()))
    return program

class ALU:

    def __init__(self, program_or_txt, inputs):
        self.reg = {'w':0, 'x': 0, 'y': 0, 'z': 0}
        if isinstance(program_or_txt, str):
            program_or_txt = parse(program_or_txt)
        self.program = program_or_txt
        self.program_counter = 0
        self.inputs = inputs
        self.input_counter = 0

    def next_code(self):
        code = self.program[self.program_counter]
        self.program_counter += 1
        return code
    
    def next_input(self):
        v = self.inputs[self.input_counter]
        self.input_counter += 1
        return v

    def value(self, reg_or_number):
        try:
            return self.reg[reg_or_number]
        except KeyError:
            return int(reg_or_number)
        
    def exec_next(self):
        code = self.next_code()
        if code[0] == 'inp':
            self.reg[code[1]] = self.next_input()
        elif code[0] == 'add':
            self.reg[code[1]] = self.reg[code[1]] + self.value(code[2])
        elif code[0] == 'mul':
            self.reg[code[1]] = self.reg[code[1]] * self.value(code[2])
        elif code[0] == 'div':
            b = self.value(code[2])
            assert b != 0
            self.reg[code[1]] = int(self.reg[code[1]] / b)
        elif code[0] == 'mod':
            a = self.reg[code[1]]
            b = self.value(code[2])
            assert a >= 0
            assert b > 0
            self.reg[code[1]] = a % b
        elif code[0] == 'eql':
            self.reg[code[1]] = int(self.reg[code[1]] == self.value(code[2]))
        else:
            raise ValueError('unknown code:', code)
    
    def exec(self):
        num_exec = len(self.program) - self.program_counter
        for _ in range(num_exec):
            self.exec_next()



ex_negate = """\
inp x
mul x -1"""

def test_ex_negate():
    for i in [-100,-1,0,4,100]:
        alu = ALU(ex_negate, [i])
        alu.exec()
        assert -i == alu.reg['x']

ex_3_times_larger="""\
inp z
inp x
mul z 3
eql z x"""

def test_ex_3_times_larger():
    for a,b in [(-100,-300),(-100,300),(-1,-3),(-1,-2),(0,0),(4,12),(4,11),(100,299)]:
        alu = ALU(ex_3_times_larger, [a,b])
        alu.exec()
        assert int(a*3 == b) == alu.reg['z']

ex_bit_split="""\
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""

def test_ex_bit_split():
    for a in [0,1,2,4,8,16,2347,23451,3245,34534985]:
        alu = ALU(ex_bit_split, [a])
        alu.exec()
        bits = f'{a:04b}'
        assert int(bits[-1]) == alu.reg['z']
        assert int(bits[-2]) == alu.reg['y']
        assert int(bits[-3]) == alu.reg['x']
        assert int(bits[-4]) == alu.reg['w']

def MONAD(number_txt):
    assert len(number_txt)==14
    assert all(c!='0' for c in number_txt)
    a = ALU(get_input(),[*map(int,number_txt)])
    return a.reg['z']==0, a

def test_monad():
    result, _ = MONAD('13579246899999')
    assert True == result

def find_z0(d_program, wanted_values):
    A = int(d_program[5][2])
    B = int(d_program[-3][2])
    Z_DIV = int(d_program[4][2])
    print(f"> A={A}, B={B}, Z_DIV={Z_DIV}")

    X = lambda z_0,w: 1 if z_0%26 + A != w else 0
    x_zero_for_w = {}
    for z_0 in range(1,max(26,26-A)):
        for w in range(1,10):
            if X(z_0,w) == 0:
                x_zero_for_w[z_0]=w
    print('> z_zero', x_zero_for_w)

    Z = lambda z_0,w: 26*int(z_0/Z_DIV) + w + B if X(z_0,w) else int(z_0/Z_DIV)

    # - z_0 cannot be negative or zero
    # x == 0 ony when z_0 + A is in the range 1 to 9
    # A<=-25: x==0 never
    # A==-24: x==0 for w,z in [(1,25),                                                               ]
    # A==-23: x==0 for w,z in [(1,24), (2,25),                                                       ]
    # A==-22: x==0 for w,z in [(1,23), (2,24), (3,25),                                               ]
    # A==-21: x==0 for w,z in [(1,22), (2,23), (3,24), (4,25),                                       ]
    # A==-20: x==0 for w,z in [(1,21), (2,22), (3,23), (4,24), (5,25),                               ]
    # A==-19: x==0 for w,z in [(1,20), (2,21), (3,22), (4,23), (5,24), (6,25),                       ]
    # A==-18: x==0 for w,z in [(1,19), (2,20), (3,21), (4,22), (5,23), (6,24), (7,25),               ]
    # A==-17: x==0 for w,z in [(1,18), (2,19), (3,20), (4,21), (5,22), (6,23), (7,24), (8,25),       ]
    # A==-16: x==0 for w,z in [(1,17), (2,18), (3,19), (4,20), (5,21), (6,22), (7,23), (8,24), (9,25)]
    # A==-15: x==0 for w,z in [(1,16), (2,17), (3,18), (4,19), (5,20), (6,21), (7,22), (8,23), (9,24)]
    # A==-14: x==0 for w,z in [(1,15), (2,16), (3,17), (4,18), (5,19), (6,20), (7,21), (8,22), (9,23)]
    # A==-13: x==0 for w,z in [(1,14), (2,15), (3,16), (4,17), (5,18), (6,19), (7,20), (8,21), (9,21)]
    # ..
    # A==-2 : x==0 for w,z in [(1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (8,10), (9,11)]
    # A==-1 : x==0 for w,z in [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9,10)]
    # A== 0 : x==0 for w,z in [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
    # A== 1 : x==0 for w,z in [        (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8)]
    # A== 2 : x==0 for w,z in [                (3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (9, 7)]
    # A== 3 : x==0 for w,z in [                        (4, 1), (5, 2), (6, 3), (7, 4), (8, 5), (9, 6)]
    # A== 4 : x==0 for w,z in [                                (5, 1), (6, 2), (7, 3), (8, 4), (9, 5)]
    # A== 5 : x==0 for w,z in [                                        (6, 1), (7, 2), (8, 3), (9, 4)]
    # A== 6 : x==0 for w,z in [                                                (7, 1), (8, 2), (9, 3)]
    # A== 7 : x==0 for w,z in [                                                        (8, 1), (9, 2)]
    # A== 7 : x==0 for w,z in [                                                                (9, 1)]
    # A>= 8 : x==0 never

    w_for_z0 = {}
    x_solutions = {}
    #z_0_range = range(1,27+(-1*A)) if Z_DIV == 26 else range(1,27+A)
    for z_0 in range(1000000):
            #z_0 = z_0*26 if Z_DIV == 1 else z_0
            for w in range(1,10):
                #alu = ALU(d_program,[w])
                #alu.reg.update({'z':z_0,})
                #alu.exec()
                #z = alu.reg['z']
                z = Z(z_0,w)
                #assert z_fast == z
                if z in wanted_values:
                    w_for_z0.setdefault(z_0, []).append((w,z))
    print('> found', len(w_for_z0))
    return w_for_z0

def brute_force(splitted_monad_program):
    all_found = {}
    wanted_values = set([0])
    for d_i in range(13,-1,-1):
        print(d_i, ': finding num_wanted', len(wanted_values))
        w_for_z0 = find_z0(splitted_monad_program[d_i], wanted_values)
        all_found[d_i] = w_for_z0
        if w_for_z0:
            print(d_i, ': found', len(w_for_z0))
            #print(w_for_z0)
            wanted_values = set(w_for_z0)
        else:
            print(d_i, ': no soluton found for wanted values')
            print(wanted_values)
            return
    return all_found

def prepare():
    full_monad_program = parse(get_input())
    splitted_monad_program = []
    for p in full_monad_program:
        if p[0] == 'inp':
            splitted_monad_program.append([])
        splitted_monad_program[-1].append(p)

    all_found = brute_force(splitted_monad_program)
    with open(Path(__file__).parent / 'cache.json', 'w') as f:
        json.dump(all_found, f)

def test_part1():
    with open(Path(__file__).parent / 'cache.json', 'r') as f:
        all_found = json.load(f)
    
    last_z = 0
    w_parts = []
    for i in range(14):
        z_options = all_found[str(i)][str(last_z)]
        z_options.sort(key = lambda t: t[0])
        w, last_z = z_options[-1]
        w_parts.append(w)
    highest_number = "".join(map(str,w_parts))
    result_highest,_ = MONAD(highest_number)
    assert result_highest == True
    print('Part 1', highest_number)


def test_part2():
    with open(Path(__file__).parent / 'cache.json', 'r') as f:
        all_found = json.load(f)
    
    last_z = 0
    w_parts = []
    for i in range(14):
        z_options = all_found[str(i)][str(last_z)]
        z_options.sort(key = lambda t: t[0])
        w, last_z = z_options[0]
        w_parts.append(w)
    lowest_number = "".join(map(str,w_parts))
    result_lowest,_ = MONAD(lowest_number)
    assert result_lowest == True
    print('Part 2', lowest_number)



if __name__ == "__main__":
    test_ex_negate()
    test_ex_3_times_larger()
    test_ex_bit_split()
    test_monad()
    # prepare() # uncomment to run brute_force preparation for part 1 and part 2
    test_part1()
    test_part2()





