# Advent of code - 2018
# Day 23 
#
# Pieter Kitslaar
#

import numpy as np
import re
regex = re.compile('-*\d+')

example_data = """\
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
"""

X, Y, Z, R = range(4)
COORDS = slice(X,R)

def parse(data):
    points = []
    for l in data.splitlines():
        x, y, z, r = map(int,regex.findall(l))
        points.append((x,y,z,r))
    points.sort(key = lambda t: t[-1], reverse = True) # sort by radius
    return np.array(points, dtype=np.int_)

def expand(k, data):
    expanded = []
    to_process = [[k]]
    while to_process:
        expanded.extend(to_process)
        new_to_process = []
        for sequence in to_process:
            root, c = sequence[0], sequence[-1]
            root_parents = data.get(root, set())
            c_parents = data.get(c, set())
            if c_parents:
                for p in c_parents:
                    if p in root_parents:
                        new_to_process.append(sequence + [p])
        to_process = new_to_process
    expanded.extend(to_process)
    print('Returning largest')
    expanded.sort(key = lambda g: len(g), reverse=True)
    return expanded[0]

def overlap(points):
    print('Computing overlap')
    overlaps = []
    for i, p in enumerate(points):
        #other_points = points[i+1:]
        has_overlap = np.sum(np.abs(points[:, COORDS] - p[COORDS]), axis=1) <= (points[:, R] + p[R])
        overlappig = np.argwhere(has_overlap).flatten().tolist()
        overlap_set = set(overlappig)
        overlaps.append(overlap_set)
    #print(overlaps)
    overlap_keys = set([tuple(ol) for ol in overlaps])
    overlap_count = {}
    for ol_key in overlap_keys:
        ol = set(ol_key)
        count = 0
        for other in overlaps:
            if ol.issubset(other):
                count += 1
        overlap_count[ol_key] = count
    #print(overlap_count)
    full_overlaps = [(v,k) for k,v in overlap_count.items() if v == len(k)]
    full_overlaps.sort(reverse=True)

    # find the groups with maximum overlap
    max_overlaps = [full_overlaps[0]]
    for n, group in full_overlaps[1:]:
        if n == max_overlaps[0][0]:
            max_overlaps.append((n,group))
    print('Found', len(max_overlaps), 'overlap groups')
    #print(*max_overlaps, sep='\n')
    for n, g in max_overlaps:
        g_points = np.take(points, g, axis=0)
        dist_origin = np.sum(np.abs(g_points[:, COORDS]), axis=1) - g_points[:, R]
        print(dist_origin)
        min_distance_all_overlap = np.max(dist_origin)
        print('PART 2: distance max overlap', min_distance_all_overlap)
        1/0

def solve(data):
    points = parse(data)
    largest_point = points[np.argmax(points[:,3], axis=0)]
    #print(largest_point)
    distance = np.sum(np.abs(points[:,0:3] - largest_point[0:3]), axis=1)
    in_range = (largest_point[3] - distance) >= 0
    print('PART 1: num in range', np.sum(in_range))
    return points

print('Example')
p = solve(example_data)
print()

example_part_2 = """\
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
"""
p = solve(example_part_2)
overlap(p)

if True:
    print('Assignment')
    with open('input.txt') as f:
        p = solve(f.read())
        overlap(p)
        print()

