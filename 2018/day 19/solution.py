# Advent of code - 2018
#
# Day 19
#
# Pieter Kitslaar
#

from pathlib import Path
THIS_DIR = Path(__file__).parent

from collections import defaultdict

class CPU(object):

    def __init__(self):
        self.instruction_pointer = None
        self.registers = defaultdict(int)
        self.all_instructions = [
            (getattr(self, method_name), method_name) for method_name in dir(self)
            if method_name.startswith('i_')]

    def get_r(self, x):
        return self.registers[x]

    def set_r(self, x, y):
        self.registers[x] = y

    def call(self, i_name, *args):
        return getattr(self, i_name)(*args)

    def i_addr(self, a, b, c):
        self.set_r(c, self.get_r(a) + self.get_r(b))

    def i_addi(self, a, b, c):
        self.set_r(c, self.get_r(a) + b)

    def i_mulr(self, a, b, c):
        self.set_r(c, self.get_r(a) * self.get_r(b))

    def i_muli(self, a, b, c):
        self.set_r(c, self.get_r(a) * b)

    def i_banr(self, a, b, c):
        self.set_r(c, self.get_r(a) & self.get_r(b))

    def i_bani(self, a, b, c):
        self.set_r(c, self.get_r(a) & b)

    def i_borr(self, a, b, c):
        self.set_r(c, self.get_r(a) | self.get_r(b))

    def i_bori(self, a, b, c):
        self.set_r(c, self.get_r(a) | b)

    def i_setr(self, a, b, c):
        self.set_r(c, self.get_r(a))

    def i_seti(self, a, b, c):
        self.set_r(c, a)

    def i_gtir(self, a, b, c):
        self.set_r(c, 1 if a > self.get_r(b) else 0)

    def i_gtri(self, a, b, c):
        self.set_r(c, 1 if self.get_r(a) > b else 0)

    def i_gtrr(self, a, b, c):
        self.set_r(c, 1 if self.get_r(a) > self.get_r(b) else 0)

    def i_eqir(self, a, b, c):
        self.set_r(c, 1 if a == self.get_r(b) else 0)

    def i_eqri(self, a, b, c):
        self.set_r(c, 1 if self.get_r(a) == b else 0)

    def i_eqrr(self, a, b, c):
        self.set_r(c, 1 if self.get_r(a) == self.get_r(b) else 0)

    def setup(self, values):
        self.registers = defaultdict(int)
        for i, v in enumerate(values):
            self.registers[i] = v

    def dump(self):
        highest_register = max(self.registers) if self.registers else -1
        return [self.registers[i] for i in range(highest_register+1)]


def execute_program(txt_data, initial_data = [0]*6, initial_ip = 0):
    ip_adress = None
    instructions = []
    for l in txt_data.splitlines():
        if l.startswith('#ip'):
            ip_adress = int(l.split('#ip ')[-1])
        else:
            op_code, call_args = l.split(' ',1)
            instructions.append((f"i_{op_code}", [int(a) for a in call_args.strip().split()]))

    ip = initial_ip
    cpu = CPU()
    cpu.setup(initial_data)
    ips = [ip]
    while True:
        if ip >= len(instructions):
            break
        before_ip = ip
        op_name, call_args = instructions[ip]
        cpu.set_r(ip_adress, ip)
        before = cpu.dump()
        cpu.call(op_name, *call_args)
        after = cpu.dump()
        ip = cpu.get_r(ip_adress) + 1        
    return cpu.dump()

example="""\
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

def test_example():
    registers = execute_program(example)
    print('Example:', registers[0], registers)

with open(THIS_DIR / 'input.txt') as f:
    data = f.read()

def fast_compute_naive(initial_register = [0]*6):
    """
    Implementation based on annotated analysis of the program.
    See input_annotated.txt

    Here we bascially recreate the entire CPU logic as simple Python code
    """
    r = initial_register[:]
    
    # setup
    if r[0] == 0:
        r[1] = 900
    else:
        r[1] = 10551300

    for r5 in range(1,r[1]+1):
        r[5] = r5
        for r4 in range(1, r[1]+1):
            r[4] = r4
            if r[4]*r[5] == r[1]:
                r[0] += r[5]
    return r[0]

def fast_compute(initial_register = [0]*6):
    """
    Implementation based on annotated analysis of the program.
    See input_annotated.txt

    Here we short-cut the two loops by taking into account we only
    need to values for r[5] that are a valid in the equation 
    r[1] = r[4]*r[5]

    So dividing r[1] by all possible values of r[5] and seeing of r[4]
    is a valid integer gives all the values for r[5] we need to sum.
    """
    r = initial_register[:]
    
    # setup
    if r[0] == 0:
        r[1] = 900
    else:
        r[0] = 0
        r[1] = 10551300

    for r5 in range(1,r[1]+1):
        r4, mod = divmod(r[1], r5)        
        if mod == 0:
            r[0] += r5
    return r[0]


def test_simple():
    # PART 1
    registers = execute_program(data, [0,3,0,0,0,0], initial_ip=1)
    #registers = execute_program(data, [1, 900, 0, 2, 900, 900], 3)
    print('PART 1:', registers[0], registers)

def test_part1():
    # PART 1
    registers = execute_program(data)
    #registers = execute_program(data, [1, 900, 0, 2, 900, 900], 3)
    print('PART 1:', registers[0], registers)

def test_part1_fast():
    # PART 1    
    #registers = execute_program(data, [1, 900, 0, 2, 900, 900], 3)
    result = fast_compute()    
    print('PART 1:', result)
    assert(result == 2821)

def test_part2():
    # PART 2
    registers = execute_program(data, [1])
    print('PART 2:', registers[0], registers)

def test_part2_fast():
    # PART 2    
    result = fast_compute([1]+[0]*5)    
    print('PART 2:', result)
    assert(result == 30529296)

if __name__ == "__main__":
    #test_example()
    test_part1_fast()
    test_part2_fast()







