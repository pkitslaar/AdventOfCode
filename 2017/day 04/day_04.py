"""
Advent of Code 2017 - Day 04
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

from collections import Counter
def validate(pass_phrase):
    counts = Counter(pass_phrase.strip().split())
    return counts.most_common(1)[0][1] == 1

assert(True  == validate("aa bb cc dd ee"))
assert(False == validate("aa bb cc dd aa"))
assert(True == validate("aa bb cc dd aaa"))

def part1():
    result = sum(1 for l in data().splitlines() if validate(l))
    print('PART 1:', result)
    assert(383 == result)

def validate2(pass_phrase):
    counts = Counter(''.join(sorted(word)) for word in pass_phrase.strip().split())
    return counts.most_common(1)[0][1] == 1

assert(True == validate2("abcde fghij"))
assert(False == validate2("abcde xyz ecdab"))
assert(True == validate2("a ab abc abd abf abj"))
assert(True == validate2("iiii oiii ooii oooi oooo"))
assert(False == validate2("oiii ioii iioi iiio"))

def part2():
    result = sum(1 for l in data().splitlines() if validate2(l))
    print('PART 2:', result)
    assert(265 == result)

if __name__ == "__main__":
    part1()
    part2()
