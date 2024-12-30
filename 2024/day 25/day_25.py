"""
Advent of Code 2024 - Day 25
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

from collections import Counter

def parse(data):
    keys = []
    locks = []
    current_element = '', None
    for line in data.strip().splitlines():
        if not line.strip():
            current_element = '', None
            continue
        if not current_element[0]:
            current_element_value = Counter()
            if set(line) == {'#'}:
                current_element = 'lock', current_element_value
                locks.append(current_element_value)
            else:
                assert set(line) == {'.'}
                current_element = 'key', current_element_value
                keys.append(current_element_value)
            continue

        for x, c in enumerate(line):
            current_element[1][x] += 1 if c == '#' else 0

    keys = [tuple(kv-1 for kv in k.values()) for k in keys]
    locks = [tuple(l.values()) for l in locks]
    return keys, locks


def solve(data, part2=False):
    keys, locks = parse(data)
    for elements in keys, locks:
        max_h = max(max(element) for element in elements)
        min_h = min(min(element) for element in elements)
        assert max_h == 5
        assert min_h == 0

    original_keys = keys
    unique_keys = set(k for k in keys)
    if len(unique_keys) != len(keys):
        print("duplicate keys")	
        keys = [k for k in unique_keys]
        keys.sort()
            
    original_locks = locks
    unique_Locks = set(l for l in locks)
    if len(unique_Locks) != len(locks):
        print("duplicate locks")
        locks = [l for l in unique_Locks]
        locks.sort()

    
    result = 0
    non_matching_pairs = 0
    for l in locks:
        for k in keys:
            if any(k+l > 5 for k,l in zip(k,l)):
                non_matching_pairs += 1
            else:
                result += 1
    assert result + non_matching_pairs == len(keys) * len(locks)
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 3


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result < 6230
    assert result < 5827


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == -1


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == -1


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()