# Advent of code - 2018
#
# Day 16
#
# Pieter Kitslaar
#

from collections import defaultdict

class CPU(object):

    def __init__(self):
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
        highest_register = max(self.registers)
        return [self.registers[i] for i in range(highest_register+1)]



def parse_sample(txt):
    before = []
    code = []
    after = []
    for l in txt.splitlines():
        if l.startswith('Before:'):
            before = eval(l.split(':')[-1])
        elif l.startswith('After:'):
            after = eval(l.split(':')[-1])
        else:
            code = [int(c) for c in l.strip().split()]
    return {'before': before, 'code': code, 'after': after}

def test_sample(sample):
    cpu = CPU()       
    matches = []
    for f, name in cpu.all_instructions:
        cpu.setup(sample['before'])
        code = sample['code']
        op_code, call_args = code[0], code[1:]
        f(*call_args)
        result = cpu.dump()
        if result == sample['after']:
            matches.append((op_code, name))
    return matches

def read():
    with open('input.txt') as f:
        num_empty = 0
        part1 = True
        
        samples = []
        sub_lines = []
        for l in f:
            if not l.strip():
                num_empty += 1
                if sub_lines and part1:
                    samples.append(parse_sample("\n".join(sub_lines)))
                    sub_lines = []
                if num_empty > 2:
                    part1 = False
            else:
                num_empty = 0
                sub_lines.append(l.strip())

        test_codes = []
        for l in sub_lines:
            test_codes.append([int(c) for c in l.strip().split()])
        return samples, test_codes

example = """\
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
"""

sample = parse_sample(example)
assert(3 == len(test_sample(sample)))

print('Starting part 1')
all_samples, test_codes = read()

total_matches = []
matching_samples = []
for sample in all_samples:
    matches = test_sample(sample)
    total_matches.extend(matches)
    if len(matches) > 2:
        matching_samples.append(sample)
print('PART 1: Num samples', len(matching_samples))

# compute matches
op_code_matches = defaultdict(set)
for op_code, f_match in total_matches:
    op_code_matches[op_code].add(f_match)

certain_matches = {}
while op_code_matches:
    c = [(len(m), op_code, m) for op_code, m in op_code_matches.items()]
    c.sort()
    num_matches, op_code, method_names = c[0]
    assert(num_matches == 1)
    method_name = list(method_names)[0]
    certain_matches[op_code] = method_name
    del op_code_matches[op_code]
    for v in op_code_matches.values():
        v.discard(method_name)

print(certain_matches)

cpu = CPU()       
for code in test_codes:
    op_code, call_args = code[0], code[1:]
    f_name = certain_matches[op_code]
    cpu.call(f_name, *call_args)
print(cpu.dump())





