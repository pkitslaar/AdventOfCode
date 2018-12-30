# Advent of code - 2018
#
# Day 20
#
# Pieter Kitslaar
#

import numpy as np
from collections import defaultdict, deque
import heapq

DIRECTIONS = {
    # Syntax CHAR: step (y,x), door CHAR, wall offsets
    'E': (( 0, 1), '|', [( 1,0), (-1, 0)]),
    'W': (( 0,-1), '|', [( 1,0), (-1, 0)]),
    'N': ((-1, 0), '-', [( 0,1), ( 0,-1)]),
    'S': (( 1, 0), '-', [( 0,1), ( 0,-1)]),
}

# some defines
BLOCKED = -2
FRONT = -1
EMPTY = 0

WALL = -2
UNKNOWN = -3
START_POS = -5
DOOR_NS = 3
DOOR_EW = 2
CORRIDOR = 1

# character to value in grid
CHAR_TABLE = {
    '.': CORRIDOR,
    '-': DOOR_NS,
    '|': DOOR_EW,
    '#': WALL,
    'X': START_POS,
    '?': UNKNOWN,
}

# grid to character
VALUE_TABLE = {v:k for k,v in CHAR_TABLE.items()}
VALUE_TABLE[EMPTY] = ' '

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


class WaveProp(object):
    def __init__(self):
        pass

    def backtrack(self, chosen_pos, accepted):
        visited = np.zeros_like(accepted)
        search_tracks = [[chosen_pos]]
        complete_tracks = []
        while search_tracks:
            new_tracks = []
            for t in search_tracks:
                search_y, search_x = t[-1]
                search_pos_step = accepted[search_y][search_x]

                search_nh = GridCoords.neighborhood(accepted.shape, search_y, search_x)
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
        
    def propagate(self, speed_map, start_pos):
        accepted = np.zeros_like(speed_map)
        accepted[speed_map != EMPTY] = BLOCKED
        wave_front = [(1, start_pos)]
        heapq.heapify(wave_front)
        while wave_front:
            # accept fastest in wave_front
            current = heapq.heappop(wave_front)
            c_steps = current[0]
            c_y, c_x = current[1]
            accepted[c_y][c_x] = c_steps

            current_nh = GridCoords.neighborhood(accepted.shape, c_y, c_x)
            empty = current_nh.get_values(accepted) == EMPTY
            if np.any(empty):
                new_front_coords = current_nh.filter(empty)
                for f_y, f_x in new_front_coords.as_tuples():
                    steps  = c_steps+1 
                    heapq.heappush(wave_front, (steps, (f_y, f_x)))
                    accepted[f_y][f_x] = FRONT
        assert(np.sum(accepted == FRONT) == 0)
        return accepted    


class Map(object):

    def __init__(self):
        self.all_maps = []

    def get_map_bounds(self, m):
        y_max = max(m) if m else 0
        y_min = min(m) if m else 0
        x_max = max([max(r) for r in m.values()] + [0])
        x_min = min([min(r) for r in m.values()] + [1])
        return y_min, y_max, x_min, x_max 
    
    def get_bounds(self):
        y_min, y_max, x_max, x_min = 0,0,0,0
        for m in self.all_maps.values():
            bounds = self.get_map_bounds(m['map'])
            y_offsets = [o[0] for o in m['offsets']]
            x_offsets = [o[1] for o in m['offsets']]
            y_min = min([y_min, bounds[0] + min(y_offsets)])
            y_max = max([y_max, bounds[1] + max(y_offsets)])
            x_min = min([x_min, bounds[2] + min(x_offsets)])
            x_max = max([x_max, bounds[3] + max(x_offsets)])
        return y_min, y_max, x_min, x_max
            

    def to_grid(self):
        y_min, y_max, x_min, x_max = self.get_bounds()
        y_width = (y_max - y_min)+1
        x_width = (x_max - x_min)+1

        grid = np.zeros((y_width, x_width))
        for m in self.all_maps.values():
            for y_offset, x_offset in m['offsets']:
                for y, r in m['map'].items():
                    mod_y = y + y_offset - y_min
                    for x, v in r.items():
                        mod_x = x + x_offset - x_min
                        current_value = grid[mod_y][mod_x]
                        if (current_value in (EMPTY, UNKNOWN)):
                            #print(f'Settings {mod_y} {mod_x} with value {v} but already has value {VALUE_TABLE[current_value]}')
                            #if current_value == EMPTY or current_value == UNKNOWN:
                            grid[mod_y][mod_x] = CHAR_TABLE[v]
                            
        grid[grid == UNKNOWN] = WALL
        return grid, (abs(y_min), abs(x_min))
        
    def bracket_gen(self, regexp):
        brackets = []
        for c in regexp:
            if c == '(':
                brackets.append(c)
            if c == ')':
                brackets.pop()
            yield c, len(brackets)
    
    def split_group(self, regexp):
        FIRST, MIDDLE, LAST = range(3)
        parts = [[] for i in range(3)]
        current = FIRST
        for c, bracket_depth in self.bracket_gen(regexp):
            if bracket_depth == 0:
                if current == MIDDLE:
                    current = LAST
                    continue
            elif bracket_depth == 1:
                if current == FIRST:
                    current = MIDDLE
                    continue
            parts[current].append(c)
            
        first = ''.join(parts[FIRST]).strip()
        middle = ''.join(parts[MIDDLE]).strip()
        last = ''.join(parts[LAST]).strip()
        return first, middle, last
        
    def split_branch(self, regexp):
        part = []
        for c, bracket_depth in self.bracket_gen(regexp):
            if c == '|' and bracket_depth == 0:
                yield ''.join(part)
                part = []
            else:
                part.append(c)
        yield ''.join(part)
    
        
    def expand(self, parsed):
        r = parsed['route']
        if 'children' in parsed:
            for c in parsed['children']:
                for c_r in self.expand(c):
                    yield r + c_r
        else:
            yield r
    
    def parse(self, regexp, level = 0, parsed = None):
        regexp  = regexp.replace('$', '')
        if parsed is None:
            parsed = {}
        
        f, m, l = self.split_group(regexp)
        parsed['regex'] = regexp
        parsed['route'] = f
        if m:
            if m.endswith('|'):
                children = parsed.setdefault('children', [])
                
                main_group = self.parse(l, level + 1, {})
                children.append(main_group)
                
                optional_group = self.parse(m[:-1], level+1, {})
                children.append(optional_group)
                #children.append({'regex': m[:-1], 'route': m[:-1], 'children': []})
                
            else:
                for branch in self.split_branch(m):
                    if branch:
                        new_group = {'regex': branch + l}
                        parsed.setdefault('children', []).append(new_group)
                        self.parse(new_group['regex'], level +1, new_group)
        else:
            parsed['route'] = f + l
        return parsed

    def fill(self, parsed , y = 0, x = 0):
        self.all_maps = self.do_fill(parsed, y, x)
        print(len(self.all_maps))

    def do_fill(self, parsed, y, x, all_maps = None, level = 0, child_index = 0):
        if all_maps is None:
            all_maps = {}
        
        if parsed['regex'] in all_maps:
            existing_map = all_maps[parsed['regex']]
            existing_map['offsets'].append((y, x))
        else:  
            new_map = defaultdict(dict)
            all_maps[parsed['regex']] = {'offsets': [(y, x)], 'map':new_map}
            c_y, c_x = self.handle_chars(parsed['route'], 0, 0, new_map)
            
            children = parsed.get('children', [])
            for i, child in enumerate(children):
                self.do_fill(child, y+c_y, x+c_x, all_maps, level + 1, i)
        return all_maps
        
    def handle_chars(self, chars, y, x, map):
            c_y, c_x = y, x
            for i, c in enumerate(chars):
                try:
                    step, door, wall_offsets = DIRECTIONS[c]
                    for k, v in enumerate([door, '.']): 
                        c_y += step[0]
                        c_x += step[1]
                        #if c_x in map[c_y]:
                        #    c_v = map[c_y][c_x]
                        #    if c_v == 'X':
                        #        print(f'{c} At position {c_y},{c_x} already has value', c_v)
                        #        print(chars, i, c)
                        #        v = c_v
                        #                                   
                        map[c_y][c_x] = v
                        for w_o in wall_offsets:
                            w_y = c_y + w_o[0]
                            w_x = c_x + w_o[1]
                            if not w_x in map[w_y]:
                                map[w_y][w_x] = '#?'[k]
                        w_y = c_y + step[0]
                        w_x = c_x + step[1]
                        if not w_x in map[w_y]:
                            map[w_y][w_x] = '?'
                except KeyError:
                    if c == '^':
                        map[c_y][c_x] = 'X'
                    elif c == '$': 
                        pass
                    else:
                        raise ValueError(f'Unexpected characted {c}')
            return c_y, c_x
            
            
def expand(regex):
    m = Map()
    parsed  = m.parse(regex)
    return m.expand(parsed) 

def print_grid(grid, conversion = lambda v: VALUE_TABLE[v]):
    #grid = WALL*((grid != EMPTY) & (grid != START_POS))
    for r in grid:
        print(''.join(conversion(v) for v in r))

def furthest_room(regex):
    m = Map()
    print('Parsing data, size', len(regex))
    parsed = m.parse(regex)
    print('Filling map...')
    m.fill(parsed)
    print('Computing grid...')
    grid, start_pos = m.to_grid()
    print('Grid size', grid.shape)
    print_grid(grid)
    

    g_shape = grid.shape
    assert(grid[start_pos[0]][start_pos[1]] == START_POS)
    speed_map = np.ones_like(grid)*BLOCKED
    speed_map[grid == CORRIDOR] = EMPTY
    speed_map[grid == DOOR_NS] = EMPTY
    speed_map[grid == DOOR_EW] = EMPTY
    
    wave_prop = WaveProp()
    prop = wave_prop.propagate(speed_map, start_pos)
    print(1*(prop > 0))
    print( 1*(grid > EMPTY))
    print((prop > 0) != (grid > EMPTY))
    assert(np.array_equal((prop > 0),(grid > EMPTY)))
    
    #print(prop)
    
    furthest_room = np.unravel_index(np.argmax(prop), prop.shape)
    num_steps = int(prop[furthest_room])
    print(num_steps)
    
    # rooms with path through at least 1000 doors
    num_doors = (0.5*(prop-1)).astype(np.int)
    num_rooms = np.sum((num_doors >= 1000) & (grid == CORRIDOR))
    print('num rooms >1000 doors', num_rooms)
    #raise
    
    return (num_steps-1)//2

def checkEqual(expected, value, sort = True):
    s_value = list(sorted(value, key = lambda r: (len(r), r))) if sort else value
    s_expected = list(sorted(expected, key = lambda r: (len(r), r) )) if sort else expected
    if s_value != s_expected:
        if sort:
            print(len(s_value), len(s_expected), len(s_value) == len(s_expected))
            for i, (v, e) in enumerate(zip(s_value, s_expected)):
                ok = 'OK' if v == e else 'FAIL'
                print(i, 'v:', v, ok)
                print(i, 'e:', e)
        raise ValueError(f"{s_value} != {s_expected}")
        
debug = False

def tests():
    m = Map()
    splitted_branch = list(m.split_branch('EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)'))
    print(splitted_branch)
    assert(['EESS(WNSE|)SSS','WWWSSSSE(SW|NNNE)'] == splitted_branch)
    
    f, m, l = m.split_group('EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)')
    print('f:', f)
    print('m:', m)
    print('l:', l)
    assert('EESS'   == f)
    assert('WNSE|'  == m)
    assert('SSS|WWWSSSSE(SW|NNNE)'  == l)

    #checkEqual([
    #    'WNE'
    #    ], expand('WNE'))

    #checkEqual([
    #    'ENWWWNEEE',
    #    'ENWWWSSEN',
    #    'ENWWWSSEEE',
    #   ], expand('ENWWW(NEEE|SSE(EE|N))'))

    #checkEqual([
    #    'ENNWSWWSSSEENEENNN',         'ENNWSWWSSSEENEESWENNNN', 
    #    'ENNWSWWSSSEENWNSEEENNN',     'ENNWSWWSSSEENWNSEEESWENNNN', 
    #    'ENNWSWWNEWSSSSEENEENNN',     'ENNWSWWNEWSSSSEENEESWENNNN', 
    #    'ENNWSWWNEWSSSSEENWNSEEENNN', 'ENNWSWWNEWSSSSEENWNSEEESWENNNN'
    #    ], expand('ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN'))

    regexp = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
    checkEqual(23 , furthest_room(regexp), False)
    
    regexp = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
    checkEqual(31 , furthest_room(regexp), False)

tests()            

with open('input.txt') as f:
    data = f.read().strip()
print('PART 1:', furthest_room(data))
            
        
        

        
