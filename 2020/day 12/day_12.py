"""
Advent of Code 2020 - Day 12
Pieter Kitslaar
"""

from pathlib import Path
import numpy as np

DIRECTIONS = {
    #         x   y
    'N':   (  0,  1),
    'E':   (  1,  0),
    'S':   (  0, -1),
    'W':   ( -1,  0),
}
DIRECTION_ORDER = list(DIRECTIONS)

def rotate(current_facing, direction, angle):
    assert(angle % 90 == 0)
    current_index = DIRECTION_ORDER.index(current_facing)
    num_turns = angle // 90
    index_step = 1 if direction == 'R' else -1
    new_index = (current_index + num_turns*index_step) % 4
    return DIRECTION_ORDER[new_index]

def test_rotate():
    assert('E' == rotate('N', 'R', 90))
    assert('W' == rotate('N', 'L', 90))
    assert('N' == rotate('E', 'L', 90))
    assert('S' == rotate('E', 'R', 90))
    assert('S' == rotate('N', 'R', 180))

example = """\
F10
N3
F7
R90
F11"""

def navigate(txt):
    state = [{'facing': 'E', 'x': 0, 'y': 0}]
    for instruction in txt.splitlines():
        current_state = state[-1]
        command, value = instruction[0], int(instruction[1:])
        if command == 'F':
            command = current_state['facing']
        step = (0,0)
        new_facing = current_state['facing']
        if command in DIRECTIONS:
            step = tuple([s*value for s in DIRECTIONS[command]])
        else:
            if command in 'LR':
                new_facing = rotate(current_state['facing'], command, value)
            else:
                raise RuntimeError('Unknown command', instruction)
        new_state = {
            'facing': new_facing,
            'x': current_state['x'] + step[0],
            'y': current_state['y'] + step[1]
        }
        state.append(new_state)
    return state

def test_example():
    states = navigate(example)
    distance = abs(states[-1]['x']) + abs(states[-1]['y'])
    assert(25 == distance)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    states = navigate(get_input())
    distance = abs(states[-1]['x']) + abs(states[-1]['y'])
    print('Part 1:', distance)
    assert(1687 == distance)

ROTATION_MATRIX = {
    'L': np.array([[ 0, -1],[ 1, 0]]),
    'R': np.array([[ 0,  1],[-1, 0]])
}

def test_rotate_coord():
    assert((0,1) == rotate_coord((1,0), 'L', 90))
    assert((0,4) == rotate_coord((4,0), 'L', 90))
    assert((0,-4) == rotate_coord((4,0), 'R', 90))
    assert((4,0) == rotate_coord((4,0), 'R', 360))
    assert((-4,-10) == rotate_coord((10,-4), 'R', 90))

def rotate_coord(xy, direction, angle):
    assert(angle % 90 == 0)
    for _ in range(angle // 90):
        if direction == 'R':
            xy = (xy[1],-xy[0])
        else:
            xy = (-xy[1],xy[0])
    return xy


def navigate_with_waypoint(txt):
    state = [{'x': 0, 'y': 0, 'waypoint_x': 10, 'waypoint_y': 1}]
    for instruction in txt.splitlines():
        current_state = state[-1]
        relative_waypoint = (
            current_state['waypoint_x'],
            current_state['waypoint_y'],
        )
        command, value = instruction[0], int(instruction[1:])
        if command in 'LR':
            # rotate way point
            new_relative_waypoint = rotate_coord(relative_waypoint, command, value)
            new_state = {
                'x': current_state['x'],
                'y': current_state['y'],
                'waypoint_x' : new_relative_waypoint[0],
                'waypoint_y' : new_relative_waypoint[1],
            }
        else:
            ship_step = (0,0)
            waypoint_step = (0,0)
            if command == 'F':
                ship_step = [value*s for s in relative_waypoint]
            elif command in DIRECTIONS:
                waypoint_step = tuple([s*value for s in DIRECTIONS[command]])
            new_state = {
                'x': current_state['x'] + ship_step[0],
                'y': current_state['y'] + ship_step[1],
                'waypoint_x' : current_state['waypoint_x'] + waypoint_step[0],
                'waypoint_y' : current_state['waypoint_y'] + waypoint_step[1],
            }
        state.append(new_state)
    return state

def test_example_part2():
    states = navigate_with_waypoint(example)
    distance = abs(states[-1]['x']) + abs(states[-1]['y'])
    assert(286 == distance)

def test_part2():
    states = navigate_with_waypoint(get_input())
    distance = abs(states[-1]['x']) + abs(states[-1]['y'])
    print('Part 2:', distance)
    assert(20873 == distance)

if __name__ == "__main__":
    test_rotate()
    test_example()
    test_part1()
    test_rotate_coord()
    test_example_part2()
    test_part2()

