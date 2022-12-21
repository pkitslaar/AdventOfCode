"""
Advent of Code 2022 - Day 21
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read().strip()

EXAMPLE_DATA="""\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

def parse(d):
    graph = {}
    for line in d.splitlines():
        node, inputs = line.split(': ')
        a_op_b = inputs.split()
        if len(a_op_b) == 1:
            a, op, b = a_op_b[0], None, None
            graph[node] = {'value': int(a)}
        else:
            a, op, b = a_op_b
            graph[node] = {'a': a, 'op': op, 'b': b}
    return graph

import operator

def compute(graph, node='root'):
    OPS = {
        '+': operator.add, 
        '-': operator.sub, 
        '*': operator.mul, 
        '/': operator.floordiv
    }
    this_node = graph[node]
    if 'value' in this_node:
        return this_node['value']
    else:
        a = compute(graph, this_node['a'])
        b = compute(graph, this_node['b'])
        return OPS[this_node['op']](a, b)
    
def solve(d):
    return compute(parse(d))

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(152 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(145167969204648 == result)

def solve2(d):
    graph = parse(d)

    # find all nodes that depend on 'humn'
    depend_on_humn = ['humn']
    while depend_on_humn[-1] != 'root':
        to_check = depend_on_humn[-1]
        for n in graph:
            if graph[n].get('a') == to_check:
                depend_on_humn.append(n)
            if graph[n].get('b') == to_check:
                depend_on_humn.append(n)

    # find the branch input to 'root' that does
    # not depend on 'humn'
    root_inputs = [graph['root']['a'], graph['root']['b']]
    humn_branch = depend_on_humn[-2]
    root_inputs.remove(humn_branch)
    other_branch = root_inputs[0]
    # the value of the other branch is the one to match
    other_branch_value = compute(graph, other_branch)    

    # walk up the humn dependency tree
    # and find the required value it should compute
    depend_on_humn = depend_on_humn[:-1]
    required_value = other_branch_value
    while depend_on_humn:
        this_depend = depend_on_humn.pop()
        if this_depend == 'humn':
            break
        n = graph[this_depend]
        n_a, op, n_b = n['a'], n['op'], n['b']
        if n_a in depend_on_humn:
            b = compute(graph, n_b)
            if op == '+':
                # a + b = required ->  a = required - b
                a = required_value - b
            elif op =='-':
                # a - b = required -> a = required + b
                a = required_value + b
            elif op == '*':
                # a * b = required -> a = required / b
                a = required_value // b
            elif op == '/':
                # a / b = required -> a = required * b
                a = required_value * b
            required_value = a
        if n_b in depend_on_humn:
            a = compute(graph, n_a)
            if op == '+':
                # a + b = required -> b = required - a
                b = required_value - a
            elif op == '-':
                # a - b = required -> b = a - required
                b = a - required_value
            elif op == '*':
                # a * b = required -> b = required / a
                b = required_value // a
            elif op == '/':
                # a / b = required -> b = a / required
                b = a // required_value
            required_value = b
    return required_value
            
def test_example2():
    result = solve2(EXAMPLE_DATA)
    assert(301 == result)

def test_part2():
    result = solve2(data())
    print('PART 2:', result)
    assert(3330805295850 == result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()