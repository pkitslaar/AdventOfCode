"""
Advent of Code 2017 - Day 07
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

EXAMPLE_DATA = """\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

def parse(d):
    nodes = {}
    for line in d.strip().splitlines():
        name_weight, _, children = line.partition(' -> ')
        if name_weight:
            name = name_weight.split()[0]
            weight = int(name_weight.split()[1][1:-1])
            nodes[name] = {'weight': weight, 'children': [c.strip() for c in children.split(',') if c.strip()]}
    return nodes

def find_root(nodes):
    all_children = set()
    for n, v in nodes.items():
        all_children.update(v['children'])
    root_nodes = set(nodes) - all_children
    assert(len(root_nodes)==1)
    return list(root_nodes)[0]

def test_example():
    assert('tknk' == find_root(parse(EXAMPLE_DATA)))

def part1():
    result =  find_root(parse(data()))
    print('PART 1:', result)
    assert(result == 'vmpywg')

def cum_weight(nodes, n):
    c_weight = nodes[n]['weight']
    for c in nodes[n]['children']:
        c_weight += cum_weight(nodes, c)
    return c_weight

from collections import Counter

def balance(nodes):
    for n, v in nodes.items():
        v['cum_weight'] = cum_weight(nodes, n)
    result = {}
    find_inbalance(nodes, find_root(nodes), result)
    return [*result.items()][0]


def find_inbalance(nodes, n, result = {}):
    v = nodes[n]
    if v['children']:
        child_counts = Counter(nodes[c]['cum_weight'] for c in v['children'])
        if len(child_counts) > 1:
            expected_cum_weight = child_counts.most_common()[0][0]
            for c in v['children']:
                if not find_inbalance(nodes, c, result) and nodes[c]['cum_weight'] != expected_cum_weight:
                    diff_weight = expected_cum_weight - nodes[c]['cum_weight']
                    result[c] = nodes[c]['weight'] + diff_weight
            return True
    return False

def test_example2():
    node, result = balance(parse(EXAMPLE_DATA))
    assert('ugml' == node)
    assert(60 == result)         

def part2():
    # node is ncrxh with weight 1679 needs to be 1674
    node, result = balance(parse(data()))
    print('PART 2:', result, 'for node', node)
    assert('ncrxh' == node)
    assert(1674 == result)

if __name__ == "__main__":
    test_example()
    part1()
    test_example2()
    part2()


