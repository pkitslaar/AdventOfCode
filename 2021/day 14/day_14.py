"""
Advent of Code 2021 - Day 14
Pieter Kitslaar
"""

from pathlib import Path

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

from itertools import tee
from collections import Counter

example="""\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

def parse(txt):
    start = ""
    rules = {}
    for line in txt.splitlines():
        if not start:
            start = line.strip()
        else:
            if line.strip():
                rule_pair, new_c = map(str.strip,line.split('->'))
                rules[tuple(rule_pair)] = new_c
    return start, rules

def perform_steps(start, rules, N):
    current = start

    counts = Counter(current)
    A, B = tee(iter(current));next(B)
    pairs = Counter(zip(A,B))
    new_pairs = pairs.copy()
    for i in range(N):
        for p, pair_count in pairs.items():
            if pair_count>0:
                new_c = rules.get(p,'')
                counts[new_c] += pair_count
                new_pairs[p] -= pair_count
                new_pairs[(p[0],new_c)] += pair_count
                new_pairs[(new_c,p[1])] += pair_count
        pairs = +new_pairs
    return counts

def solve(txt, N=10):
    start, rules = parse(txt)
    counts= perform_steps(start, rules, N)
    common = counts.most_common()
    result = common[0][1]-common[-1][1]
    return result

def test_example():
    start, rules = parse(example)
    counts= perform_steps(start, rules, 1)
    assert counts == Counter('NCNBCHB')    
    counts= perform_steps(start, rules, 2)
    assert counts == Counter('NBCCNBBBCBHCB')
    counts= perform_steps(start, rules, 3)
    assert counts == Counter('NBBBCNCCNBBNBNBBCHBHHBCHB')
    counts= perform_steps(start, rules, 4)
    expected = Counter('NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB')
    print(expected)
    assert counts == expected

def test_part1():
    result = solve(get_input())
    print('Part 1', result)
    assert 2587 == result

def test_example2():
    result = solve(example, 40)
    assert 2188189693529 == result

def test_part2():
    result = solve(get_input(), 40)
    print('Part 2:', result)
    assert 3318837563123 == result
 
if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()