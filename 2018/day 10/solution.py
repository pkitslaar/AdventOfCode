# Advent of code - 2018
# Day 10
#
# Pieter Kitslaar
#

import re
from collections import deque

# Setup some constants
POSITIONS, VELOCITIES = range(2)

def parse(text):
    data = {
        POSITIONS: [],
        VELOCITIES: [],
    }
    tuple_re = re.compile('\<(.+?),(.+?)\>')
    for l in text.splitlines():
        for i, m in enumerate(tuple_re.finditer(l)):
            data[i].append([int(g) for g in m.groups()])
    return data

def bounding_box(data):
    x_pos = [x for x,y in data[POSITIONS]]
    y_pos = [y for x,y in data[POSITIONS]]
    return min(x_pos), max(x_pos), min(y_pos), max(y_pos)

def rect_area(x_min, x_max, y_min, y_max):
        return (x_max-x_min)*(y_max-y_min)

def step(data):
    """Take the current positiona and velocity data and produce new version
    with updated positions."""
    new_data = {POSITIONS:[], VELOCITIES:[]}
    for pos, v in zip(data[POSITIONS], data[VELOCITIES]):
        new_data[POSITIONS].append([
            pos[0] + v[0],
            pos[1] + v[1],
        ])
        new_data[VELOCITIES].append(v)
    return new_data

def step_until_minimum(data):
    """Starting from the input, update the positions until a minimum bounding box area is obtained."""
    start_area = rect_area(*bounding_box(data)) 
    iteration_data = deque([(data, start_area)], maxlen=2)
    num_iterations = 0
    while len(iteration_data) < 2 or iteration_data[-1][1] < iteration_data[-2][1]:
        new_data = step(iteration_data[-1][0])
        new_area = rect_area(*bounding_box(new_data))
        iteration_data.append((new_data, new_area))
        num_iterations += 1
    print(len(iteration_data))
    return iteration_data[-2][0], num_iterations-1 

def grid(data):
    """Create a 2D grid representation of the positions."""
    min_x, max_x, min_y, max_y = bounding_box(data)
    # create grid from bbox with additional border of 3
    grid = [['.']*(max_x-min_x+3) for y in range(min_y, max_y+3)]
    for x,y in data[POSITIONS]:
        local_x = x-min_x+1
        local_y = y-min_y+1
        grid[local_y][local_x] = '#'
    return grid

def print_grid(grid):
    for l in grid:
        print(''.join(l))
    
def solve(input_file):
    """Load the positions and velocities from file and find the minimum area."""
    with open(input_file) as f:
        test_data = parse(f.read())
    test_result, number_of_seconds = step_until_minimum(test_data)
    print_grid(grid(test_result))
    print('Took', number_of_seconds, 'seconds')

# Example data
print('Example')
solve('test_input.txt')
print()

# Real data
print('PART 1 + 2:')
solve('input.txt')


