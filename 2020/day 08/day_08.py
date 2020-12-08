"""
Advent of Code 2020 - Day 08
Pieter Kitslaar
"""

import sys
from pathlib import Path

# Import the shared CPU class
# we will probably need to reuse this in the next puzzles...
sys.path.insert(0,str(Path(__file__).absolute().parents[1] / 'shared'))
from cpu import CPU

example="""\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

def detect_loop(program_txt):
    cpu = CPU(program_txt)
    history= []
    found_loop = False
    try:
        while not found_loop:
            this_state = cpu.step()
            if history:
                for his in history:
                    if this_state['pc'] == his['pc']:
                        found_loop = True
                        break
            if not found_loop:
                history.append(this_state)
    except IndexError:
        # the cpu will raise an IndexError when the
        # program halts
        pass

    return found_loop, history

def test_example():
    _, history = detect_loop(example)
    assert(5 == history[-1]['a'])

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    _, history = detect_loop(get_input())
    answer = history[-1]['a']
    print('Part 1:', answer)
    assert(1489 == answer)

def fix_program(program_txt):
    original_instructions = program_txt.splitlines()
    num_instructions = len(original_instructions)
    for i in range(num_instructions):
        if original_instructions[i].startswith(('jmp', 'nop')):
            new_instructions = original_instructions[:] # make copy
            new_instructions[i] = "{0}{1}".format(
                    {'jmp':'nop', 'nop':'jmp'}[new_instructions[i][:3]],
                    new_instructions[i][3:]
            )
            # check for loop
            found_loop, history = detect_loop("\n".join(new_instructions))
            if not found_loop:
                return history

def test_example_part2():
    history = fix_program(example)
    assert(8 == history[-1]['a'])

def test_part2():
    history = fix_program(get_input())
    answer = history[-1]['a']
    print('Part 2:', answer)
    assert(1539 == answer)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example_part2()
    test_part2()