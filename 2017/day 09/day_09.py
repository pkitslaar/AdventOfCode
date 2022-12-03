"""
Advent of Code 2017 - Day 09
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

def parse_garbage(d):
    assert(d[0]=='<')
    skip_next = False
    num_garbage_chars = 0
    for i, current_c in enumerate(d[1:]):
        if not skip_next:
            if current_c == '>':
                break
            elif current_c == '!':
                skip_next = True
            else:
                num_garbage_chars += 1
        else:
            skip_next = False
        
    return i+1, num_garbage_chars

def test_parse_garbage():
    assert((1,0)==parse_garbage('<>'))
    assert((20,13)==parse_garbage('<!>},{<!>},{<!>},{<a>'))
    assert((3,0)==parse_garbage('<!!>'))

def strip_garbage(d):
    found_garbage = True
    total_num_garbage = 0
    while found_garbage:
        found_garbage = False
        for i,c in enumerate(d):
            if c=='<':
                end_garbage, num_garbage = parse_garbage(d[i:])
                total_num_garbage += num_garbage
                d = d[:i] + d[i+end_garbage+1:]
                found_garbage = True
                break
    return d, total_num_garbage


def test_strip_garbage():
    assert(('',0)==strip_garbage('<>'))
    assert(('{}',0)==strip_garbage('{}'))
    assert(('{,,{}}',0)==strip_garbage('{<>,<>,{}}'))
    assert(('{{}}',13)==strip_garbage('{{<!>},{<!>},{<!>},{<a>}}'))
    assert(('{{},{},{},{}}',0)==strip_garbage('{{<!!>},{<!!>},{<!!>},{<!!>}}'))
   


def parse_group(d):
    d, _ = strip_garbage(d)
    assert(d[0]=='{')
    assert(d[-1]=='}')
    num_groups = 1
    total_score = 1
    prev_group_score = 1
    for c in d[1:-1]:
        if c == '{':
            num_groups += 1
            total_score += prev_group_score+1
            prev_group_score += 1
        elif c == '}':
            prev_group_score -= 1
        elif c == ',':
            pass
        else:
            raise ValueError(f'Unexpected character {c}')
    return total_score


def test_parse_group():
    assert(1 == parse_group('{}'))
    assert(6 == parse_group('{{{}}}'))
    assert(5 == parse_group('{{},{}}'))
    assert(16 == parse_group('{{{},{},{{}}}}'))
    assert(1 == parse_group('{<a>,<a>,<a>,<a>}'))
    assert(3 == parse_group('{{<a!>},{<a!>},{<a!>},{<ab>}}'))
    assert(9 == parse_group('{{<ab>},{<ab>},{<ab>},{<ab>}}'))
    assert(9 == parse_group('{{<!!>},{<!!>},{<!!>},{<!!>}}'))

def test_part1():
    result = parse_group(data())
    print('PART 1:', result)
    assert(12505 == result)

def test_part2():
    _, result = strip_garbage(data())
    print('PART 2:', result)
    assert(6671 == result)
    
    
if __name__ == "__main__":
    test_parse_garbage()
    test_parse_group()
    test_part1()
    test_part2()
        

