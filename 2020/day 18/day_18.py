"""
Advent of Code 2020 - Day 18
Pieter Kitslaar
"""

import re
from pathlib import Path

NUMBER  = re.compile(r'^ *\({0,1}(\d+)\){0,1}')
OPERATOR = re.compile(r'^ *([+*])')
GROUP = re.compile(r'^ *(\(.+\))')
ADD_GROUP = re.compile('^ *([^+]+ \* .+$)')

OP_FUNCS = {
    '+': lambda a,b:a+b,
    '*': lambda a,b:a*b,
}

example_a="1 + 2 * 3 + 4 * 5 + 6"
example_b="1 + (2 * 3) + (4 * (5 + 6))"

def parse_bracket_group(txt):
    if m:=GROUP.match(txt):
        g_start = m.start(1)+1

        # UGLY hack to find first enclosed group
        num_open = 1
        for g_end in range(g_start,len(txt)):
            c = txt[g_end]
            if c == '(':
                num_open += 1
            if c == ')':
                num_open -= 1
            if num_open == 0:
                break
        sub_expression = txt[g_start:g_end]
        next_offset = g_end+2
        return sub_expression, next_offset
    return None

def tokenize(txt, total_value=0, current_op='+', sub_level=0, group_parser = parse_bracket_group, verbose=False):
    if not txt:
        return total_value
    next_offset = 0
    if sub_info:=group_parser(txt):
        sub_expression, next_offset = sub_info
        this_value = tokenize(sub_expression, sub_level=sub_level+1, group_parser=group_parser, verbose=verbose)
        if verbose:
            print(' '*sub_level, sub_info, this_value)
        total_value = OP_FUNCS[current_op](total_value, this_value)
    elif m:=NUMBER.match(txt):
        this_value = int(m.group(1))
        if verbose:
            print(' '*sub_level, m, this_value)
        total_value = OP_FUNCS[current_op](total_value, this_value)
        next_offset = m.end(1)
    elif m:=OPERATOR.match(txt):
        current_op = m.group(1)
        if verbose:
            print(' '*sub_level, m, current_op)
        next_offset = m.end(1)
    else:
        raise RuntimeError("No match for", txt)
    return tokenize(txt[next_offset:],total_value, current_op, sub_level=sub_level, group_parser=group_parser, verbose=verbose)

def test_example():
    assert(71 == tokenize(example_a))
    assert(51 == tokenize(example_b))
    assert(26 == tokenize('2 * 3 + (4 * 5)'))
    assert(437== tokenize('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    assert(12240== tokenize('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    assert(13632== tokenize('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()    

def test_part1():
    answer = sum(tokenize(l) for l in get_input().splitlines())
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

def tokenize2(txt_raw):
    txt = '('+re.sub(r'(\+|\*)',r',"\1",', txt_raw)+')'
    t = eval(txt)
    g = create_groups(t)
    new_txt  = str(g).replace("'","").replace(",","")
    return eval(new_txt)

def test_example_part2():
    assert(231 == tokenize2('1 + 2 * 3 + 4 * 5 + 6'))
    assert(51 == tokenize2('1 + (2 * 3) + (4 * (5 + 6))'))
    assert(46  == tokenize2('2 * 3 + (4 * 5)'))
    assert(1445 == tokenize2('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    assert(669060 == tokenize2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    assert(23340 == tokenize2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))

def test_part2():
    answer = sum(tokenize2(l) for l in get_input().splitlines())
    print('Part 2:', answer)
    assert(122438593522757 == answer)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example_part2()
    test_part2()