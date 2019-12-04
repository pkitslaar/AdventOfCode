"""
Day 4 puzzle - Advent of Code 2019
Pieter Kitslaar
"""
from itertools import groupby

def has_doubles(group_length):
    return group_length > 1

def has_pair(group_length):
    return group_length == 2 

def check_password(v, check_length=has_doubles):
    # Convert number to individual digits
    digits = [int(d) for d in str(v)]
    # group adjacent digits
    groups = [(k, len(list(g))) for k, g in groupby(digits)]
    # get the value of the digits in the group
    group_values = [k for k,_ in groups]
    # differences between adjacent values
    diffs = [current - prev for (current, prev) in zip(group_values[1:], group_values)]
    increases = all(d >= 0 for d in diffs)
    if increases:
        # length of each group
        group_lengths = [l for _,l in groups]

        # check if the sizes of the group match
        # for Part1 and Part2 there are different criteria
        if any(check_length(l) for l in group_lengths):
            return True

    return False


assert(check_password('111111') == True)
assert(check_password('223450') == False)
assert(check_password('123789') == False)
assert(check_password('123788') == True)

puzzle_range = (246540, 787419)

def generate_passwords(lower, upper, check_func):
    for v in range(lower, upper):
        if(check_func(v)):
            yield v

# Part 1
part1_computation = len(list(generate_passwords(puzzle_range[0], puzzle_range[1], check_password)))
print('Part 1:', part1_computation)
assert(1063 == part1_computation)

# Part 2
check_password_2 = lambda v: check_password(v, has_pair)
assert(check_password_2('123455') == True)
assert(check_password_2('111111') == False)
assert(check_password_2('112233') == True)
assert(check_password_2('111122') == True)
assert(check_password_2('123444') == False)

part2_computation = len(list(generate_passwords(puzzle_range[0], puzzle_range[1], check_password_2)))
print('Part 2:', part2_computation)
assert(686 == part2_computation)