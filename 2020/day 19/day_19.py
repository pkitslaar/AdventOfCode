"""
Advent of Code 2020 - Day 19
Pieter Kitslaar
"""

from pathlib import Path
import re
import itertools

example_rules_a='''\
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
'''

example_rules_b='''\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
'''

def parse_rules(txt):
    #print(txt)
    rule_dict = {}
    for line in txt.splitlines():
        n,r = [s.strip() for s in line.split(':',1)]
        if '"' in r:
            r = r[1:-1]
        elif '|' in r:
            r = [tuple(map(int,p.split())) for p in r.split('|')]
        else:
            r = tuple(map(int,r.split()))
        rule_dict[int(n)]=r
    return rule_dict

def expand_rules(rule_dict, create_regexp=True):
    #print(rule_dict)
    s_g = '('
    e_g = ')'
    # expand rules
    found_subst = True
    while found_subst:
        #print('>',rule_dict)
        found_subst = False
        new_rules = {}
        for k, v in rule_dict.items():
            if isinstance(v, str):
                new_rules[k]= v
            elif isinstance(v, tuple):
                try:
                    new_rules[k]=''.join(rule_dict[i] for i in v)
                    found_subst = True
                except TypeError as e:
                    new_rules[k]=v
                    #print('TUPLE', k,v, e)
            elif isinstance(v, list):
                try:
                    new_rules[k] = s_g+'|'.join(['%s%s%s' % (s_g, ''.join(rule_dict[i] for i in t), e_g) for t in v])+e_g
                    found_subst = True
                except TypeError as e:
                    new_rules[k]=v
                    #print('LIST', k, v, e)
            elif isinstance(v, set):
                pass
            else:
                raise RuntimeError('Unkown type', v)
        rule_dict = new_rules
    if create_regexp:
        return {k:re.compile('^'+r+'$') for k,r in rule_dict.items()}
    return rule_dict
    
def test_example_rules():
    r_a = expand_rules(parse_rules(example_rules_a))
    assert(r_a[0].match('aab'))
    assert(r_a[0].match('aba'))
    assert(not r_a[0].match('abb'))
    
    r_b = expand_rules(parse_rules(example_rules_b))
    for test in 'aaaabb,aaabab,abbabb,abbbab,aabaab,aabbbb,abaaab,ababbb'.split(','):
        assert(r_b[0].match(test))
        assert(not r_b[0].match(test+'a'))

example_full="""\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

def parse_full(txt):
    rules_txt = []
    patterns_txt = []
    current = rules_txt
    for line in txt.splitlines():
        if not line.strip():
            current = patterns_txt
        else:
            current.append(line)
    rules = parse_rules('\n'.join(rules_txt))
    return rules, patterns_txt

def solve1(txt):
    initial_rules, patterns_txt = parse_full(txt)
    rules = expand_rules(initial_rules)
    answer = [p for p in patterns_txt if rules[0].match(p)]
    return answer

def test_example_full():
    assert(2 == len(solve1(example_full)))

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()    

def test_part1():
    answer = len(solve1(get_input()))
    print('Part 1:', answer)

example_full_2="""\
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""


def expand_rules2(rule_dict):
    found_subst = True
    while found_subst:
        #print('>',rule_dict)
        found_subst = False
        new_rules = {}
        for k, v in rule_dict.items():
            if isinstance(v, set):
                new_rules[k] = v
            elif isinstance(v, str):
                new_rules[k] = set([v])
                found_subst = True
            elif isinstance(v, tuple) and all(isinstance(rule_dict[t], set) for t in v):
                #print('**', k, v, [rule_dict[t] for t in v])
                new_v = set()
                for c in itertools.product(*[rule_dict[t] for t in v]):
                    #print('combo:', c)
                    new_v.add(''.join(c))
                new_rules[k] = new_v
                #print(new_v)
                found_subst = True
            elif isinstance(v, list):
                new_v = []
                for t in v:
                    if isinstance(t, tuple) and all(isinstance(rule_dict[p], set) for p in t):
                        new_t = set()
                        for c in itertools.product(*[rule_dict[p] for p in t]):
                            #print('list combo:', c)
                            new_t.add(''.join(c))
                        new_v.append(new_t)
                        found_subst = True
                    else:
                        new_v.append(t)
                if all(isinstance(t, set) for t in new_v):
                    new_v_set = set()
                    for t in new_v:
                        new_v_set.update(t)
                    new_v = new_v_set
                    found_subst = True
                new_rules[k] = new_v
            else:
                new_rules[k]=v
        rule_dict = new_rules
    return rule_dict

def solve2(txt):
    initial_rules, patterns_txt = parse_full(txt)
    rules = expand_rules2(initial_rules)#, create_regexp=False)
    N = list(set([len(r) for r in rules[31]] + [len(r) for r in rules[42]]))[0]

    max_pattern_length = max(len(p) for p in patterns_txt)
    max_repeat = 1+ max_pattern_length // (N*2)
    
    rule_31 = "|".join(rules[31])
    rule_42 = "|".join(rules[42])
    
    """
    0: 8 11 -> 0: 42+ 42{i}31{i}
    8: 42 | 42 8 -> 8: 42+ e.g repeat 42 1-to-N
    11: 42 31 | 42 11 31 -> 11: 42{i}31{i} for i=1...N
      > 42 31
      > 42 42 31 31
      > 42 42 42 31 31 31
    """
    p31_end = re.compile(r'(%s)+$' % rule_31)
    p42_repeat = re.compile(r'^(%s)+$' % rule_42)
    regexps = [re.compile(r'^(%s){%s,}(%s){%s}$' % (rule_42, i+1, rule_31, i)) for i in range(1,max_repeat)]

    all_matches = []
    for pattern in patterns_txt:
        for regex in regexps:
            if m:=regex.match(pattern):
                all_matches.append(pattern)
                break
    return all_matches

def test_example_part2():
    answer = len(solve2(example_full_2))
    assert(12 == answer)
    
def test_part2():
    answer = len(solve2(get_input()))
    print('Part 2:', answer)
    assert(296 == answer)

if __name__ == "__main__":
    test_example_rules()
    test_example_full()
    test_part1()
    test_example_part2()
    test_part2()
