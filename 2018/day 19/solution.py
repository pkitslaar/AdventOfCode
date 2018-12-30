# Advent of code - 2018
#
# Day 19
#
# Pieter Kitslaar
#

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


def execute_program(txt_data, initial_data = [0]*6):
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
    while True:
        if ip >= len(instructions):
            break
        op_name, call_args = instructions[ip]
        cpu.set_r(ip_adress, ip)
        before = cpu.dump()
        cpu.call(op_name, *call_args)
        after = cpu.dump()
        #print(f"ip={ip} {before} {op_name} {call_args} {after}")
        ip = cpu.get_r(ip_adress) + 1
    return cpu.dump()

with open('input.txt') as f:
    data = f.read()

# PART 1
registers = execute_program(data)
print('PART 1:', registers[0], registers)


# PART 2
registers = execute_program(data, [1])
print('PART 2:', registers[0], registers)




