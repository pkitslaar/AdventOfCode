"""
Advent of Code 2020 - Day 06
Pieter Kitslaar
"""

from pathlib import Path
import string

example = """\
abc

a
b
c

ab
ac

a
a
a
a

b"""

def solve(txt, answered_by_all=False):
    """
    Parse the lines and for each group (separeted by blank lines) count the
    number of ansers.

    When 'answered_by_all' is False (par1), we keep adding the unique answers to an empty
    set to obtain the final collection of answers which where answered by ANY member.

    When 'answered_by_all' is True (part2), we start with a default set of all possible answers
    and only keep the intersection with the answers for each person. The left over set will
    be set of answers given by ALL members of the group.
    """
    groups = []
    def new_group():
        """Helper function to add a new group to the list
        When 'answered_by_all' is False we simply add an empty set.
        When 'answered_by_all' is True we add a set with all lower_case letters.
        """
        groups.append(set(string.ascii_lowercase) if answered_by_all else set())

    new_group() # initial group
    for line in txt.splitlines():
        if not line: # blank line, add new group
            new_group()
        else:
            if answered_by_all:
                # Update the group answers by taking the intersection with the
                # answers of the current person
                groups[-1].intersection_update(set(line))
            else:
                # Update the group answers by adding the answers for the current
                # person
                groups[-1].update(line)
    return groups

def test_example():
    groups_any = solve(example)
    summed_any = sum([len(g) for g in groups_any])
    assert(11 == summed_any)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    groups = solve(get_input())
    summed = sum([len(g) for g in groups])
    assert(6726 == summed)
    print('Part 1:', summed)

def test_example2():
    groups_all = solve(example, True)
    summed_all = sum([len(g) for g in groups_all])
    assert(6 == summed_all)

def test_part2():
    groups = solve(get_input(), True)
    summed = sum([len(g) for g in groups])
    assert(3316 == summed)
    print('Part 2:', summed)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()
