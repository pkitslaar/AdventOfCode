"""
Advent of Code 2024 - Day 23
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

import networkx as nx

def parse(data):
    G = nx.Graph()
    for line in data.strip().splitlines():
        a, b = line.split('-')
        G.add_edge(a, b)
    return G


def solve(data, part2=False):
    result = 0
    g : nx.Graph = parse(data)
    # find subgraphs
    lan_groups = set()
    for c in g.nodes:
        C_N = set(g.neighbors(c))
        for n in C_N:
            N_N = set(g.neighbors(n))
            common_N = C_N.intersection(N_N)
            if part2:
                lan_groups.add(frozenset([c,n, *common_N]))
            else:
                for cn in common_N:
                    lan_groups.add(frozenset([c,n,cn]))
    if part2:
        # prune the groups
        connected_lan_groups = set()
        for lg in lan_groups:
            is_connected = True
            for c in lg:
                N = set(g.neighbors(c))
                diff = lg - N
                if diff != {c}:
                    is_connected = False
                    break
            else:
                # no break
                if is_connected:
                    connected_lan_groups.add(lg)

    if part2:
        largest_group = max(connected_lan_groups, key=len)
        return ",".join(sorted(largest_group))
        
    return sum(1 for lg in lan_groups if any(n.startswith('t') for n in lg))


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 7


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 1306


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == "co,de,ka,ta"


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == "bd,dk,ir,ko,lk,nn,ob,pt,te,tl,uh,wj,yl"


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()