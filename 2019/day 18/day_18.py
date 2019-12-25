from pathlib import Path
import networkx as nx
from matplotlib import pyplot as plt
import itertools
import heapq
from dataclasses import dataclass

def parse_map(map_txt):
    g = nx.Graph()
    splitted = map_txt.splitlines()
    height = len(splitted)
    width = len(splitted[0])
    items = {}
    node_labels = {}
    for y, r in enumerate(splitted):
        for x, c in enumerate(r):
            if c != '#':
                g.add_node((x,y))
                if x > 0 and splitted[y][x-1] != '#':
                    g.add_edge((x-1,y), (x,y))
                if y > 0 and splitted[y-1][x] != '#':
                    g.add_edge((x,y-1), (x,y))
                if c == '@':
                    items.setdefault('start_positions', []).append((x,y))
                    node_labels[(x,y)] = '@'
                elif c.isalpha():
                    if c.islower():
                        items.setdefault('keys', []).append((x,y))
                        node_labels[(x,y)] = c
                    else:
                        items.setdefault('doors', []).append((x,y))
                        node_labels[(x,y)] = c
    #nx.draw(g, pos={n:n for n in g.nodes()}, labels=node_labels, with_labels=True)
    #plt.show()
    items['node_values'] = node_labels
    return g, items

@dataclass(order=True)
class State:
    remaining_keys: set
    found_keys: list
    key_set: tuple
    current_positions: list
    routes: list
    total_steps: int


def collect_all_keys(g, items):
    node_values = items['node_values']
    key_to_pos = {node_values[p]:p for p in items['keys']}
    door_to_pos = {node_values[p]:p for p in items['doors']}

    states_to_explore = [
        (0, 
            State(
                # global state
                remaining_keys = set(items['keys']),
                found_keys = [],
                key_set = None,
                # per robot state
                current_positions = items['start_positions'],
                routes = [[] for _ in range(len(items['start_positions']))],
                total_steps = 0,
            )
        )
    ]

    print('Computing info...')
    p2p = {kp:nx.single_source_dijkstra_path(g, kp) for kp in set(items['keys'])}
    for sp in items['start_positions']:
        p2p[sp] = nx.single_source_dijkstra_path(g,sp)
    completed_states = []
    fastest_per_keys = {}
    while states_to_explore:
        print(len(states_to_explore))
        current_states = states_to_explore[:]
        heapq.heapify(current_states)
        states_to_explore.clear()
        while current_states:
            efficiency, state = heapq.heappop(current_states)
            if len(state.found_keys) > 1:
                key_set = state.key_set
                if key_set:
                    current_fastest = fastest_per_keys.get(key_set)
                    if current_fastest is not None:
                        if state.total_steps > current_fastest:
                            #print('skipping', state['found_keys'], state['key_set'], state['total_steps'], current_fastest)
                            continue # skip this state

            #print('using', state['found_keys'], state['key_set'], state['total_steps'])
            if len(state.remaining_keys) < 1:
                completed_states.append(state)
            else:
                possible_next_paths_per_robot = []
                for i_robot, current_pos in enumerate(state.current_positions):
                    possible_next_paths_per_robot.append([])
                    possible_next_paths = possible_next_paths_per_robot[i_robot]
                    for kp in state.remaining_keys:
                        path = p2p[current_pos].get(kp, [])[1:]
                        if path:
                            reachable = True
                            path_items = {p:node_values[p] for p in path if p in node_values}
                            test_keys = set(state.found_keys)
                            for pi in path_items.values():
                                if pi.islower():
                                    test_keys.add(pi)
                                if pi.isupper() and pi.lower() not in test_keys:
                                    reachable = False
                                    break
                            if reachable:
                                possible_next_paths.append((len(path), path, path_items))
                    if not possible_next_paths:
                        possible_next_paths.append(None) # place holder to indicate no path found  
                    #min_path_lenghts = min([p[0] for p in possible_next_paths])
                    #possible_next_paths = [p for p in possible_next_paths if p[0] == min_path_lenghts] 
                for pnp_group in itertools.product(*possible_next_paths_per_robot):
                    # make copy of current state
                    new_state_found_keys = state.found_keys[:]
                    new_state_remaining_keys = set(state.remaining_keys)
                    new_state_routes = [r[:] for r in state.routes]
                    new_state_positions = [cp for cp in state.current_positions]
                    
                    num_found_keys = 0
                    for i_robot, pnp in enumerate(pnp_group):
                        if pnp is not None:
                            pnp_len, pnp_path, pnp_items = pnp                    
                            for p, k in pnp_items.items():
                                if k.islower():
                                    if p in new_state_remaining_keys:
                                        new_state_found_keys.append(k)
                                        new_state_remaining_keys.remove(p)
                                        num_found_keys += 1
                            new_state_routes[i_robot].extend(pnp_path)
                            new_state_positions[i_robot] = pnp_path[-1]

                    
                    total_route_length = sum([len(r) for r in new_state_routes])
                    key_set = tuple([tuple(sorted(new_state_found_keys[:-1])), new_state_found_keys[-1]])
                        
                    current_fastest = fastest_per_keys.get(key_set)
                    if (current_fastest is None) or (total_route_length < current_fastest):
                        fastest_per_keys[key_set] = total_route_length

                        states_to_explore.append((total_route_length/len(new_state_found_keys), State(
                            remaining_keys = new_state_remaining_keys,
                            found_keys = new_state_found_keys,
                            current_positions = new_state_positions,
                            routes = new_state_routes,
                            total_steps = total_route_length,
                            key_set = key_set,
                        )))
                        #else:
                    #    print(key_set, new_state_found_keys, route_length, current_fastest)
    #print(fastest_per_keys[tuple(sorted(key_to_pos))])
    print(len(completed_states))
    return completed_states
    
def solution_part1(map_txt, draw=False):
    g, items = parse_map(map_txt)
    if draw:
        nx.draw(g, 
            pos={n:(n[0],-n[1]) for n in g.nodes()}, 
            with_labels=True,
            labels={n:items['node_values'].get(n,'') for n in g.nodes()})
        plt.show()
    all_solutions = collect_all_keys(g, items)
    solution_steps = [solution.total_steps for solution in all_solutions]
    min_steps = min(solution_steps)  
    return min_steps  

ex1 = """\
#########
#b.A.@.a#
#########"""

def test_ex1():    
    assert(8 == solution_part1(ex1))

ex_larger = """\
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

def test_ex_larger():        
    assert(86 == solution_part1(ex_larger))

ex_2 = """\
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""

def test_ex_2():        
    assert(132 == solution_part1(ex_2))

ex_3 = """\
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

def test_ex_3():        
    assert(136 == solution_part1(ex_3))


ex_4 = """\
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

def test_ex_4():        
    assert(81 == solution_part1(ex_4))


ex_part2_original="""\
#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######"""

ex_part2_filled="""\
#######
#a.#Cd#
##@#@##
#######
##@#@##
#cB#Ab#
#######"""

def test_entrace_update():
    updated = update_entraces(ex_part2_original)
    assert(updated == ex_part2_filled)

def test_part2_ex1():
    part2_ex1_filled = update_entraces(ex_part2_original)
    part2_ex1_sol = solution_part1(part2_ex1_filled)
    assert(8 == part2_ex1_sol)

part2_ex2 = """\
###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############"""

def test_part2_ex2():
    part2_ex2_sol = solution_part1(part2_ex2)
    assert(24 == part2_ex2_sol)

part2_ex3 = """\
#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############"""

def test_part2_ex3():
    part2_ex3_sol = solution_part1(part2_ex3)
    assert(32 == part2_ex3_sol)

part2_ex4 = """\
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""

def test_part2_ex4():
    part2_ex4_sol = solution_part1(part2_ex4)
    assert(72 == part2_ex4_sol)

def find_entrance(grid):
    for y,r in enumerate(grid):
        for x,c in enumerate(r):
            if c == '@':
                return (x,y)

def update_entraces(map_txt):
    grid = [list(r) for r in map_txt.strip().splitlines()]
    x,y = find_entrance(grid)
    grid[y-1][x-1:x+2] = '@#@'
    grid[y  ][x-1:x+2] = '###'
    grid[y+1][x-1:x+2] = '@#@'
    return '\n'.join([''.join(r) for r in grid])

def main():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_txt = f.read().strip()
    part1_solution = solution_part1(main_txt)
    print('Part 1:', part1_solution)
    assert(4620 == part1_solution)

    updated_main_txt = update_entraces(main_txt)
    part2_solution = solution_part1(updated_main_txt)
    print('Part 2:', part2_solution)

if __name__ == "__main__":
    main()
    
