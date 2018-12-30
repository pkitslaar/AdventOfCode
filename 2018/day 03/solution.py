# Advent of code - 2018
# Day 3
#
# Pieter Kitslaar
import re
from collections import defaultdict

group_names = ('id', 'x', 'y', 'w', 'h')
claim_re = re.compile('\#(\d+) \@ (\d+),(\d+): (\d+)x(\d+)')

claims = []
with open('input.txt', 'r') as f:
    for l in f:
        m = claim_re.match(l)
        m_d = dict(zip(group_names, map(int, m.groups())))
        claims.append(m_d)

def claim_coords(claim):
    for y in range(claim['y'], claim['y'] + claim['h']):
        for x in range(claim['x'], claim['x'] + claim['w']):
            yield (x,y)

fabric_claims= defaultdict(list)
for claim in claims:
    for coord in claim_coords(claim):
        fabric_claims[coord].append(claim['id'])

overlap = sum(1 for coord, hits in fabric_claims.items() if len(hits) > 1)
print(overlap) # part 1

conflicts = defaultdict(set)
for hits in fabric_claims.values():
    for claim_id in hits:
        conflicts[claim_id].update(hits)

for k, v in conflicts.items():
    if len(v) == 1:
        print(k, v) # part 2

