"""
Advent of Code 2023 - Day 12
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


from functools import cache
from re import match


@cache
def n_solutions(springs, n_broken):
    """
    Based on https://github.com/kaathewise/aoc2023/blob/main/12.py

    I intially tried to solve this using an iterative approach.
    See day_12_initial.py for this attempt.

    This worked for Part 1 and the example of part2.
    For part2 I combined the solutions for Par1 and solutions with
    and additional '?' at the start or end of the string. Next, I tried
    to multiply these solutions based on the possible concationations.
    However, this worked find for the example of Part2 it produced to small results for
    the real Part2. I finally resorted to Reddit and found the solution above.

    Intuitively, I found it hard to understand why the memoization works so well for this problem.
    It seems to number of different input arguments is rather large.
    However, each call reduces the number of characters and there are only a few possible solution
    when the inputs are smaller.
    """
    if not springs:
        # This is the termination condition for the recursion
        # No more springs left to check
        # If there are no more known broken springs to be found
        # else we have found a solution
        return 1 if len(n_broken) == 0 else 0
    else:
        result = 0
        if springs[0] in ".?":
            # this is assuming that the '?' acts as a '.'
            result += n_solutions(springs[1:], n_broken)
        if n_broken:
            n_to_find = n_broken[0]
            # the regex tries to find concecutive '#' or '?' of the correct length
            # thereby assuming all the '?' act as '#'.
            # Not that the regex always wants to end with a '.' or a '?'
            # Therefore we need to always add a '.' to the end of the string
            if m := match(r"[#?]{%d}[.?]" % n_to_find, springs):
                result += n_solutions(springs[len(m.group()) :], n_broken[1:])
    return result


def solve(data, part2=False):
    result = 0
    for row in data.splitlines():
        springs, n_broken = row.split()
        n_broken = tuple(map(int, n_broken.split(",")))

        # note that we add a '.' to the end of the string
        # since the regex in n_solutions always wants to find a '.' or a '?'
        # at the end of a possible broken spring pattern
        if not part2:
            n = n_solutions(springs + ".", n_broken)
        else:
            n = n_solutions("?".join([springs] * 5) + ".", (*n_broken,) * 5)
        result += n
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    print(f"[cache]: {n_solutions.cache_info()}")
    assert result == 21


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    print(f"[cache]: {n_solutions.cache_info()}")
    assert result == 6949


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    print(f"[cache]: {n_solutions.cache_info()}")
    assert result == 525152


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    print(f"[cache]: {n_solutions.cache_info()}")
    assert result == 51456609952403


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
