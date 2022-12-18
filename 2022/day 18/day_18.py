"""
Advent of Code 2022 - Day 18
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read().strip()

def surface_area(d):
    cubes = [tuple(map(int,line.split(','))) for line in d.splitlines()]    
    total_surface = 6*len(cubes)
    for dim in range(3):
        cubes.sort(key = lambda c: c[dim])
        other_dims = list(range(3))
        other_dims.remove(dim)
        prev_c = cubes[0]
        for this_c in cubes[1:]:
            d = this_c[dim] - prev_c[dim]
            if d == 1:
                other_d = sum(abs(prev_c[o_d]-this_c[o_d]) for o_d in other_dims)
                if other_d == 0:
                    # adjacent
                    total_surface -= 2 # for both sides
            prev_c = this_c
    return total_surface

from collections import defaultdict

def compute_surface_area(cubes, exterior=None):
    total_surface_area = 0
    for c in cubes:
        for N in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
            n_pos = tuple([sum(z) for z in zip(c,N)])
            if not n_pos in cubes:
                if not exterior or n_pos in exterior:
                    total_surface_area += 1
    return total_surface_area

def surface_area_grid(d, part2=False):
    cubes = {tuple(map(int,line.split(','))):1 for line in d.splitlines()}
    if not part2:
        return compute_surface_area(cubes)
    else:
        # "region growing" - all the visited coords
        # that are not part of the cubes are outside
        x_coords = [c[0] for c in cubes]
        y_coords = [c[1] for c in cubes]
        z_coords = [c[2] for c in cubes]
        min_x, max_x = min(x_coords)-1,max(x_coords)+1
        min_y, max_y = min(y_coords)-1, max(y_coords)+1
        min_z, max_z = min(z_coords)-1, max(z_coords)+1
        
        visit_grid = set()
        front = [(min_x,min_y, min_z)]
        while front:
            c = front.pop()
            visit_grid.add(c)
            for N in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                n_pos = tuple([sum(z) for z in zip(c,N)])
                if not n_pos in cubes:
                    if not n_pos in visit_grid:
                        if min_x <= n_pos[0] <= max_x and min_y <= n_pos[1] <= max_y and min_z <= n_pos[2] <= max_z:
                            front.append(n_pos)
        # compute surface but only count neighbors part of the outside coords
        return compute_surface_area(cubes, visit_grid)


def test_small():
    assert(10 == surface_area_grid("1,1,1\n2,1,1"))

EXAMPLE_DATA = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

def test_example():
    assert(64 == surface_area_grid(EXAMPLE_DATA))

def test_part1():
    result = surface_area_grid(data())
    print('PART 1:', result)

def test_example2():
    assert(58 == surface_area_grid(EXAMPLE_DATA, part2=True))

def test_part2():
    result = surface_area_grid(data(), part2=True)
    print('PART 2:', result)
    assert(2052 == result)

if __name__ == "__main__":
    test_small()
    test_example()
    test_part1()
    test_example2()
    test_part2()