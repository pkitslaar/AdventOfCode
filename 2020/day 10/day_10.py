"""
Advent of Code 2020 - Day 10
Pieter Kitslaar
"""

from pathlib import Path
from collections import Counter
from functools import reduce

example_a = """\
16
10
15
5
1
11
7
19
6
12
4"""

def parse(txt):
    values = list(map(int, txt.splitlines()))
    values.sort()
    return values

def compute_diffs(txt):
    values = parse(txt)
    values.append(max(values)+3)
    prev = 0
    differences = []
    for v in values:
        differences.append(v - prev)
        prev = v
    return differences

def compute_combinations(differences):
    """
    Here we compute the number of consecutive '1' difference.
    Each number of consecutive '1's can be substituted for a number
    of combinations of 1,2 and 3 jolt difference adapters.
    These can be easily used to define a multiplier for each of these
    difference groups which when multiplied provide the total number of
    combinations.

    2: 1,1  => 2
       2

    3: 1,1,1   => 4
       1,2
       2,1
       3
    
    4: 1,1,1,1 => 7
       2,1,1
       2,2
       1,2,1
       1,1,2
       3,1
       1,3
    """
    prev_diff = 0
    diff_runs = []
    for d in differences:
        if d == 1:
            if d != prev_diff:
                diff_runs.append(1)
            else:
                diff_runs[-1] += 1
        prev_diff = d
    diff_runs = [dr for dr in diff_runs if dr > 1]

    # see doc string
    multiplier = {1:1, 2:2, 3:4, 4:7}
    return reduce(lambda a,b:a*multiplier[b],diff_runs, 1)

def test_example_a():
    differences = compute_diffs(example_a)
    diff_count = Counter(differences)
    assert(diff_count[1] == 7)
    assert(diff_count[3] == 5)
    num_combinations = compute_combinations(differences)
    assert(8 == num_combinations)

example_b = """\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

def test_example_b():
    differences = compute_diffs(example_b)
    diff_count = Counter(differences)
    assert(diff_count[1] == 22)
    assert(diff_count[3] == 10)
    num_combinations = compute_combinations(differences)
    assert(19208 == num_combinations)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_puzzle():
    differences = compute_diffs(get_input())
    diff_count = Counter(differences)
    answer = diff_count[1]*diff_count[3]
    print('Part 1:', answer)
    assert(1980 == answer)
    num_combinations = compute_combinations(differences)
    print('Part 2:', num_combinations)
    assert(4628074479616 == num_combinations)


if __name__ == "__main__":
    test_example_a()
    test_example_b()
    test_puzzle()

