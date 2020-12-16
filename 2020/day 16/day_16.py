
"""
Advent of Code 2020 - Day 16
Pieter Kitslaar
"""

from pathlib import Path
from functools import reduce

example="""\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

def parse(txt):
    rules = {}
    your_ticket = None
    nearby_tickets = []
    state = 'rules'
    for line in txt.splitlines():
        if not line:
            continue
        if 'ticket' in line:
            state = line[:-1]
            continue
        if state == 'rules':
            rule_name, ranges = line.split(':')
            valid_numbers = set()
            for s_e_txt in ranges.split(' or '):
                s, e = map(int, s_e_txt.split('-'))
                valid_numbers.update(range(s,e+1))
            rules[rule_name] = valid_numbers
        elif state == 'your ticket':
            your_ticket = list(map(int, line.split(',')))
        elif state == 'nearby tickets':
            nearby_tickets.append(list(map(int, line.split(','))))
        else:
            raise RuntimeError('Unknown state', state, line)
    return rules, your_ticket, nearby_tickets

def error_rate(rules, tickets):
    all_valid_numbers = set()
    for valid in rules.values():
        all_valid_numbers.update(valid)
    valid_tickets = []
    invalid_numbers = []
    for t in tickets:
        invalid = set(t) - all_valid_numbers
        if invalid:
            invalid_numbers.extend(invalid)
        else:
            valid_tickets.append(t)
    return sum(invalid_numbers), valid_tickets

def test_example():
    rules, y, n = parse(example)
    assert(71 == error_rate(rules, n)[0])

example_2="""\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

def field_order(rules, tickets):
    num_fields = len(tickets[0])

    # combine all values from all tickets per field
    field_values = [set() for _ in range(num_fields)]
    for t in tickets:
        for i, v in enumerate(t):
            field_values[i].add(v)

    # check for each field what rules could possibly apply
    field_possibilities = [set() for _ in range(num_fields)]
    for fi, fv in enumerate(field_values):
        for r,v in rules.items():
            invalid = fv - v
            if invalid:
                continue
            else:
                field_possibilities[fi].add(r)

    # keep looping over de possibilities and deduce the
    # final order by iteratively remove rules that
    # are only possible for a single field from fields
    # that have multiple options

    # keep looping while there are fields with more than 1 option
    while any(len(p)>1 for p in field_possibilities):
        # collect all options that are just listed once
        single_p = {list(p)[0] for p in field_possibilities if len(p) == 1}

        # define new options list by removing the single_p
        # values from multi valued options
        new_fp = []
        for p in field_possibilities:
            if len(p) == 1:
                new_fp.append(p)
            else:
                new_fp.append(p - single_p)
        field_possibilities = new_fp
    # return simple list of field order
    return [list(fp)[0] for fp in field_possibilities]

def test_example2():
    r,y,n = parse(example_2)
    assert(['row','class','seat'] == field_order(r,n + [y]))


def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_puzzle():
    r,y,n=parse(get_input())
    rate, valid_tickets = error_rate(r,n)
    print('Part 1:', rate)
    assert(21081 == rate)

    order = field_order(r, valid_tickets + [y])
    depart_numbers = [n for f,n in zip(order,y) if f.startswith('departure')]
    answer = reduce(lambda a,b:a*b, depart_numbers)
    print('Part 2:', answer)
    assert(314360510573 == answer)

if __name__ == "__main__":
    test_example()
    test_example2()
    test_puzzle()
        