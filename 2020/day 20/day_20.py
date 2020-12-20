"""
Advent of Code 2020 - Day 20
Pieter Kitslaar
"""

from pathlib import Path
from collections import Counter
from functools import reduce
import numpy as np
import itertools
import math
from scipy import signal

def get_input(name='input.txt'):
    with open(Path(__file__).parent / name, 'r') as f:
        return f.read()   

def array_to_id(np_a, both_ways = False):
    bin_txt = ''.join([str(v) for v in np_a])
    forward = int(bin_txt,2)
    if both_ways:
        backward = int(bin_txt[::-1],2)
        return frozenset([forward, backward])
    return forward

def permute_array(base_array):
    for num_90_rotations in range(4):
        rot_array = np.rot90(base_array, num_90_rotations)
        yield rot_array
        #self.add_permutation(rot_array)
        for np_func in (np.flipud, np.fliplr):
            flipped_array = np_func(rot_array)
            yield flipped_array
            #self.add_permutation(flipped_array)

class Tile:
    def __init__(self, tile_id, grid):
        self.tile_id = tile_id
        self.grid = grid
        
        # global (indepent of orientation)
        self.edges_set = set()
        self.unique_edges = set()

        # current edges and their direction
        self.current_permutation = 0
        self.permutations = []

    def set_permutation(self, permuation_index):
        self.current_permutation = permuation_index

    def get_permutated_edges(self, permuation_index):
        self.set_permutation(permuation_index)
        return self.get_current_edges()

    def get_current_edges(self):
        return self.permutations[self.current_permutation]['edges']

    def get_current_array(self):
        return self.permutations[self.current_permutation]['array']

    def add_permutation(self, np_a):
        self.permutations.append({'array': np_a, 'edges': self.edge_ids_for_array(np_a)})
    
    def initialize_array(self):
        grid_numbers = [[1 if c == '#' else 0 for c in r] for r in self.grid]
        array = np.array(grid_numbers)
        self.permutations = []
        for p_array in permute_array(array):
            self.add_permutation(p_array)
        self.update_edge_ids()

    def edge_ids_for_array(self, np_a):
        return dict(
            top = array_to_id(np_a[0,:]),
            left = array_to_id(np_a[:,0]),
            right = array_to_id(np_a[:,-1]),
            bottom = array_to_id(np_a[-1,:])
        )

    def update_edge_ids(self):  
        base_array = self.permutations[0]['array']
        all_edge_ids = dict(
            top = array_to_id(base_array[0,:], both_ways=True),
            left = array_to_id(base_array[:,0], both_ways=True),
            right = array_to_id(base_array[:,-1], both_ways=True),
            bottom = array_to_id(base_array[-1,:], both_ways=True)
        )      
        self.edges_set = set(all_edge_ids.values())
    
    def update_unique_edges(self, all_edges):
        self.unique_edges = set([e for e in self.edges_set if all_edges[e] == 1])

def parse(txt):
    tiles = {}
    current_grid = None
    for line in txt.splitlines():
        if not line.strip():
            continue
        if line.startswith('Tile '):
            tile_id = int(line[4:-1])
            current_grid = []
            tiles[tile_id] = Tile(tile_id, current_grid) 
        else:
            current_grid.append(line)
    for t in tiles.values():
        t.initialize_array()
    return tiles

def find_num_unique_edges(tiles):
    all_edges = Counter()
    for tile in tiles.values():
        all_edges.update(tile.edges_set)
    for tile_id, tile in tiles.items():
        tile.update_unique_edges(all_edges)

def solve1(txt):
    tiles = parse(txt)
    find_num_unique_edges(tiles)
    corner_ids = [t_id for t_id, tile in tiles.items() if len(tile.unique_edges) == 2]
    answer = reduce(lambda a,b:a*b, corner_ids)
    return tiles, answer


SEA_MONSTER="""\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

SEA_MONSTER_ARRAY = np.array([[1 if c == '#' else 0 for c in r] for r in SEA_MONSTER.splitlines()])
SEA_MONSTER_NUM_FILLED = np.sum(SEA_MONSTER_ARRAY)


def solve2(tiles):
    map_dimension = int(math.sqrt(len(tiles)))
    full_map = complete_map(tiles)
    
    # Construct the full image
    rows = []
    for y in range(map_dimension):
        row = []
        for x in range(map_dimension):
            tile = full_map[(x,y)]
            t_array = tile.get_current_array()
            row.append(t_array[1:-1,1:-1]) # add array without borders
        rows.append(np.hstack(row))
    full_array = np.vstack(rows)

    monster_for_permutation = []
    for p_array in permute_array(full_array):
        corr = signal.correlate2d(p_array, SEA_MONSTER_ARRAY,mode='valid')
        num_monsters = np.sum(corr == SEA_MONSTER_NUM_FILLED)
        monster_for_permutation.append(num_monsters)
    max_monsters = max(monster_for_permutation)
    answer2 = np.sum(full_array) - SEA_MONSTER_NUM_FILLED*max_monsters
    return answer2

def test_example():
    tiles, answer1 = solve1(get_input('example.txt'))
    assert(20899048083289 == answer1)
    answer2 = solve2(tiles)
    assert(273 == answer2)

def test_puzzle():
    tiles, answer1 = solve1(get_input())
    print('Part 1:', answer1)
    assert(7492183537913 == answer1)
    answer2 = solve2(tiles)
    print('Part 2:', answer2)
    assert(2323 == answer2)

def complete_map(tiles):
    corner_ids = [t_id for t_id, tile in tiles.items() if len(tile.unique_edges) == 2]
    border_ids = [t_id for t_id, tile in tiles.items() if len(tile.unique_edges) == 1]
    middle_ids = [t_id for t_id, tile in tiles.items() if len(tile.unique_edges) == 0]

    full_map = {}
    #                x y
    current_index = (0,0)
    map_dimension = int(math.sqrt(len(tiles)))
    max_index = map_dimension - 1
    corners_to_directions = {
        # x y
        (0,0): set(['left','top']),
        (max_index,0): set(['top', 'right']),
        (max_index, max_index): set(['right','bottom']),
        (0,max_index): set(['bottom','left'])
    }
    for y in range(map_dimension):
        for x in range(map_dimension):
            current_index = (x, y)
            # assume we are in the middle
            tile_id_container = middle_ids #

            # requirements for 'outside' edges 
            # for corners and border tiles
            required_outside_directions = set()
            if current_index in corners_to_directions:
                # corners
                required_outside_directions = corners_to_directions[current_index]
                tile_id_container = corner_ids
            elif current_index[0] == 0 or current_index[1] == 0 or current_index[0] == max_index or current_index[1] == max_index:
                # border
                tile_id_container = border_ids
                if current_index[0] == 0:
                    required_outside_directions.add('left')
                if current_index[1] == 0:
                    required_outside_directions.add('top')
                if current_index[0] == max_index:
                    required_outside_directions.add('right')
                if current_index[1] == max_index:
                    required_outside_directions.add('bottom')

            required_neigbor_edges = {}
            if current_index[0] > 0:
                left_neighbor = full_map[(current_index[0]-1,current_index[1])]
                required_neigbor_edges['left'] = left_neighbor.get_current_edges()['right']
            if current_index[1] > 0:
                top_neighbor = full_map[(current_index[0], current_index[1]-1)]
                required_neigbor_edges['top'] = top_neighbor.get_current_edges()['bottom']

            # find tile
            found_tile = False
            for tile_id in tile_id_container:
                if found_tile:
                    break
                tile = tiles[tile_id]
                outside_edges = set(itertools.chain(*tile.unique_edges))
                for perm_index in range(12):
                    tile_edges = tile.get_permutated_edges(perm_index)
                    outside_direction = set([direction for direction,edge in tile_edges.items() if edge in outside_edges])
                    good_neighbor = all(tile_edges[k]==v for k,v in required_neigbor_edges.items())
                    if outside_direction == required_outside_directions and good_neighbor:
                        full_map[current_index] = tile
                        #print('Found tile', tile_id, tile.current_permutation)
                        tile_id_container.remove(tile_id)
                        found_tile = True
                        break

            if not found_tile:
                raise RuntimeError("could not find tile for", current_index)
    return full_map
    
if __name__ == "__main__":
    test_example()
    test_puzzle()