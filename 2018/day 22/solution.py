# Advent of code - 2018
# Day 22 
#
# Pieter Kitslaar
#

import numpy as np
import heapq

ROCKY = 0
WET = 1
NARROW = 2
MOUTH = 3 
TARGET = 4 
TARGET = 5 

CHAR_TABLE = {
    MOUTH: 'M',
    TARGET: 'T',
    ROCKY: '.',
    WET: '=',
    NARROW: '|',
}

def cave(depth, target):
    tx, ty = target
    h,w = 4*ty, 6*tx

    geological_index = np.zeros((h,w), dtype=np.int_)
    geological_index[0, :] = 16807*np.array(range(geological_index.shape[1]))
    geological_index[:, 0] = 48271*np.array(range(geological_index.shape[0]))
    geological_index[0][0] = 0
    geological_index[ty][tx] = 0

    erosion_level = np.mod(depth+geological_index, 20183)
    for y in range(1, geological_index.shape[0]):
        for x in range(1, geological_index.shape[1]):
            if y == ty and x == tx:
                g = 0
            else:
                g = erosion_level[y-1][x] * erosion_level[y][x-1]
            geological_index[y][x] = g
            erosion_level[y][x] = (depth+g) % 20183

    #erosion_level = np.mod(depth+geological_index, 20183)
    region_type = np.mod(erosion_level, 3)
    #region_type[0][0] = MOUTH
    #region_type[ty][tx] = TARGET
    return region_type

def render(region_type):
    for r in region_type:
        print(*[CHAR_TABLE[v] for v in r], sep='')

def risk(region_type, target):
    tx, ty = target
    return np.sum(region_type[0:ty+1, 0:tx+1])


# item types
NEITHER = 0
TORCH = 1
CLIMING_GEAR = 2

class Route(object):
    def __init__(self):
        self.transitions = {
            NEITHER: {
                WET: {
                    TARGET: [(8+7, TORCH)],
                    ROCKY:  [(8, CLIMING_GEAR)],
                    WET:    [(1, NEITHER), (8, CLIMING_GEAR)],
                    NARROW: [(1, NEITHER)],
                },
                NARROW: {
                    TARGET:  [(8, TORCH)],
                    ROCKY:   [(8, TORCH)],
                    NARROW:  [(1, NEITHER), (8, TORCH)],
                    WET:     [(1, NEITHER)],
                }
            },
            TORCH: {
                ROCKY: {
                    TARGET: [(1, TORCH)],
                    ROCKY:  [(1, TORCH), (8, CLIMING_GEAR)],
                    WET:    [(8, CLIMING_GEAR)],
                    NARROW: [(1, TORCH)],
                },
                NARROW: {
                    TARGET: [(1, TORCH)],
                    ROCKY:  [(1, TORCH)],
                    WET:    [(8, NEITHER)],
                    NARROW: [(1, TORCH), (8, NEITHER)],
                },
            },
            CLIMING_GEAR: {
                ROCKY: {
                    TARGET: [(1+7, TORCH)],
                    ROCKY:  [(1, CLIMING_GEAR), (8, TORCH)],
                    WET:    [(1, CLIMING_GEAR)],
                },
                WET: {
                    TARGET: [(1+7, TORCH)],
                    ROCKY:  [(1, CLIMING_GEAR)],
                    WET:    [(1, CLIMING_GEAR), (8, NEITHER)],
                    NARROW: [(8, NEITHER)],
                }
            }
        }

    def item_str(self, item):
        return {TORCH: 'TORCH', CLIMING_GEAR: 'CLIMING_GEAR', NEITHER: 'NEITHER'}[item]
    
    def type_str(self, region_type):
        return {ROCKY: 'ROCKY', NARROW: 'NARROW', WET: 'WET', TARGET: 'TARGET'}[region_type]

    def speed(self, current_item, from_, to_):
            try:
                return self.transitions[current_item][from_][to_]
            except KeyError:
                return [(None, None)]

    def search(self, region_types, target):
        h, w = region_types.shape
        t_x, t_y = target

        # mark the target as the special TARGET type
        # this makes the transition table use the special
        # transitions which already account for the requirement
        # that at the target location we need a TORCH
        region_types[t_y][t_x] = TARGET
        times = -1*np.ones((h, w, 3))

        # start front with potential staring situations
        front = [
            (0, TORCH, (0,0)),
            (7, CLIMING_GEAR, (0,0)),
        ]
        for t, item, (y, x) in front:
            times[y][x][item] = t

        heapq.heapify(front)
        while front:
            fastest = heapq.heappop(front)
            f_time, f_item, f_pos = fastest
            f_y, f_x = f_pos
            if times[f_y][f_x][f_item] < f_time:
                # old duplicate item in queue ignore
                continue 

            if f_item == TORCH and (f_y,f_x) == (t_y,t_x):
                print('Reached target', fastest, f_item)
                return fastest

            for offset_y, offset_x in [(0,-1),(0,1),(-1,0),(1,0)]:
                n_y = f_y + offset_y
                n_x = f_x + offset_x
                n_pos = (n_y, n_x)
                if 0 <= n_y < h and 0 <= n_x < w:
                       f_type = region_types[f_y][f_x]
                       n_type = region_types[n_y][n_x]
                       for n_speed, n_item in self.speed(f_item, f_type, n_type):
                           if n_speed: 
                               n_time = f_time + n_speed
                               c_time = times[n_y][n_x][n_item]
                               if c_time < 0 or n_time < c_time:
                                    times[n_y][n_x][n_item] = n_time
                                    heapq.heappush(front, (n_time, n_item, (n_pos)) ) 

def solve(depth, target):
    region_type = cave(depth, target)
    #render(region_type)
    print('risk', risk(region_type, target))
    r = Route()
    r.search(region_type, target)
    return region_type

print('Example')
solve(510, (10,10))

#depth: 11739
#target: 11,718
print('PART 1')
solve(11739, (11,718))
            


