# Advent of code - 2018
#
# Day 21
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


def execute_program(txt_data, initial_data = [0]*6, cb = None):
    ip_adress = None
    instructions = []
    for l in txt_data.splitlines():
        if l.startswith('#ip'):
            ip_adress = int(l.split('#ip ')[-1])
        else:
            op_code, call_args = l.split(' ',1)
            instructions.append((f"i_{op_code}", [int(a) for a in call_args.strip().split()]))

    ip = 0
    cpu = CPU()
    cpu.setup(initial_data)
    num_instructions = 0
    print(ip_adress)
    while True:
        if ip >= len(instructions):
            break
        if cb:
            cb(ip, cpu)
        op_name, call_args = instructions[ip]
        cpu.set_r(ip_adress, ip)
        before = cpu.dump()
        cpu.call(op_name, *call_args)
        num_instructions += 1
        after = cpu.dump()
        #print(f"ip={ip} {before} {op_name} {call_args} {after}")
        ip = cpu.get_r(ip_adress) + 1
    return cpu.dump(), num_instructions

def fast_execute(initial_data = [0]*6):
    r = initial_data[:]

    # ip=5
    r[3] = 0

    while True:
        
        # ip = 6, 7
        r[5] = r[3] | 65536
        r[3] = 15028787

        while True:
            # update r[3]
            # ip=8 - 12
            r[2] = r[5] & 255
            r[3] = r[3] + r[2]
            r[3] = r[3] & 16777215
            r[3] = r[3] * 65899
            r[3] = r[3] & 16777215

            if r[5] >= 256:
                # ip-17
                r[2] = 0

                # update r[4]
                while True:
                    r[4] = r[2] + 1
                    r[4] = r[4]*256

                    if r[4] > r[5]:
                        break
                    else:
                        r[2] = r[2] + 1
                
                # r[4] > r[5]
                r[5] = r[2] # jump back to ip=8
            else:    
                # ip=26
                if r[3] == r[0]:
                    return r # halt


def test_part1():
    with open(THIS_DIR / 'input.txt') as f:
        data = f.read()

    # PART 1
    print(execute_program(data, [13270004,0,0,0,0,0]))
    fast_execute([13270004,0,0,0,0,0])

def test_part2():
    with open(THIS_DIR / 'input.txt') as f:
        data = f.read()

    # PART 2
    r3_values = []
    def check_ip_28(ip, cpu):
        if ip == 8 or ip==9:
            print(ip, cpu.dump())
    print(execute_program(data, [13181393], cb = check_ip_28))

if __name__ == "__main__":
    test_part1()
    #test_part2()

