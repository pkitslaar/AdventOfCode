"""
Advent of Code 2023 - Day 08
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

EXAMPLE_DATA2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

def parse(data):
    turns = None
    nodes = {}
    for line in data.splitlines():
        if not line.strip():
            continue
        if not turns:
            turns = line.strip()
            continue
        node, children = line.split("=")
        left, right = children.strip()[1:-1].split(",")
        nodes[node.strip()] = {'L': left.strip(), 'R': right.strip()}
    return turns, nodes

def solve(data):
    turns, nodes = parse(data)    
    current = 'AAA'
    steps = 0
    while current != 'ZZZ':
        turn = turns[steps % len(turns)]
        current = nodes[current][turn]
        steps += 1

    result = steps
    return result



def test_example1a():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 2

def test_example1b():
    result = solve(EXAMPLE_DATA2)
    print(f"example: {result}")
    assert result == 6

def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 18113

EXAMPLE_DATA_PART2 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

import math

def solve2(data):
    turns, nodes = parse(data) 
    start_nodes = [n for n in nodes.keys() if n.endswith('A')]  
    node_steps = {n: 0 for n in start_nodes}
    for n in start_nodes:
        steps = 0
        current = n
        while current[-1] != 'Z':
            turn = turns[steps % len(turns)]
            current = nodes[current][turn]
            steps += 1
        node_steps[n] = steps

    # find the least common multiple of the steps for each node
    result = math.lcm(*node_steps.values())
    return result

def test_example2():
    result = solve2(EXAMPLE_DATA_PART2)
    print(f"example 2: {result}")
    assert result == 6


def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result == 12315788159977


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()