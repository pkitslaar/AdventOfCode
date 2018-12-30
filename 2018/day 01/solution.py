# Advent of code - 2018
# Day 1
#
# Pieter Kitslaar
#
from collections import Counter
from itertools import cycle

all_changes = []
with open('input.txt', 'r') as f:
    for l in f:
        all_changes.append(int(l.strip()))
result = sum(all_changes)  
print(result) # part 1

result = 0
result_by_change = Counter()
for change in cycle(all_changes):
    result += change
    result_by_change[result] += 1
    if result_by_change[result] == 2:
        print('First frequency reached twice', result) # part 2
        break

