import sys
from pathlib import Path
d5_dir = Path(__file__).resolve().parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))
from day_05 import run, txt_values

import networkx as nx
from matplotlib import pyplot as plt
from collections import Counter
from itertools import groupby

NORTH, SOUTH, EAST, WEST = range(4)
STEP = {
    NORTH: ( 0, 1),
    SOUTH: ( 0,-1),
    WEST:  (-1, 0),
    EAST:  ( 1, 0)
}
INTERSECTION, CORNER, END_POINT = range(3)

def lines_to_view(camera_view_lines):
    camera_view = [list(r) for r in camera_view_lines if r.strip()]
    return camera_view

def print_view(camera_view):
    for r in camera_view:
            print("".join(r))

def get_neighbors(camera_view, x, y):
    height = len(camera_view)
    width  = len(camera_view[0])

    neighbors = {}
    if x > 0:
        neighbors[WEST] = camera_view[y][x-1]
    if x+1 < width:
        neighbors[EAST] = camera_view[y][x+1]
    if y > 0:
        neighbors[SOUTH] = camera_view[y-1][x]
    if (y+1) < height:
        neighbors[NORTH] = camera_view[y+1][x]
    return neighbors

def plan_route(camera_view):
    _, start_pos = find_nodes(camera_view)
    
    path = []
    next_node = start_pos
    while next_node:
        current_pos = next_node
        path.append(current_pos)
        next_node = None

        neighbor_steps = [STEP[d] for d,v in get_neighbors(camera_view, current_pos[0], current_pos[1]).items() if v=='#']
        neighbor_options = [(current_pos[0]+s[0], current_pos[1]+s[1]) for s in neighbor_steps]
        if len(path) > 1:
            neighbor_options = [p for p in neighbor_options if p != path[-2]] # dont turn around
        if neighbor_options:
            if len(neighbor_options) > 1:
                prev_step = (path[-1][0] - path[-2][0], path[-1][1] - path[-2][1])
                for no in neighbor_options:
                    new_step = (no[0] - path[-1][0], no[1] - path[-1][1])
                    if new_step == prev_step:
                        next_node = no
                assert(next_node)
            else:
                next_node = neighbor_options[0]
    return path

DIR_TO_STEP = {
    '^': ( 0,-1),
    'v': ( 0, 1),
    '<': (-1, 0),
    '>': ( 1, 0),
}
STEP_TO_DIR = {v:k for k,v in DIR_TO_STEP.items()}

DIR_CHANGE = {
    ('^','>'): 'R',
    ('^','<'): 'L',
    ('>','^'): 'L',
    ('>','v'): 'R',
    ('v','<'): 'R',
    ('v','>'): 'L',
    ('<','^'): 'R',
    ('<','v'): 'L',
}

def route_instructions(camera_view, route):
    prev_pos = route[0]
    prev_dir = camera_view[prev_pos[1]][prev_pos[0]]
    
    assert(prev_dir in ('^','v','<','>'))
    instructions = []
    for (x,y) in route[1:]:
        new_step = x-prev_pos[0], y-prev_pos[1]
        prev_step = DIR_TO_STEP[prev_dir]
        if new_step == prev_step:
            instructions[-1] += 1
        else:
            new_dir = STEP_TO_DIR[new_step]
            #print(x,y,prev_dir, new_dir)
            dir_change_instruction = DIR_CHANGE[(prev_dir, new_dir)]
            instructions.append(dir_change_instruction)
            instructions.append(1)
            prev_dir = new_dir
        prev_pos = (x,y)

    return list(map(str, instructions))



def print_route(camera_view, path):
    height = len(camera_view)
    width = len(camera_view[0])
    grid = [['   ' for _ in range(width)] for _ in range(height)]
    for i, (x,y) in enumerate(path):
        grid[y][x] = "{0:^3}".format(i)
    #for r in grid:
    #    print(''.join(r))
            

def find_nodes(camera_view):
    height = len(camera_view)
    width  = len(camera_view[0])

    nodes = {}
    start_pos = None
    for y in range(height):
        for x in range(width):
            v = camera_view[y][x]
            if v in ('^','v','<','>'):
                start_pos = (x,y)
                nodes[(x,y)] = END_POINT
            if v == '#':
                neighbors = get_neighbors(camera_view, x, y)
                neighbor_counts = Counter(neighbors.values())
                if neighbor_counts['#'] > 2:
                    nodes[(x,y)] = INTERSECTION
                elif neighbor_counts['#'] == 1 and neighbor_counts.get('.', 0) == len(neighbors)-1:
                    nodes[(x,y)] = END_POINT
                elif neighbor_counts['#'] == 2:
                    if neighbors.get(NORTH) == neighbors.get(SOUTH) or neighbors.get(WEST) == neighbors.get(EAST): 
                        pass
                    else:
                        nodes[(x,y)] = CORNER
    return nodes, start_pos


def compute_alignment(intersections):
    return sum(x*y for x,y in intersections)

example = """\
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^.."""

def test_example():
    ex_view = lines_to_view(example.splitlines())
    ex_nodes, _ = find_nodes(ex_view)
    ex_alignment = compute_alignment([pos for pos,n_type in ex_nodes.items() if n_type == INTERSECTION])
    assert(76 == ex_alignment)

ex2 = """\
#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......"""

import itertools

def test_example2():
    ex2_view = lines_to_view(ex2.splitlines())
    nodes, _ = find_nodes(ex2_view)
    route = plan_route(ex2_view)
    print_route(ex2_view, route)

    ex2_long_instruct_gt = 'R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2'
    ex2_route_instructions = route_instructions(ex2_view, route)
    ex2_long_instruct = ','.join(ex2_route_instructions)
    assert(ex2_long_instruct_gt == ex2_long_instruct)
    ex2_grouped = group_instructions(ex2_route_instructions)
    for sol in find_group_subset(ex2_route_instructions, ex2_grouped):
        reconstructed_route = []
        for f_name in sol['main_routine']:
            reconstructed_route.extend(sol['functions'][f_name])
        assert(reconstructed_route == ex2_route_instructions)

def group_instructions(route_instructions):
    #print(route_instructions)
    groups = {}
    for offset in range(0,len(route_instructions),2):
        equal = [p[0]==p[1] for p in zip(route_instructions, route_instructions[offset:])]
        for k,g_iter in groupby(enumerate(equal), key = lambda t: t[1]):
            g = list(g_iter)
            if k and len(g) > 2 and len(g) % 2 == 0: 
                g1 = tuple([t[0] for t in g])
                g2 = tuple([t[0]+offset for t in g])
                if g1[0] % 2 == 0:
                    if not set(g1).intersection(set(g2)): # should not be any overlap
                        group_chars = tuple([route_instructions[i] for i in g1])
                        #print(offset, group_chars)
                        for group_offset in range(0,len(group_chars),2):
                            for d in (1,-1):
                                if group_offset > 0:
                                    sl = slice(group_offset, None) if d > 0 else slice(0,-group_offset)
                                else:
                                    sl = slice(None)
                                this_chars = group_chars[sl]
                                if this_chars:
                                    this_g1 = g1[sl]
                                    this_g2 = g2[sl]
                                    #print('this_chars', sl, d, group_offset, this_chars, this_g1, this_g2)
                                    g_value = groups.setdefault(this_chars, set())
                                    g_value.add(this_g1)
                                    g_value.add(this_g2)

    sorted_groups = list(sorted(groups.items(), key = lambda t: len(t[0])*len(t[1]), reverse=True))
    return sorted_groups


def find_group_subset(route_instructions, sorted_groups):
    all_indices_in_route = set(range(len(route_instructions)))
    for sub_set in itertools.combinations(sorted_groups, 3):
        
        all_indices = []
        complete_indices = set()
        functions = {}
        for i, (g, indices) in zip('ABC',sub_set):
            functions[i] = g
            for ind in indices:
                all_indices.append((i, ind))
                complete_indices.update(ind)

        if complete_indices == all_indices_in_route:
            remaining = set(range(len(route_instructions)))
            gr_to_use = []
            found_group = True
            while found_group:
                found_group = False
                for g, ind in all_indices:
                    if len(remaining.intersection(ind)) == len(ind):
                        remaining.difference_update(ind)
                        gr_to_use.append((g, ind))
            if not remaining:
                sorted_functions = list(sorted(gr_to_use, key = lambda t: t[1][0]))
                yield {'main_routine': [t[0] for t in sorted_functions], 'main_routine_details': sorted_functions, 'functions': functions}

def main():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
            main_program = txt_values(f.read().strip())
    current_pos, values, outputs = run(main_program, stop_on_output=False)
    camera_view_lines = ''.join(chr(v) for v in outputs).splitlines()
    camera_view = lines_to_view(camera_view_lines)
    print_view(camera_view)
    nodes, _ = find_nodes(camera_view)
    end_nodes = [pos for pos, n_type in nodes.items() if n_type == END_POINT]
    print('Number end_points', len(end_nodes))
    alignment = compute_alignment([pos for pos, n_type in nodes.items() if n_type == INTERSECTION])
    print('Part 1:', alignment)
    assert(5620 == alignment)

    
    main_route = plan_route(camera_view)
    main_instructions = route_instructions(camera_view, main_route)
    main_grouped  = group_instructions(main_instructions)
    all_solutions = list(find_group_subset(main_instructions, main_grouped))
    main_solution = all_solutions[0]

    reconstructed_route = []
    for f_name in main_solution['main_routine']:
        reconstructed_route.extend(main_solution['functions'][f_name])
    assert(reconstructed_route == main_instructions)
    
    ascii_instructions = [
        list(map(ord, ','.join(main_solution['main_routine'])+'\n')),   # Main routine
        list(map(ord, ','.join(main_solution['functions']['A'])+'\n')), # Function A
        list(map(ord, ','.join(main_solution['functions']['B'])+'\n')), # Function B
        list(map(ord, ','.join(main_solution['functions']['C'])+'\n')), # Function C
        list(map(ord, 'n\n')), # set to 'y' for live camera feed, or 'n' if no feed
    ] 
    
    # construct input function for IntCode machine
    def feed_instructions():
        i = itertools.chain(*ascii_instructions)
        def get_v():
            v = next(i)
            return v
        return get_v

    main_program[0] = 2 # activate program
    current_pos, values, outputs = run(main_program, input_v=feed_instructions(), stop_on_output=False)
    part2_sol = outputs[-1]
    print('Part 2:', part2_sol)
    assert(part2_sol ==  768115)

if __name__ == "__main__":
    test_example2()
    main()