"""
Day 3 puzzle - Advent of Code 2019
Pieter Kitslaar
"""

UNIT_MOVES = {
    'R': ( 1, 0),
    'U': ( 0, 1),
    'L': (-1, 0),
    'D': ( 0,-1)
}

def code_to_movement(code):
    direction, distance = code[0], code[1:]
    unit_move = UNIT_MOVES[direction]    
    return [unit_move for _ in range(int(distance))]

def wire_to_positions(wire_txt):
    positions = [(0, 0)]
    for code in wire_txt.split(','):
        movements = code_to_movement(code)
        for movement in movements:            
            positions.append((positions[-1][0]+movement[0], positions[-1][1]+movement[1]))
    return positions

def manhattan(p):
    return abs(p[0]) + abs(p[1])


def find_cross_points(wire1, wire2):
    wire1_path = wire_to_positions(wire1)    
    wire2_path = wire_to_positions(wire2)
    cross_points = set(wire1_path).intersection(set(wire2_path))
    cross_points.remove((0,0))
    return cross_points, wire1_path, wire2_path

def closest_cross(wire1, wire2):
    cross_points, _, _ = find_cross_points(wire1, wire2)
    sorted_points = list(cross_points)    
    sorted_points.sort(key = manhattan)
    return manhattan(sorted_points[0])

assert(closest_cross('R8,U5,L5,D3', 'U7,R6,D4,L4') == 6)    
assert(closest_cross('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 159)
assert(closest_cross('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 135)

# Part 1
with open('input.txt', 'r') as f:
    wires = f.readlines()
print('Part 1:', closest_cross(wires[0], wires[1]))

# Part 2

def position_delay(wire_path):
    pos_to_delay = {}
    for i, p in enumerate(wire_path):
        if not p in pos_to_delay:
            pos_to_delay[p] = i
    return pos_to_delay

def lowest_delay(wire1, wire2):
    cross_points, wire1_path, wire2_path = find_cross_points(wire1, wire2)
    wire1_signal_delay = position_delay(wire1_path)
    wire2_signal_delay = position_delay(wire2_path)
    sorted_points = list(cross_points)    
    sorted_points.sort(key = lambda p: wire1_signal_delay[p] + wire2_signal_delay[p])
    best_point = sorted_points[0]
    d1 = wire1_signal_delay[best_point]
    d2 = wire2_signal_delay[best_point]
    print(best_point, d1, d2, 'total:', d1+d2)
    return  d1+d2

assert(lowest_delay('R8,U5,L5,D3', 'U7,R6,D4,L4') == 30)
assert(lowest_delay('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 610)
assert(lowest_delay('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 410)

print('Part 2:', lowest_delay(wires[0], wires[1]))

