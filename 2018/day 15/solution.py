# Advent of code - 2018
# Day 15
#
# Pieter Kitslaar
#

import numpy as np
from collections import deque

EMPTY  = 0
WALL   = -2 
ELF    = 1 
GOBLIN = 2 

# some defines
BLOCKED = -2
FRONT = -1
EMPTY = 0

CHAR_TABLE = {
    '.': EMPTY,
    '#': WALL,
    'E': ELF,
    'G': GOBLIN,
}

VALUE_TABLE = {v:k for k,v in CHAR_TABLE.items()}

class NoMoreEnemies(Exception):
    pass

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
            (-1, 0),
            ( 1, 0),
            ( 0, 1),
            ( 0,-1)
        ]
        neighbours_y = [] 
        neighbours_x = [] 
        for offset_x, offset_y in offsets:
            if 0 <= center_x+offset_x < shape[1] and 0 <= center_y+offset_y < shape[0]:
                neighbours_y.append(center_y+offset_y)
                neighbours_x.append(center_x+offset_x)
        return GridCoords(shape, (np.array(neighbours_y), np.array(neighbours_x)))


class Map(object):

    def __init__(self):
        grid = np.zeros(0)
        units = {}

    def units_array(self, encode='type', include_dead = False):
        units_array = np.zeros_like(self.grid)
        for unit in self.units.values():
            y,x = unit['pos']
            if include_dead or unit['hp'] > 0:
                units_array[y][x] = unit[encode]
        return units_array

    def filled_grid(self):
        return self.grid + self.units_array()

    def to_txt(self, array = None):
        if array is None:
            array = self.filled_grid()
        txt_data = []
        for r in array:
           row_text = ''.join(VALUE_TABLE[v] for v in r) 
           txt_data.append(row_text)
        return '\n'.join(txt_data)

    def current_units_array(self):
        return self.units_array(encode = 'id')

    def get_neighbour_positions(self, y, x):
        return GridCoords.neighborhood(self.grid.shape, y, x)

    def attack(self, attacker_id, target_id):
        attacker = self.units[attacker_id]
        target = self.units[target_id]
        target['hp'] -= attacker['attack']
        if target['hp'] <= 0:
            #print(target_id, 'died')
            return True

    def wave_prop(self, speed_map, start_pos):
        accepted = np.zeros_like(speed_map)
        accepted[speed_map != EMPTY] = BLOCKED
        wave_front = deque([(1, start_pos)])
        while wave_front:
            # accept fastest in wave_front
            current = wave_front.popleft()
            c_steps = current[0]
            c_y, c_x = current[1]
            accepted[c_y][c_x] = c_steps

            current_nh = self.get_neighbour_positions(c_y, c_x)
            empty = current_nh.get_values(accepted) == EMPTY
            if np.any(empty):
                new_front_coords = current_nh.filter(empty)
                for f_y, f_x in new_front_coords.as_tuples():
                    steps  = c_steps+1 
                    wave_front.append((steps, (f_y, f_x)))
                    accepted[f_y][f_x] = FRONT
        return accepted


    def attack_in_neighborhood(self, unit_id, units_array_2d):
        # info on current unit
        current_unit = self.units[unit_id]
        c_type = current_unit['type']
        c_y, c_x = current_unit['pos']

        # check current nh
        current_nh = self.get_neighbour_positions(c_y, c_x)
        current_nh_types = current_nh.get_values(units_array_2d)
        units_in_nh = current_nh_types > EMPTY
        if np.any(units_in_nh):
            unit_ids = current_nh.filter(units_in_nh).get_values(units_array_2d)
            enemy_ids = [u_id for u_id in unit_ids if self.units[u_id]['type'] != c_type]
            if enemy_ids:
                # found enemy in neighbourhoud
                enemy_info = [self.units[enemy_id] for enemy_id in enemy_ids]
                enemy_info.sort(key = lambda i: (i['hp'],i['pos']))
                selected_enemy_info = enemy_info[0]
                enemy_died = self.attack(unit_id, selected_enemy_info['id'])
                if enemy_died:
                    s_y, s_x = selected_enemy_info['pos']
                    units_array_2d[s_y][s_x] = EMPTY # clear map
                return selected_enemy_info

    def turn(self, unit_id, units_array_2d):
        # create combined map
        combined_map = self.grid + units_array_2d

        if self.attack_in_neighborhood(unit_id, units_array_2d):
            return

        current_unit = self.units[unit_id]
        c_type = current_unit['type']
        c_y, c_x = current_unit['pos']

        # no direct target find closest and move to it
        targets = [v for u_id, v in self.units.items() if v['type'] != c_type and v['hp'] > 0]
        if not targets:
            # no more targets left
            raise NoMoreEnemies()

        # find targets (in range)
        in_range_positions = [] 
        for target in targets:
            y, x = target['pos']
            target_nh = self.get_neighbour_positions(y, x)
            nh_types = target_nh.get_values(combined_map)
            empty_nh = nh_types == EMPTY
            if np.any(empty_nh):
                empty_coords = target_nh.filter(empty_nh)
                in_range_positions.append(empty_coords)

        if not in_range_positions:
            return

        in_range = GridCoords.combine(*in_range_positions)

        # propagate
        accepted = self.wave_prop(combined_map, current_unit['pos'])
        not_blocked = in_range.get_values(accepted) > EMPTY
        if not np.any(not_blocked):
            return

        reachable = in_range.filter(not_blocked)
        num_steps = reachable.get_values(accepted)

        combined = [tuple(t.tolist()) for t in np.vstack([num_steps, reachable.Y(), reachable.X()]).T]
        combined.sort()
        chosen = combined[0]
        chosen_pos = chosen[1:]
        backtracks = self.backtrack(chosen_pos, accepted)

        next_moves = [bt[-1] for bt in backtracks]
        next_moves.sort()
        next_position = next_moves[0]

        current_unit['pos'] = next_position
        units_array_2d[c_y][c_x] = EMPTY
        units_array_2d[next_position[0]][next_position[1]] = unit_id

        return self.attack_in_neighborhood(unit_id, units_array_2d)
        

    def backtrack(self, chosen_pos, accepted):
        visited = np.zeros_like(accepted)
        search_tracks = [[chosen_pos]]
        complete_tracks = []
        while search_tracks:
            new_tracks = []
            for t in search_tracks:
                search_y, search_x = t[-1]
                search_pos_step = accepted[search_y][search_x]

                search_nh = self.get_neighbour_positions(search_y, search_x)
                next_options = np.logical_and(
                        search_nh.get_values(visited) == EMPTY,
                        search_nh.get_values(accepted) == (search_pos_step - 1)
                )
                next_positions = list(search_nh.filter(next_options).as_tuples())
                if next_positions:
                    pos_iter = 0
                    for i, next_p in enumerate(next_positions):
                        if i == 0:
                            next_t = t 
                        else:
                            next_t = t[:] # copy current if more positions
                        if accepted[next_p[0]][next_p[1]] == 1:
                            complete_tracks.append(next_t)
                            search_tracks.remove(next_t)
                        else:
                            next_t.append(next_p)
                            visited[next_p[0]][next_p[1]] = 1

                        if i > 0:
                            new_tracks.append(next_t)
                else:
                    # track is dead end
                    search_tracks.remove(t)

            search_tracks.extend(new_tracks)
        return complete_tracks

    def round(self):
        units_array_2d = self.current_units_array()
        units_flat = units_array_2d.flat
        units_order = units_flat[np.nonzero(units_flat)]
        for unit_id in units_order:
            if self.units[unit_id]['hp'] > 0:
                self.turn(unit_id, units_array_2d)

    def __str__(self):
        return self.to_txt()

    @staticmethod
    def read(txt_data, last_column = None):
        units = {}
        grid = []
        for y, l in enumerate(txt_data.splitlines()):
            grid.append([])
            row = grid[-1]
            for x, c in enumerate(l.strip()):
                if last_column and x > last_column:
                    break
                if c in 'EG':
                    units_id = len(units)+1
                    units[units_id] = {
                        'id': units_id,
                        'type': CHAR_TABLE[c],
                        'hp': 200,
                        'attack': 3,
                        'pos': (y,x),
                    }
                    c = '.' 
                row.append(CHAR_TABLE[c])

        m = Map()
        m.units = units
        m.grid = np.array(grid)
        return m

def battle(input_data, last_column = None, init_map_callback = None, check_map_callback = None):
    """Start battle from input data and return the outcome of the battle."""
    m = Map.read(input_data, last_column)
    if init_map_callback:
        init_map_callback(m)
    try:
        r= 0
        while True:
            m.round()
            r += 1
            if check_map_callback:
                check_map_callback(m)

    except NoMoreEnemies:
        if check_map_callback:
            check_map_callback(m)

        alive = [u for u in m.units.values() if u['hp'] > 0]
        summed = sum([a['hp'] for a in alive]) 
        outcome = r*summed
        return outcome

def battle_test(outcome, *args, **kwargs):
    if run_tests:
        assert(outcome == battle(*args, **kwargs))

class ElvesDied(Exception):
    pass

class ElvesChecker(object):
    def __init__(self, attack):
        self.map = None
        self.attack = attack
        self.num_initial_elves = 0

    def setup(self, m):
        self.map = m
        elves = [u for u in m.units.values() if u['type'] == ELF]
        for e in elves:
            e['attack'] = self.attack
        self.num_initial_elves = len(elves)

    def check(self, m):
        elves = [u for u in m.units.values() if u['type'] == ELF and u['hp'] > 0]
        if len(elves) < self.num_initial_elves:
            raise ElvesDied()

def powerup_elves(d, last_column = None):
    """Perform binary search to find optimal attack value for Elves."""
    lower, upper = [0, 50] 
    results = {
        lower: (0, None),
        upper: (1, None),
    }
    iteration = 0
    while upper-lower > 1:
        iteration += 1
        mid_point = (lower + upper)//2
        mid_result = battle_attack(d, last_column, mid_point)
        success = 1 if mid_result else 0
        results[mid_point] = (success, mid_result)
        if success == 0:
            lower = mid_point
        else:
            upper = mid_point
    print('Took', iteration, 'iterations. Attack power is', upper)
    return results[upper][-1]

def battle_attack(d, last_column, attack):
    checker = ElvesChecker(attack)
    try:
        result = battle(d, 
            last_column = last_column,
            init_map_callback = checker.setup,
            check_map_callback = checker.check)
        return result, checker
    except ElvesDied:
        pass

def powerup_test(outcome, data, last_column):
    if run_tests:
        result, checker = powerup_elves(data, last_column)
        if not outcome == result:
            print(checker.map)
            raise ValueError(f'result {result} not equal to {outcome}')

        
run_tests = True
debug = False

battle_test(27730, ("""\
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######
"""))

battle_test(36334, """\
#######       #######
#G..#E#       #...#E#   E(200)
#E#E.E#       #E#...#   E(197)
#G.##.#  -->  #.E##.#   E(185)
#...#E#       #E..#E#   E(200), E(200)
#...E.#       #.....#
#######       #######
""", 6)

battle_test(39514, """\
#######       #######   
#E..EG#       #.E.E.#   E(164), E(197)
#.#G.E#       #.#E..#   E(200)
#E.##E#  -->  #E.##.#   E(98)
#G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#   
#######       #######   
""", 6)


battle_test(27755, """\
#######       #######   
#E.G#.#       #G.G#.#   G(200), G(98)
#.#G..#       #.#G..#   G(200)
#G.#.G#  -->  #..#..#   
#G..#.#       #...#G#   G(95)
#...E.#       #...G.#   G(200)
#######       #######  
""", 6)


battle_test(28944, """\
#######       #######   
#.E...#       #.....#   
#.#..G#       #.#G..#   G(200)
#.###.#  -->  #.###.#   
#E#G#G#       #.#.#.#   
#...#G#       #G.G#G#   G(98), G(38), G(200)
#######       ####### 
""", 6)

battle_test(18740, """\
#########       #########   
#G......#       #.G.....#   G(137)
#.E.#...#       #G.G#...#   G(200), G(200)
#..##..G#       #.G##...#   G(200)
#...##..#  -->  #...##..#   
#...#...#       #.G.#...#   G(200)
#.G...G.#       #.......#   
#.....G.#       #.......#   
#########       #########   
""", 7)


with open('input.txt') as f:
    input_data = f.read()

print('PART 1: outcome is', battle(input_data))


powerup_test(4988, """\
#######       #######
#.G...#       #..E..#   E(158)
#...EG#       #...E.#   E(14)
#.#.#G#  -->  #.#.#.#
#..G#E#       #...#.#
#.....#       #.....#
#######       #######
""", 6)

powerup_test(1140, """\
#########       #########   
#G......#       #.......#   
#.E.#...#       #.E.#...#   E(38)
#..##..G#       #..##...#   
#...##..#  -->  #...##..#   
#...#...#       #...#...#   
#.G...G.#       #.......#   
#.....G.#       #.......#   
#########       #########  
""", 8)

print('Starting part 2....')
print('PART 2: outcome is', powerup_elves(input_data)[0])

