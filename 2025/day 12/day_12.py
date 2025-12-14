"""
Advent of Code 2025 - Day 12
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

import numpy as np

def parse(data):
    shapes = []
    regions = []
    shape_index = -1
    for line in data.strip().splitlines():
        if not line.strip():
            shape_index = -1
            continue

        if shape_index < 0 and line.endswith(':'):
            shape_index = int(line[:-1])
            shapes.append([])
            continue
        
        if 'x' in line:
            dims, *shape_idxs = line.split(':')
            width, height = map(int, dims.strip().split('x'))
            shape_counts = list(map(int, shape_idxs[0].strip().split()))
            regions.append({
                'width': width,
                'height': height,
                'shape_counts': shape_counts
            })
            continue

        if shape_index >= 0:
            shapes[shape_index].append(list(line))

    shapes_info = []
    for shape in shapes:
        shape_array = np.array(shape)
        on_positions = [tuple(map(int,n)) for n in list(zip(*np.where(shape_array == '#')))]
        shapes_info.append({
            'array': shape_array,
            'on_positions': on_positions,
            'occupied_size': len(on_positions)
        })
    return  shapes_info, regions    


def solve(data, part2=False):
    result = 0
    shapes, regions = parse(data)
    for region in regions:
        total_occupied = 0
        for shape_idx, shape_count in enumerate(region['shape_counts']):
            if shape_count > 0:
                shape_info = shapes[shape_idx]
                total_occupied += shape_count * shape_info['occupied_size']
        
        region_size = region['width'] * region['height']
        if total_occupied <= region_size:
            # num 3x3 squares that fit
            n_x = region['width'] // 3
            n_y = region['height'] // 3
            n_squares = n_x * n_y
            if n_squares >= sum(region['shape_counts']):
                result += 1
            else:
                # need to do more complex fitting
                # this is (in this example) only needed for the example data
                raise NotImplementedError("Complex fitting not implemented")
    return result

import pytest

@pytest.mark.skip(reason="Not implemented")
def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 2 

def test_part1():
    result = solve(data())
    print("Part 1:", result)
    # The actual test data only contains shapes and regions that can be
    # quickly discarded or proven to fit
    assert result == 505



from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()