"""
Advent of Code 2017 - Day 14
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

import sys
sys.path.insert(0, str(THIS_DIR.parent / "day 10"))
print(sys.path[0])
from day_10 import dense_hash

def parse(d):
    rows = []
    for i in range(128):
        row = []
        knot_hash = dense_hash(f"{d}-{i}")
        for c in knot_hash:
            bits = f'{int(c,16):04b}'
            row.append(bits)
        rows.append(''.join(row))
        assert(len(rows[-1])==128)
    return rows

def solve(d):
    rows = parse(d)
    return sum([r.count('1') for r in rows])

def test_example():
    result = solve('flqrgnkx')
    assert(8108 == result)

def test_part1():
    result = solve('hwlqcszp')
    print('PART 1:', result)

import networkx as nx
def solve2(d):
    rows = parse(d)
    g = nx.Graph()

    for y in range(128):
        for x in range(128):
            if rows[y][x] != '0':
                g.add_node((y,x))
                for N in [(-1,0),(0,-1),(1,0),(0,1)]:
                    n_pos_y = y+N[0]
                    n_pos_x = x+N[1]
                    if n_pos_y >= 0 and n_pos_x >= 0 and n_pos_y < 128 and n_pos_x < 128:
                        n_value = rows[n_pos_y][n_pos_x] 
                        if n_value != '0':
                            g.add_edge((y,x),(n_pos_y,n_pos_x))
    g = g.to_undirected()
    return len([*nx.connected_components(g)])
  
def test_example2():
    result = solve2('flqrgnkx')
    assert(1242 == result)

def test_part2():
    result = solve2('hwlqcszp')
    print('PART 2:', result)
    assert(1018 == result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()