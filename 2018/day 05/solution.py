# Advent of code - 2018
# Day 5
#
# Pieter Kitslaar
#

import re
import string

# expression matching same characters (ignoring case)
p1 = re.compile('[a-z][A-Z]')
p2 = re.compile('[A-Z][a-z]')

def collapse_pair(m):
    """Takes a matching pair and checks if they have the different case."""
    pair = m.group(0)
    if pair[0].lower() == pair[1].lower():
        return ''
    return pair

with open('input.txt', 'r') as f:
    polymer = f.read().strip()


def react(polymer):
    prev_collapsed = polymer
    iteration = 0
    while True:
        #print(iteration, len(prev_collapsed))
        iteration += 1
        collapsed = p1.sub(collapse_pair, prev_collapsed)
        collapsed = p2.sub(collapse_pair, collapsed)
        if len(collapsed) == len(prev_collapsed):
            break
        prev_collapsed = collapsed
    return collapsed

collapsed = react(polymer)
print('PART 1:' , len(collapsed))

result = {}
for c in string.ascii_lowercase:
    modified_polymer = re.sub(c, '', polymer, flags=re.IGNORECASE)
    result[c] = len(react(modified_polymer))
    print(c, result[c])

sort_result = sorted(result.items(), key = lambda t: t[1]) 
print('PART 2:', sort_result[0])
