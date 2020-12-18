"""
Advent of Code 2020 - Day 18
Pieter Kitslaar
"""

from pathlib import Path

OP_FUNCS = {
    '+': lambda a,b:a+b,
    '*': lambda a,b:a*b,
}

example_a="1 + 2 * 3 + 4 * 5 + 6"
example_b="1 + (2 * 3) + (4 * (5 + 6))"

def tokenize(txt):
    tokens = []
    group = ''
    for token in txt.split():
        if token.endswith(')') and token.count(')') + group.count(')') == group.count('('):
            group += ' ' + token
            tokens.append(tokenize(group[1:-1]))
            group = ''
        elif token.startswith('('):
            if group:
                group += ' ' + token
            else:
                group = token
        elif group:
            group += ' ' + token
        else: 
            if token.isnumeric():
                tokens.append(int(token))
            elif token in '+*':
                tokens.append(token)
            else:
                raise RuntimeError(token)
    return tuple(tokens)

def equate(tokens):
    operator = '+'
    values = []
    for t in tokens:
        if isinstance(t, tuple):
            values.append(equate(t))
        elif str(t) in '+*':
            operator = t
        else:
            values.append(t)
        if len(values) == 2:
            values = [OP_FUNCS[operator](*values)]
    return values[0]

def solve1(txt):
    return equate(tokenize(txt))

def test_example():
    assert(71 == solve1(example_a))
    assert(51 == solve1(example_b))
    assert(26 == solve1('2 * 3 + (4 * 5)'))
    assert(437== solve1('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    assert(12240== solve1('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    assert(13632== solve1('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()    

def test_part1():
    answer = sum(solve1(l) for l in get_input().splitlines())
    print('Part 1:', answer)
    assert(21993583522852 == answer)

def create_groups(t):
    new_t = []
    for p in t:
        if isinstance(p, tuple):
            p = create_groups(p)
        new_t.append(p)
        if len(new_t) > 2 and new_t[-2] == '+':
            g = tuple(new_t[-3:])
            del new_t[-3:]
            new_t.append(g)
    return tuple(new_t)

def solve2(txt):
    return equate(create_groups(tokenize(txt)))

def test_example_part2():
    assert(231 == solve2('1 + 2 * 3 + 4 * 5 + 6'))
    assert(51 == solve2('1 + (2 * 3) + (4 * (5 + 6))'))
    assert(46  == solve2('2 * 3 + (4 * 5)'))
    assert(1445 == solve2('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    assert(669060 == solve2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    assert(23340 == solve2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))

def test_part2():
    answer = sum(solve2(l) for l in get_input().splitlines())
    print('Part 2:', answer)
    assert(122438593522757 == answer)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example_part2()
    test_part2()