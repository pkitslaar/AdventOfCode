"""
Advent of Code 2021 - Day 10
Pieter Kitslaar
"""

from pathlib import Path

example = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


CLOSE_TO_OPEN_TAGS = {')': '(', ']':'[', '}':'{','>':'<'}
OPEN_TO_CLOSE_TAGS = {v:k for k,v in CLOSE_TO_OPEN_TAGS.items()}

CORRUPT_SCORES = {')': 3,']': 57, '}': 1197, '>': 25137}
INCOMPLETE_SCORES = {')': 1,']': 2, '}': 3, '>': 4}

def parse(txt):
    for line in txt.splitlines():
        yield line

def analyse(txt):
    line_results = []
    for line in parse(txt):
        assert line[0] in OPEN_TO_CLOSE_TAGS
        this_result = None
        open_tags = []
        for c_index, c in enumerate(line):
            if c in OPEN_TO_CLOSE_TAGS:
                open_tags.append(c)
            elif c in CLOSE_TO_OPEN_TAGS:
                expected_close = OPEN_TO_CLOSE_TAGS[open_tags[-1]]
                if c != expected_close:
                    this_result = ('CORRUPT', c, expected_close, line)
                    break
                else:
                    open_tags.pop()
        if this_result:
            line_results.append(this_result)
        else:
            if open_tags:
                line_results.append(('INCOMPLETE', open_tags, line))
    
    for r in line_results:
        yield r

def solve1(txt):
    score = 0
    for t in analyse(txt):
        if t[0] == 'CORRUPT':
            illegal_character = t[1]
            score += CORRUPT_SCORES[illegal_character]
    return score

def test_example():
    result = solve1(example)
    assert 26397 == result

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    result = solve1(get_input())
    print('Part 1:', result)

def compute_incomplete_score(close_sequence):
    sum = 0
    for c in close_sequence:
        sum = (sum*5) + INCOMPLETE_SCORES[c]
    return sum

def solve2(txt):
    line_scores = []
    for t in analyse(txt):
        if t[0] == 'INCOMPLETE':
            open_tags, line = t[1:]
            close_sequence = ''.join([OPEN_TO_CLOSE_TAGS[o] for o in reversed(open_tags)])
            line_score = compute_incomplete_score(close_sequence)
            line_scores.append(line_score)
    line_scores.sort()
    return line_scores[len(line_scores)//2]

def test_example2():
    result = solve2(example)
    assert 288957 == result

def test_part2():
    result = solve2(get_input())
    print('Part 2:', result)
    assert 820045242 == result

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()


