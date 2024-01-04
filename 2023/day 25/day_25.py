"""
Advent of Code 2023 - Day 25
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

import networkx as nx
from itertools import combinations
from functools import reduce

def solve(data, part2=False):
    graph = nx.Graph()
    for line in data.splitlines():
        node, connections = line.split(": ")
        for conn in connections.split():
            graph.add_edge(node.strip(), conn.strip(), capacity=1)

    for s, t in combinations(graph.nodes(), 2):
        cut_value, partition = nx.minimum_cut(graph, s, t)
        if cut_value == 3 and len(partition) == 2:
            result = reduce(lambda a, b: a * b, map(len, partition))
            break
    
   
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 54


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 600369


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == -1


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == -1


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()