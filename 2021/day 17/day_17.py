"""
Advent of Code 2021 - Day 17
Pieter Kitslaar
"""

import operator
from pathlib import Path

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

example="""target area: x=20..30, y=-10..-5"""

def parse(txt):
    _, coords_txt = txt.split(':')
    x_range_txt, y_range_txt = coords_txt.strip().split(',')
    x_range = tuple(map(int, x_range_txt.strip()[2:].split('..')))
    y_range = tuple(map(int, y_range_txt.strip()[2:].split('..')))
    return x_range, y_range

def test_example():
    x_range, y_range = parse(example)
    assert (20,30) == x_range
    assert (-10,-5) == y_range

    result, positions = reaches_target((0,0,7,2),(x_range,y_range))
    #print(positions)
    assert result

    result, positions = reaches_target((0,0,6,3),(x_range,y_range))
    #print(positions)
    assert result

    result, positions = reaches_target((0,0,9,0),(x_range,y_range))
    #print(positions)
    assert result

    result, positions = reaches_target((0,0,17,-4),(x_range,y_range))
    #print(positions)
    assert not result

    result, positions  = reaches_target((0,0,6,9),(x_range,y_range))
    #assert result
    assert 45 == max([p[1] for p in positions])

    result, positions  = reaches_target((0,0,6,10),(x_range,y_range))
    assert not result

    result, positions  = reaches_target((0,0,6,8),(x_range,y_range))
    assert result
    assert max([p[1] for p in positions]) < 45

    assert 45 == solve1(0,0,*parse(example))[0]


def probe_step(x,y,vx,vy):
    x += vx
    y += vy
    vx = vx - 1 if vx > 0 else (vx + 1 if vx < 0 else 0)
    vy = vy - 1
    return x,y,vx,vy

def reaches_target(initial, target):
    x,y,vx,vy = initial
    x_range, y_range = target
    positions = [(x,y)]
    while True:
        if x_range[0] <= x <= x_range[1] and y_range[0] <= y <= y_range[1]:
            # inside area
            return True, positions
        elif (
                (x < x_range[0] and vx<=0) or 
                (x > x_range[1] and vx>=0) or 
                (y < y_range[0]) and vy<=0):
                return False, positions
        else:
            x,y,vx,vy = probe_step(x,y,vx,vy)
            positions.append((x,y))

def x_progression(x, vx):
    yield x, vx
    while True:
        x += vx
        vx = vx - 1 if vx > 0 else (vx + 1 if vx < 0 else 0)
        yield x, vx

def y_progression(y, vy):
    yield y, vy
    while True:
        y += vy
        vy = vy - 1
        yield y, vy

from itertools import count

def solve1(start_x, start_y, target_x_range, target_y_range):
    x_speed_steps = find_speed_steps(start_x, target_x_range, x_progression)
    steps_to_speed = {}
    for v, steps in x_speed_steps.items():
        steps_to_speed.setdefault(steps, []).append(v)
    max_steps = max(steps_to_speed)
 
    y_speed_steps = find_speed_steps(start_y, target_y_range, y_progression)
    min_y_speed = min(y_speed_steps)
    highest_results = []
    for VX in steps_to_speed[max_steps]:
        higest_y = (target_y_range[0], None, target_y_range[1])
        for VY in count(min_y_speed, 1):
            result, path = reaches_target((start_x, start_y, VX, VY),(target_x_range, target_y_range))
            if result:
                max_y = max(p[1] for p in path)
                if max_y > higest_y[0]:
                    higest_y = (max_y, VY, path[-1][1])
                    #print(higest_y)
            else:
                if higest_y[1] is not None and higest_y[2] <= target_y_range[0]:
                    break

        highest_results.append((higest_y[0], VX, higest_y[1]))
    return  max(highest_results)
    

def find_speed_steps(start, target_range, progression_func):
    direction = int(target_range[0] > start) or -1
    max_v = target_range[1] - start # maximum speed

    speeds_and_steps = {}
    for V in range(0, max_v+2, direction):
        for i, (p, v) in enumerate(progression_func(start, V)):
            if target_range[0] <= p <= target_range[1]:
                speeds_and_steps[V]=i
                break
            elif (p > target_range[1] and v >= 0) or (p < target_range[1] and v <= 0):
                break
    return speeds_and_steps

def test_part1():
    results = solve1(0,0,*parse(get_input()))
    print('Part1', results[0])
    assert 4753 == results[0]



example_2_results = """\
23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7"""

def parse_results():
    velocities = set()
    for line in example_2_results.splitlines():
        for initial_vel in line.strip().split():
            velocities.add(tuple(map(int, initial_vel.split(','))))
    return velocities

def solve2(start_x, start_y, target_x_range, target_y_range):
    x_speed_steps = find_speed_steps(start_x, target_x_range, x_progression)
    x_speeds = set(x_speed_steps)
    _, _, max_vy = solve1(start_x, start_y, target_x_range, target_y_range)
    min_vy = target_y_range[0]
    velocities = set()
    for vx in x_speeds:
        for vy in range(min_vy, max_vy+1):
            result, _ = reaches_target((start_x, start_y, vx, vy),(target_x_range, target_y_range))
            if result:
                velocities.add((vx, vy))
    return velocities


def test_example2():
    expected = parse_results()
    expected_vx = set(t[0] for t in expected)
    expected_vy = set(t[1] for t in expected)
    assert len(expected) == 112

    results = solve2(0,0,*parse(example))
    assert expected == results
    assert len(results) == 112

def test_part2():
    results = solve2(0,0,*parse(get_input()))
    print('Part 2', len(results))
    
if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()
