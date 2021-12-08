"""
Advent of Code 2021 - Day 08
Pieter Kitslaar
"""

from pathlib import Path
    
example="""\
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""


example2="""\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

def parse(txt):
    for line in txt.splitlines():
        signals, digits = line.split("|")
        yield [set(s) for s in signals.strip().split()], [d for d in digits.strip().split()]

def solve1(txt):
    num_unique = 0
    for _, digits in parse(txt):
        num_unique += sum(1 for d in digits if len(d) in (2,3,4,7))
    return num_unique

def test_example():
    result = solve1(example2)
    assert result == 26

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    result = solve1(get_input())
    print('Part 1:', result)

SEGMENTS_TO_NUMBER = {
    'a''b''c'   'e''f''g' : '0', # 6
          'c'      'f'    : '1', # 2 <-
    'a'   'c''d''e'   'g' : '2', # 5
    'a'   'c''d'   'f''g' : '3', # 5
       'b''c''d'   'f'    : '4', # 4 <-
    'a''b'   'd'   'f''g' : '5', # 5
    'a''b'   'd''e''f''g' : '6', # 6
    'a'   'c'      'f'    : '7', # 3 <-
    'a''b''c''d''e''f''g' : '8', # 7 <-
    'a''b''c''d'   'f''g' : '9'  # 6
}
NUMBER_TO_SEGMENTS = {v:k for k,v in SEGMENTS_TO_NUMBER.items()}
import itertools
from collections import Counter

def decode_lookup(signals):
    singal_per_length = {}
    for s in signals:
        singal_per_length.setdefault(len(s), []).append(s)

    unique_singals = {}
    for number, length in [('1', 2), ('4', 4), ('7',3), ('8', 7)]:
        signal = singal_per_length[length][0]
        unique_singals[number] = signal
    
    lookup = {}
    lookup['a'] = unique_singals['7'] - unique_singals['1']
    lookup['b'] = (unique_singals['8'] & unique_singals['4'])  - (unique_singals['1'] | unique_singals['7'])
    lookup['c'] = unique_singals['1'] & unique_singals['4'] & unique_singals['7'] & unique_singals['8']
    lookup['d'] = (unique_singals['4'] & unique_singals['8']) - (unique_singals['1'] & unique_singals['7'])
    lookup['e'] = unique_singals['8'] - (unique_singals['1'] | unique_singals['4'] | unique_singals['7'])
    lookup['f'] = unique_singals['1'] & unique_singals['4'] & unique_singals['7'] & unique_singals['8']
    lookup['g'] = unique_singals['8'] - (unique_singals['1'] | unique_singals['4'] | unique_singals['7'])
    
    # from the non unique '5' segment numbers
    segment_5_count = Counter(itertools.chain(*singal_per_length[5]))
    # from the 5 segment numbers the 'b' and 'e' option only occurs ones
    lookup['b'] = lookup['b'] & {k for k,v in segment_5_count.items() if v == 1}
    lookup['e'] = lookup['e'] & {k for k,v in segment_5_count.items() if v == 1}

    # from the 6 segment numbers the 'c', 'd' and 'e' option only occur twice
    segment_6_count = Counter(itertools.chain(*singal_per_length[6]))
    lookup['c'] = lookup['c'] & {k for k,v in segment_6_count.items() if v == 2}
    lookup['d'] = lookup['d'] & {k for k,v in segment_6_count.items() if v == 2}
    lookup['e'] = lookup['e'] & {k for k,v in segment_6_count.items() if v == 2}

    # find all lookups with single solution
    solved_lookups = set()
    for n in lookup.values():
        if len(n) == 1:
            solved_lookups = solved_lookups | n
    
    # reduce the remaining solutions
    for k, n in lookup.items():
        if len(n) > 1:
            lookup[k] = lookup[k] - solved_lookups

    # reverse to lookup
    current_to_actual = {list(v)[0]:k for k,v in lookup.items()}
    return current_to_actual

def decode(signals, digits):
    lookup = decode_lookup(signals)
    number_digits = []
    for d_segments in digits:
        decoded_segments = ''.join(sorted([lookup[d] for d in d_segments]))
        number_digits.append(SEGMENTS_TO_NUMBER[decoded_segments])
    return int(''.join(number_digits))

def test_decode():
    signals, digits = list(parse(example))[0]
    result = decode(signals, digits)
    assert 5353 == result

def solve2(txt):
    total = 0
    for signals, digits in parse(txt):
        result = decode(signals, digits)
        total += result
    return total

def test_example2():
    result = solve2(example2)
    assert 61229 == result

def test_part2():
    result = solve2(get_input())
    print('Part 2:', result)
    assert 1048410 == result

if __name__ == "__main__":
    test_example()
    test_part1()
    test_decode()
    test_example2()
    test_part2()