"""
Advent of Code 2020 - Day 14
Pieter Kitslaar
"""

import re
from pathlib import Path

example = """\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

MASK_RE = re.compile('^mask = ([X01]{36})')
MEM_RE = re.compile('^mem\[(\d+)\] = (\d+)')

def parse(txt):
    nonzero_memory = {}
    current_mask = 'X'*36
    for line in txt.splitlines():
        if mask:= MASK_RE.match(line):
            current_mask = mask.groups()[0]
        elif mem:= MEM_RE.match(line):
            address, value = list(map(int, mem.groups()))
            value_bits = f'{bin(value)[2:]:0>36}'
            new_value_bits = []
            for b,m in zip(value_bits,current_mask):
                new_value_bits.append(b if m =='X' else m)
            new_value = int(''.join(new_value_bits),2)
            if new_value > 0:
                nonzero_memory[address] = new_value
            else:
                del nonzero_memory[address]
        else:
            raise ValueError("Could not parse line", line)
    return nonzero_memory
        

def test_example():
    memory = parse(example)
    answer = sum(memory.values())
    assert(165 == answer)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    memory = parse(get_input())
    answer = sum(memory.values())
    print('Part 1:', answer)
    assert(11501064782628 == answer)

def expand_masks(mask_txt):
    x_indices = [i for i,c in enumerate(mask_txt) if c == 'X']
    options = [{}]
    for xindex in x_indices:
        new_options = []
        for opt in options:
            opt[xindex] = '0'
            new_opt = opt.copy()
            new_opt[xindex] = '1'
            new_options.append(new_opt)
        options.extend(new_options)
    for opt in options:
        new_mask = list(mask_txt)
        for i,v in opt.items():
            new_mask[i] = v
        yield ''.join(new_mask)

def test_expand_masks():
    assert(['0010','1010','0011','1011'] == list(expand_masks('X01X')))


def parse2(txt):
    nonzero_memory = {}
    current_mask = 'X'*36
    for line in txt.splitlines():
        if mask:= MASK_RE.match(line):
            current_mask = mask.groups()[0]
        elif mem:= MEM_RE.match(line):
            address, value = list(map(int, mem.groups()))
            address_bits = f'{bin(address)[2:]:0>36}'
            new_address_bits = []
            for b,m in zip(address_bits,current_mask):
                new_address_bits.append(b if m =='0' else m)
            for expanded_address_bits in expand_masks(''.join(new_address_bits)):
                expanded_address = int(''.join(expanded_address_bits),2)
                if value > 0:
                    nonzero_memory[expanded_address] = value
                else:
                    del nonzero_memory[expanded_address]
        else:
            raise ValueError("Could not parse line", line)
    return nonzero_memory

example2="""\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

def test_example2():
    memory = parse2(example2)
    assert(208 == sum(memory.values()))

def test_part2():
    memory = parse2(get_input())
    answer = sum(memory.values())
    print('Part 2:', answer)
    assert(5142195937660 == answer)



if __name__ == "__main__":
    test_example()
    test_part1()
    test_expand_masks()
    test_example2()
    test_part2()
