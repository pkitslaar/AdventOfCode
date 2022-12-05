"""
Advent of Code 2022 - Day 05
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

EXAMPLE_DATA="""\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

from collections import namedtuple

Move = namedtuple('Move', "amount from_stack to_stack")

def parse(d):
    stacks = {}
    moves = []
    for line in d.splitlines():
        if line.startswith('move'):
            amount, from_stack, to_stack = map(int,line.split()[1::2])
            moves.append(Move(amount, from_stack, to_stack))
        elif not moves:
            for stack_number, stack_value_index in enumerate(range(1,len(line), 4)):
                stack_value = line[stack_value_index].strip()
                if stack_value and not stack_value.isdigit():
                    stacks.setdefault(stack_number+1, []).append(stack_value)
    for s in stacks.values():
        s.reverse()
    return stacks, moves

def test_parse():
    parse(EXAMPLE_DATA)

def solve(d, part2=False):
    stacks, moves = parse(d)
    for m in moves:
        f_stack = stacks[m.from_stack]
        t_stack = stacks[m.to_stack]
        if part2:
            crates = [f_stack.pop() for _ in range(m.amount)]
            t_stack.extend(reversed(crates))
        else:
            for _ in range(m.amount):
                t_stack.append(f_stack.pop())
    return ''.join([v[-1] for _,v in sorted(stacks.items())])

def test_example():
    result = solve(EXAMPLE_DATA)
    assert('CMZ'==result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert('JDTMRWCQJ' == result)

def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    assert('MCD' == result)

def test_part2():
    result = solve(data(), part2=True)
    print('PART 2:', result)
    assert('VHJDDCWRD' == result)


if __name__ == "__main__":
    test_parse()
    test_example()
    test_part1()
    test_example2()
    test_part2()