"""
Advent of Code 2021 - Day 12
Pieter Kitslaar
"""

from pathlib import Path

from collections import Counter
import networkx as nx

example = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

example2 = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""


example3 = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

def parse(txt):
    g = nx.Graph()
    for line in txt.splitlines():
        u, v = line.split('-')
        g.add_edge(u,v)
    return g

def find_paths(g, source='start', target='end', part2=False):
    search_paths = [[source]]
    while search_paths:
        new_paths = []
        for p in search_paths:
            for n in g.neighbors(p[-1]):
                if n == target:
                    yield p + [n]
                else:
                    if n == source:
                        pass
                    elif n.isupper():
                        new_paths.append(p+[n])
                    else:
                        small_counter = Counter(c for c in p if c.islower())
                        if n not in small_counter:
                            new_paths.append(p+[n])
                        elif part2 and max(small_counter.values()) < 2:
                            new_paths.append(p+[n])
        search_paths = new_paths

def solve1(txt):
    return sum(1 for p in find_paths(parse(txt)))

def test_example():
    assert 10 == solve1(example)
    assert 19 == solve1(example2)
    assert 226 == solve1(example3)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    result = solve1(get_input())
    print('Part 1', result)
    assert 3510 == result

def solve2(txt):
    return sum(1 for p in find_paths(parse(txt), part2=True))

def test_example2():
    assert 36 == solve2(example)
    assert 103 == solve2(example2)
    assert 3509 == solve2(example3)

def test_part2():
    result = solve2(get_input())
    print('Part 2', result)
    assert 122880 == result

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()