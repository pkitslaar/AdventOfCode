"""
Advent of Code 2022 - Day 13
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent


def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

EXAMPLE_DATA = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def compare(a, b):
    if isinstance(a,int) and isinstance(b,int):
        if a == b:
            return "CONTINUE"
        elif a < b:
            return "CORRECT"
        return "NOT_CORRECT"
    else:
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b  = [b]
    if len(a) == 0 and len(b) == 0:
        return "CONTINUE"
    if len(a) == 0 and len(b) > 0:
        return "CORRECT"
    elif len(a) > 0 and len(b) == 0:
        return "NOT_CORRECT"
    result = compare(a[0], b[0])
    if result == "CONTINUE":
        return compare(a[1:],b[1:])
    return result

def solve(d):
    pairs = [[]]
    for line in d.strip().splitlines():
        if not line.strip():
            pairs.append([])
        else:
            pairs[-1].append(eval(line))
    
    correct_indices_sum = 0
    for i, (a,b) in enumerate(pairs):
        result = compare(a, b)
        if False:
            print(a)
            print(b)
            print(result)
            print()
        assert(result != "CONTINUE")
        if result == "CORRECT":
            correct_indices_sum += i+1
    return correct_indices_sum

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(13 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)

class Comparer:
    def __init__(self, line):
        self.val = eval(line)

    def __lt__(self, other):
        return compare(self.val, other.val) == "CORRECT"

def solve2(d):
    lines = list(l.strip() for l in d.splitlines() if l.strip())
    lines.append('[[2]]')
    lines.append('[[6]]')
    lines.sort(key =Comparer)
    return (lines.index('[[2]]')+1)*(lines.index('[[6]]')+1)


def test_example2():
    result = solve2(EXAMPLE_DATA)
    assert(140 == result)

def test_part2():
    result = solve2(data())
    print('PART 2:', result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()
