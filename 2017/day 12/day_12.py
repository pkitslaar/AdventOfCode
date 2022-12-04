"""
Advent of Code 2017 - Day 12
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

import networkx as nx

EXAMPLE_DATA="""\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
"""

def parse(d):
    g = nx.Graph()
    for line in d.strip().splitlines():
        f_node, _, to_nodes = line.partition(' <-> ')
        for to_node in to_nodes.split(','):
            g.add_edge(f_node.strip(), to_node.strip())
    return g

def solution(d):
    g = parse(d)
    groups = list(nx.connected_components(g))
    num_zero = -1
    for c in groups:
        if '0' in c:
            num_zero = len(c)
    return num_zero, len(groups)

def test_example():
    assert((6,2) == solution(EXAMPLE_DATA))

def test_solution():
    result, result2 = solution(data())
    print('PART 1:', result)
    assert(239 == result)
    print('PART 2:', result2)
    assert(215 == result2)


if __name__ == "__main__":
    test_example()
    test_solution()

