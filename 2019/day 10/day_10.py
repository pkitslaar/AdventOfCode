"""
Day 10
"""

import math
from math import gcd
from pathlib import Path

EMPTY   = '.'
ASTROID = '#'

def check(a,b, tolerance=None):
    same = a == b
    if tolerance:
        same = abs(a-b) < tolerance
    if not same:
        raise AssertionError(f"{a} != {b}")
    return True

def direction_to_angle(d):
    """
    Convert a direction in grid space to an angle
    """
    angle = 0.5*math.pi - math.atan2(d[1],d[0])
    if angle < 0:
        angle += 2.0*math.pi
    return angle

TOLERANCE = 1e-6

def test_direction_to_angle():
    check(0, direction_to_angle((0,1)))
    check(0, direction_to_angle((1e-8,1)), TOLERANCE)
    check(45, math.degrees(direction_to_angle((1,1))), TOLERANCE)
    check(90, math.degrees(direction_to_angle((1,0))))
    check(135, math.degrees(direction_to_angle((1,-1))), TOLERANCE)
    check(180, math.degrees(direction_to_angle((0,-1))))
    check(225, math.degrees(direction_to_angle((-1,-1))), TOLERANCE)
    check(270, math.degrees(direction_to_angle((-1,0))))
    check(315, math.degrees(direction_to_angle((-1,1))), TOLERANCE)
    check(360, math.degrees(direction_to_angle((-1e-8,1))), TOLERANCE)

class Grid:
    def __init__(self, txt):
        self.shape, self.asteroids = txt_to_grid(txt)

    def __repr__(self):
        return "Grid (shape={0}, ateroids={1})".format(self.shape, self.asteroids)

    def vaporize(self, coord):
        vaporize_list = self.detected_asteroids(coord)
        total_vaporize = []
        while vaporize_list:
            total_vaporize.extend(vaporize_list)
            for v in vaporize_list:
                self.asteroids.remove(v)
            vaporize_list = self.detected_asteroids(coord)
        return total_vaporize

    def best_location(self):
        ast_detected = [(ast, self.detected_asteroids(ast)) for ast in self.asteroids]
        ast_detected.sort(key = lambda t: len(t[1]), reverse=True)
        return ast_detected[0]

    def detected_asteroids(self, coord, debug_output=False):
        asteroids_detected = set()
        for asteroid in self.asteroids:
            diff = asteroid[0] - coord[0], asteroid[1] - coord[1]
            diff_gdc = int(abs(gcd(diff[0], diff[1])))
            if diff_gdc > 0:
                diff_norm = tuple(map(lambda p: int(p/diff_gdc), diff))
                test_coord = coord[0]+diff_norm[0], coord[1]+diff_norm[1]
                while (test_coord[0] >= 0) and (test_coord[0] < self.shape[0]) and (test_coord[1] >= 0) and (test_coord[1] < self.shape[1]):
                    if test_coord in self.asteroids:
                        asteroids_detected.add((test_coord, diff_norm, direction_to_angle((diff_norm[0], -diff_norm[1]))))
                        break
                    test_coord = (test_coord[0]+diff_norm[0], test_coord[1]+diff_norm[1])
        sorted_asteroids = list(asteroids_detected)
        sorted_asteroids.sort(key=lambda p: p[2])
        if debug_output:
            for p in sorted_asteroids:
                print(p)
            
        return [p[0] for p in sorted_asteroids]

def txt_to_grid(txt):
    asteroids = set()
    for y, r in enumerate(txt.strip().splitlines()):
        for x, v in enumerate(r):
            if v != EMPTY:
                asteroids.add((x,y))
    shape = (x+1,y+1)
    return shape, asteroids


ex1="""
.#..#
.....
#####
....#
...##
"""

def text_ex1():
    g1 = Grid(ex1)
    assert(8 == len(g1.detected_asteroids((3,4))))
    assert((3,4) == g1.best_location()[0])

ex2="""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""

def test_ex2():
    g2 = Grid(ex2)
    g2_best = g2.best_location()
    assert((5,8) == g2_best[0])
    assert(33 == len(g2_best[1]))

ex3 = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""

def test_ex3():
    g3 = Grid(ex3)
    g3_best = g3.best_location()
    assert((1,2) == g3_best[0])
    assert(35 == len(g3_best[1]))

ex4="""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""

def test_ex4():
    g4 = Grid(ex4)
    g4_best = g4.best_location()
    assert((6,3) == g4_best[0])
    assert(41 == len(g4_best[1]))

ex5="""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

def test_ex5():
    g5 = Grid(ex5)
    g5_best = g5.best_location()
    assert((11,13) == g5_best[0])
    assert(210 == len(g5_best[1]))

def test_vaporize():
    g5 = Grid(ex5)
    g5_test_asteroids = g5.vaporize((11,13))
    check(g5_test_asteroids[0], (11,12))
    check(g5_test_asteroids[1], (12,1))
    check(g5_test_asteroids[2], (12,2))
    check(g5_test_asteroids[9], (12,8))
    check(g5_test_asteroids[19], (16,0))
    check(g5_test_asteroids[49], (16,9))
    check(g5_test_asteroids[99], (10,16))
    check(g5_test_asteroids[198], (9,6))
    check(g5_test_asteroids[199], (8,2))
    check(g5_test_asteroids[200], (10,9))
    check(g5_test_asteroids[298], (11,1))

def main():
    # Part 1
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_grid = Grid(f.read())
    part1_solution = main_grid.best_location()
    print('Part 1:', part1_solution[0], len(part1_solution[1]))

    part2_vaporize = main_grid.vaporize((23,20))
    part2_solution = part2_vaporize[199]
    print('Part 2:', part2_solution, 100*part2_solution[0]+part2_solution[1])


if __name__ == "__main__":
    main()
