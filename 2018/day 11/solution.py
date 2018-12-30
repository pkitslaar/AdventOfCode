# Advent of code - 2018
# Day 11
#
# Pieter Kitslaar
#

import numpy as np

GRID_SIZE = 300
SUB_GRID_SIZE = 3

def create_grid(serial_number):
    grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    for y_index, row in enumerate(grid):
        y = y_index + 1
        for x_index, cell_value in enumerate(row):
            x = x_index + 1
            rack_id = x + 10
            power_level = rack_id * y
            increased_level = power_level + serial_number
            multiplied = increased_level * rack_id
            str_multiplied = str(multiplied)
            hundred_digit = int(str_multiplied[-3]) if len(str_multiplied) > 2 else 0
            final_level = hundred_digit - 5
            row[x_index] = final_level
    return np.array(grid)

def sub_grid(grid, top_left, sub_grid_size = SUB_GRID_SIZE):
   start_x_index = top_left[0]-1
   start_y_index = top_left[1]-1
   return grid[ start_y_index:start_y_index+sub_grid_size, 
                start_x_index:start_x_index+sub_grid_size]
   
def power(grid):
    return np.sum(grid)
    
def max_sub_power_coord(grid, sub_grid_size = SUB_GRID_SIZE):
    powers = []
    for start_y in range(0, GRID_SIZE-sub_grid_size):
        for start_x in range(0, GRID_SIZE-sub_grid_size):
            coord = (start_x+1, start_y+1)
            sg = sub_grid(grid, coord, sub_grid_size)
            powers.append((coord, power(sg)))
    powers.sort(key = lambda t: t[1])
    return powers[-1]
    
def max_sub_power_coord_size(grid):
    powers = []
    for sub_grid_size in range(2, GRID_SIZE-1):
        max_coord, max_power = max_sub_power_coord(grid, sub_grid_size)
        powers.append(((max_coord[0], max_coord[1], sub_grid_size), max_power))
    powers.sort(key = lambda t: t[1])
    return powers[-1]        
    
def get_value(grid, x, y):
    return grid[y-1][x-1]

example_grid_8 = create_grid(8)
assert(4 == get_value(example_grid_8, 3, 5))

example_grid_18 = create_grid(18)
sub_18 = sub_grid(example_grid_18, (33,45))
assert(29 == power(sub_18))
max_coord, max_power = max_sub_power_coord(example_grid_18)
assert((33,45)==max_coord )

example_grid_42 = create_grid(42)
sub_42 = sub_grid(example_grid_42, (21,61))
assert(30 == power(sub_42))
max_coord, max_power = max_sub_power_coord(example_grid_42)
assert((21,61) == max_coord)

# Test grid: Serial 7689
test_grid = create_grid(7689)
max_coord, max_power = max_sub_power_coord(test_grid)
print('PART 1:', max_coord, 'max power', max_power)

max_coord_size, max_power = max_sub_power_coord_size(test_grid)
print('PART 2:', max_coord_size, 'max power', max_power)
