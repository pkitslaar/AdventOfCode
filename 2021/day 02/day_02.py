"""
Advent of Code 2021 - Day 02
Pieter Kitslaar
"""

from pathlib import Path

example = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2"""

INSTRUCTION = {
    'forward': (1,0),
    'down': (0,1),
    'up': (0,-1)
}

def parse_data(txt):
    for line in txt.splitlines():
        instruction_txt, value_txt = line.split()
        value = int(value_txt)
        instruction = INSTRUCTION[instruction_txt]
        yield instruction, value

def compute_route(instruction_values, start = (0,0)):
    result = list(start)
    for instruction, value in instruction_values:
        result[0] += instruction[0]*value
        result[1] += instruction[1]*value
    return result

def test_example():
    result = compute_route(parse_data(example))
    assert [15,10] == result
    assert 150 == result[0]*result[1]


def get_input():
    input_numbers = []
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    result = compute_route(parse_data(get_input()))
    print('Part 1:', result[0]*result[1])

def compute_route2(instruction_values, start = (0,0)):
    result = list(start)
    aim = 0
    for instruction, value in instruction_values:
        aim += instruction[1]*value
        result[0] += instruction[0]*value
        result[1] += instruction[0]*aim*value
    return result

def test_example2():
    result = compute_route2(parse_data(example))
    assert [15,60] == result
    assert 900 == result[0]*result[1]

def test_part2():
    result = compute_route2(parse_data(get_input()))
    print('Part 2:', result[0]*result[1])

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()