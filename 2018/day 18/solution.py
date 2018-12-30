# Advent of code - 2018
#
# Day 18
#
# Pieter Kitslaar
#

import numpy as np

class GridCoords(object):
    """Helper class to easily handle coordinates in a 2D numpy array (grid)"""

    def __init__(self, grid_shape, grid_indices = None):
        self.grid_shape = grid_shape
        self.grid_indices = grid_indices or (np.empty(0), np.empty(0))

    def Y(self):
        return self.grid_indices[0]
    
    def X(self):
        return self.grid_indices[1]

    def as_tuples(self):
        return zip(*self.grid_indices)

    def __str__(self):
        return str(list(self.as_tuples()))

    def filter(self, include):
        return GridCoords(self.grid_shape, 
            (
                self.grid_indices[0][include],
                self.grid_indices[1][include],
            ))

    def get_values(self, value_map):
        return value_map[self.grid_indices]

    @staticmethod
    def combine(*grid_coords):
        combined_y = np.hstack([gc.Y() for gc in grid_coords])
        combined_x = np.hstack([gc.X() for gc in grid_coords])
        first_shape = grid_coords[0].grid_shape
        assert(all(first_shape == gc.grid_shape for gc in grid_coords))
        return GridCoords(first_shape, (combined_y, combined_x))

    @staticmethod
    def neighborhood(shape, center_y, center_x):
        offsets = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            ( 1,-1),
            ( 1, 0),
            ( 1, 1),
            ( 0, 1),
            ( 0,-1),
        ]
        neighbours_y = [] 
        neighbours_x = [] 
        for offset_x, offset_y in offsets:
            if 0 <= center_x+offset_x < shape[1] and 0 <= center_y+offset_y < shape[0]:
                neighbours_y.append(center_y+offset_y)
                neighbours_x.append(center_x+offset_x)
        return GridCoords(shape, (np.array(neighbours_y), np.array(neighbours_x)))


OPEN, TREES, LUMBER = range(3)

CHAR_TABLE = {
    '#': LUMBER,
    '|': TREES,
    '.': OPEN,
}
VALUE_TABLE = {v:k for k,v in CHAR_TABLE.items()}

test = """\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""

def parse(txt):
    rows = []
    for l in txt.splitlines():
        rows.append([CHAR_TABLE[c] for c in l])
    return np.array(rows)

def next(data):
    shape = data.shape
    new_data = np.zeros_like(data)
    for y in range(shape[0]):
        for x in range(shape[1]):
            current = data[y][x]
            new_value = current
            nh = GridCoords.neighborhood(shape, y, x)
            nh_values = nh.get_values(data)
            if current == OPEN:
                if np.sum(nh_values == TREES) > 2:
                    new_value = TREES
            if current == TREES:
                if np.sum(nh_values == LUMBER) > 2:
                    new_value = LUMBER
            if current == LUMBER:
                num_lumb = np.sum(nh_values == LUMBER)
                num_tree = np.sum(nh_values == TREES)
                if num_lumb > 0 and num_tree > 0:
                    new_value = LUMBER
                else:
                    new_value = OPEN

            new_data[y][x] = new_value
    return new_data

def print_grid(data):
    for r in data:
        print(''.join([VALUE_TABLE[v] for v in r]))

def resource_value(new_data):
    num_wood = np.sum(new_data == TREES)
    num_lumber = np.sum(new_data == LUMBER)
    value = num_wood*num_lumber
    return value

def iterate(data, num_minutes, plot = False, use_hash = False):
    if plot:
        print_grid(data)
        print()

    lookup = {}
    prev_data = data
    new_data = None
    prev_hash = None
    for i in range(num_minutes):
        if use_hash:
            prev_hash = prev_hash or hash(prev_data.data.tobytes())
            if prev_hash in lookup:
                new_hash, new_data = lookup[prev_hash]
            else:
                new_data =  next(prev_data)
                new_hash = hash(new_data.data.tobytes())
                lookup[prev_hash] = (new_hash, new_data)
            prev_hash = new_hash
        else:
            new_data = next(prev_data)
        prev_data = new_data
        if plot:
            print_grid(new_data)
            print()
    return resource_value(new_data)

# Example
test_data = parse(test)
assert(1147 == iterate(test_data, 10))

# PART 1
with open('input.txt') as f:
    real_data = parse(f.read())

real_result = iterate(real_data, 10)
print('PART 1: resource value', real_result)
assert(545600 == real_result)

print('PART 2: ', iterate(real_data, 1000000000, plot=False, use_hash=True))

                
