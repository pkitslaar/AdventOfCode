# Advent of code - 2018
# Day 25 
#
# Pieter Kitslaar
#

import numpy as np

# Setup an array with all neighbor offsets in the 4D grid
# that are within 3 Manhatthan distance and are 'before'
# the center coordinate. These are the neighbors to
# examine while traversing the coordinates to find
# 'connected' other coordinates
ALL_NEIGHBORS = [(x,y,z,t) for x in range(-3,3) for y in range(-3,3) for z in range(-3,3) for t in range(-3,3)]
ALL_NEIGHBORS.sort(key = lambda t: t[::-1])
CENTER = ALL_NEIGHBORS.index((0,0,0,0))
BACK_NEIGHBORS = np.array(ALL_NEIGHBORS[:CENTER])
LABEL_NEIGHBORS = BACK_NEIGHBORS[np.sum(np.abs(BACK_NEIGHBORS), axis=1) < 4]

def parse(data):
    coords = []
    for l in data.splitlines():
        coords.append(list(map(int, l.split(','))))
    # sort the coordinates so we will process them
    # in a logicial coordinate order
    coords.sort(key = lambda t: t[::-1])
    return np.array(coords)

def grid(coords):
    coords_min = np.min(coords, axis=0)
    grid_size = np.max(coords, axis=0) - coords_min + 1
    grid = np.zeros(grid_size, np.int8)
    mod_coords = coords - coords_min
    indices = coords_to_indices(mod_coords)
    grid[indices] = 1
    return grid, mod_coords

def coords_to_indices(coords):
    return tuple([coords[:,i] for i in range(coords.shape[1])])

def indices_to_coords(indices):
    return np.vstack(indices).T

def processed_neighbors(coord, shape):
    all_backwards = coord + LABEL_NEIGHBORS
    inside_max_bound = np.min(all_backwards < shape, axis=1) == True
    inside_min_bound = np.min(all_backwards >= 0, axis=1) == True
    valid = all_backwards[inside_max_bound & inside_min_bound]
    array_indices = coords_to_indices(valid)
    return array_indices

def filter_indices(indices, include):
    return tuple([v[include] for v in indices])
    

def label(coords, grid):
    labels = -1*np.ones_like(grid, dtype=np.int_)
    labels[grid > 0] = 0 
    max_label = 0
    for c in coords:
        nh = processed_neighbors(c, grid.shape)
        nh_coords = filter_indices(nh, grid[nh] > 0)
        nh_labels = labels[nh_coords].tolist()
        if not nh_labels:
            max_label += 1
            labels[coords_to_indices(c.reshape((-1,4)))] = max_label 
        else:
            exist_label = min(nh_labels)
            labels[coords_to_indices(c.reshape((-1,4)))] = exist_label 
            for l in nh_labels:
                if l != exist_label:
                    labels[labels == l] = exist_label
    label_values = set(np.unique(labels))
    label_values.remove(-1)
    return len(label_values)

def solve(raw_data):    
    data = parse(raw_data)
    g, coords = grid(data)
    num = label(coords, g)
    return num

example1 = """\
 0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0"""
assert(2 == solve(example1))

example2 = """\
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""
assert(4 == solve(example2))

example3="""\
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2"""
assert(3 == solve(example3))

example4="""\
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""
assert(8 == solve(example4))

with open('input.txt') as f:
    num = solve(f.read())
    print(f'PART 1: number of constilations {num}')

