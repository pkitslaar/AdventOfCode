# Advent of code - 2018
# Day 23 
#
# Pieter Kitslaar
#
from pathlib import Path
THIS_DIR = Path(__file__).parent
import numpy as np
import re
regex = re.compile('-*\d+')

example_data = """\
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
"""

X, Y, Z, R = range(4)
COORDS = slice(X,R)

def parse(data):
    points = []
    for l in data.splitlines():
        x, y, z, r = map(int,regex.findall(l))
        points.append((x,y,z,r))
    points.sort(key = lambda t: t[-1], reverse = True) # sort by radius
    return np.array(points, dtype=np.int_)

def solve(data):
    points = parse(data)
    largest_point = points[np.argmax(points[:,3], axis=0)]    
    distance = np.sum(np.abs(points[:,0:3] - largest_point[0:3]), axis=1)
    in_range = (largest_point[3] - distance) >= 0
    return np.sum(in_range)
    
def test_example():    
    in_range = solve(example_data)
    print('Example 1:', in_range)
    assert(in_range == 7)
    

def test_part1():
    with open(THIS_DIR / 'input.txt') as f:
        in_range = solve(f.read())
        print('PART 1:', in_range)
        assert(in_range == 943)

example_part_2 = """\
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5
"""

class Box:
    def __init__(self, min_x, max_x, min_y, max_y, min_z, max_z):        
        self.bounds = tuple([
            min_x,
            max_x,
            min_y,
            max_y,
            min_z,
            max_z,
        ])

    def __eq__(self, __o: object) -> bool:
        return self.bounds == __o.bounds

    def __lt__(self, other):
        return self.bounds < other.bounds

    def __hash__(self) -> int:
        return hash(self.bounds)

    def __repr__(self):
        return f"Box(*{self.bounds})"

    def get_bounds_for_dim(self, dim):
        return self.bounds[2*dim], self.bounds[(2*dim) + 1]

    def intersects(self, bot):
        # This implementation was taken from 
        # https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/ecfmpy0/
        d = 0
        for dim in range(3):
            min_d, max_d = self.get_bounds_for_dim(dim)
            d += abs(bot[dim] - min_d) + abs(bot[dim] - max_d)
            d -= max_d - min_d
        d //= 2            
        return d <= bot[3]

    def single_position(self):
        return self.bounds[0] == self.bounds[1] and self.bounds[2] == self.bounds[3] and self.bounds[4] == self.bounds[5]

    def center(self):
        center = []
        for dim in range(3):
            min_d, max_d = self.get_bounds_for_dim(dim)
            split_d = min_d + (max_d - min_d) // 2
            center.append(split_d)
        return center        

    def split_dim(self, dim):
        min_d, max_d = self.get_bounds_for_dim(dim)
        split_d = min_d + (max_d - min_d) // 2
        if split_d != max_d:
            return [(min_d, split_d), (split_d+1, max_d)]
        return [(min_d, max_d)]
    
    def partition(self):        
        for new_x_bounds in self.split_dim(0):
            for new_y_bounds in self.split_dim(1):
                for new_z_bounds in self.split_dim(2):
                    yield Box(
                        new_x_bounds[0], new_x_bounds[1], 
                        new_y_bounds[0], new_y_bounds[1], 
                        new_z_bounds[0], new_z_bounds[1])
        
def test_box_partition():
    a = Box(0, 10, 0, 10, 0, 10)
    p_a = list(a.partition())
    assert(len(p_a) == 8)    
    assert(p_a[0] == Box(0, 5, 0, 5, 0, 5))
    assert(p_a[1] == Box(0, 5, 0, 5, 6, 10))
    assert(p_a[2] == Box(0, 5, 6, 10, 0, 5))
    assert(p_a[3] == Box(0, 5, 6, 10, 6, 10))
    assert(p_a[4] == Box(6, 10, 0, 5, 0, 5))
    assert(p_a[5] == Box(6, 10, 0, 5, 6, 10))
    assert(p_a[6] == Box(6, 10, 6, 10, 0, 5))
    assert(p_a[7] == Box(6, 10, 6, 10, 6, 10))

    a = Box(0, 1, 0, 1, 0, 1)
    p_a = list(a.partition())    
    assert(len(p_a) == 8)    
    assert(p_a[0] == Box(0, 0, 0, 0, 0, 0))    
    assert(p_a[1] == Box(0, 0, 0, 0, 1, 1))    
    assert(p_a[2] == Box(0, 0, 1, 1, 0, 0))    
    assert(p_a[3] == Box(0, 0, 1, 1, 1, 1))
    assert(p_a[4] == Box(1, 1, 0, 0, 0, 0))    
    assert(p_a[5] == Box(1, 1, 0, 0, 1, 1))    
    assert(p_a[6] == Box(1, 1, 1, 1, 0, 0))    
    assert(p_a[7] == Box(1, 1, 1, 1, 1, 1))        

    a = Box(0, 0, 0, 0, 0, 2)
    p_a = list(a.partition())
    assert(len(p_a) == 2)    
    assert(p_a[0] == Box(0, 0, 0, 0, 0, 1))
    assert(p_a[1] == Box(0, 0, 0, 0, 2, 2)) 

    a = Box(0, 0, 0, 0, 0, 0)
    p_a = list(a.partition())
    assert(len(p_a) == 1)    
    assert(p_a[0] == Box(0, 0, 0, 0, 0, 0))

import heapq

def solve2(d):
    points = parse(d)
    
    min_total = np.min(points - points[:, R][:,np.newaxis], axis=0)
    max_total = np.max(points + points[:, R][:,np.newaxis], axis=0)    

    def compute_intersections(b):
        return sum(1 for nb in points if b.intersects(nb))

    def compute_cost(b):
        intersections = compute_intersections(b)
        
        box_radius_values = []
        for dim in range(3):
            min_d, max_d = b.get_bounds_for_dim(dim)
            box_radius_values.append(max_d - min_d)
        box_radius = min(box_radius_values)

        dist_center = sum(np.abs(b.center()))

        return (-intersections, -box_radius, dist_center )

    big_box = Box(
        min_total[0], max_total[0],
        min_total[1], max_total[1],
        min_total[2], max_total[2],
    )
    
    best_single = None
    
    test_boxes = [(compute_cost(big_box), big_box)]
    heapq.heapify(test_boxes)       
    while test_boxes:                
        (this_cost, tb) = heapq.heappop(test_boxes)              
        #print(len(test_boxes), this_cost, tb)
        if tb.single_position():                    
            if not best_single or this_cost < best_single[0]:
                best_single = (this_cost, tb)
                #print('best single pos', best_single)                
                break
        else:
            for new_tb in tb.partition():                
                cost = compute_cost(new_tb)                                 
                heapq.heappush(test_boxes, (cost, new_tb))
    return best_single[0][-1]
    

def test_example2():    
    dist = solve2(example_part_2)
    print('Example 2:', dist)
    assert(dist == 36)

def test_part2():
    with open(THIS_DIR / 'input.txt') as f:
        d = f.read()        
        dist = solve2(d)
        print('PART 2:', dist)
        assert(dist == 84087816)

if __name__ == "__main__":    
    test_box_partition()
    test_example()
    test_part1()
    test_example2()
    test_part2()
