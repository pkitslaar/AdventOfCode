"""
Advent of Code 2017 - Day 08
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

EXAMPLE_DATA="""\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""

import operator

OP_CODES = {
    '>': operator.gt,
    '<': operator.lt,
    '==': operator.eq,
    '>=': operator.ge,
    '<=': operator.le,
    '!=': operator.ne
}

from collections import defaultdict

def solve(d):
    registers=defaultdict(int)
    instructions = []
    all_time_max = 0
    for line in d.strip().splitlines():
        reg, op, value, *cond = line.split()
        # check condition
        cond_reg_value = registers[cond[1]]
        cond_op = OP_CODES[cond[2]]
        cond_value = int(cond[3])
        if cond_op(cond_reg_value, cond_value):
            if op == 'inc':
                registers[reg] += int(value)
            elif op == 'dec':
                registers[reg] -= int(value)
            else:
                raise ValueError(f'Unknown op: {op}')
        all_time_max = max([all_time_max, max(registers.values())])
    return max(registers.values()), all_time_max

assert((1,10) == solve(EXAMPLE_DATA))

def solution():
    result, all_time = solve(data())
    print('PART 1:', result)
    print('PART 2:', all_time)

if __name__ == "__main__":
    solution()