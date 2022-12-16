"""
Advent of Code 2022 - Day 15
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent


def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

EXAMPLE_DATA="""\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

import re
RE_COORDS = re.compile("=(-?\d+)")

from collections import namedtuple
class SensorInfo(namedtuple("SensorInfo", "sensor_x sensor_y beacon_x beacon_y")):
    def radius(self):
        return abs(self.sensor_x-self.beacon_x)+abs(self.sensor_y-self.beacon_y)
    def dist(self, x, y):
        return (abs(self.sensor_x-x)+abs(self.sensor_y-y)) 

def parse(d):
    sensors = []
    for line in d.splitlines():
        sensors.append(SensorInfo(*map(int,RE_COORDS.findall(line))))
    return sensors


def solve(d, y=10):
    sensors = parse(d)
    # sort by X coord
    sensors.sort(key=lambda si: si.sensor_x)

    no_valid_beacon_pos = set()
    for s in sensors:
        # check if at the sensor X pos and the requested Y position is in range
        d = s.dist(s.sensor_x,y)
        inside_d = s.radius()-d
        if inside_d > 0:
            for x in range(s.sensor_x-inside_d, s.sensor_x+inside_d+1):
                no_valid_beacon_pos.add(x)
    
    no_valid_beacon_pos.difference_update({s.beacon_x for s in sensors if s.beacon_y == y})
    return len(no_valid_beacon_pos)

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(26 == result)
    result = solve(EXAMPLE_DATA, y=11)
    assert(28 == result)

def test_part1():
    result = solve(data(),y=2000000)
    print('PART 1:', result)

def perimeter_points(radius, offset_x=0, offset_y=0, max_dim=None):
    for i in range(radius+1):
        for p in [(i,radius-i),(-radius+i,i),(i,-radius+i),(-radius+i,-i)]:
            full_p = (p[0]+offset_x, p[1]+offset_y)
            if max_dim is None or (0<=full_p[0]<=max_dim, 0<=full_p[1]<=max_dim):
                yield full_p

def test_perimeter_points():
    """
    r = 1

    .x.
    x.x
    .x.
    """
    assert({(0,-1),(0,1),(-1,0),(1,0)}==set(perimeter_points(1)))

    """
    r = 2

    ..x..
    .x.x.
    x...x
    .x.x.
    ..x..
    """
    assert({(0,2),(-1,1),(1,1),(-2,0),(2,0),(-1,-1),(1,-1),(0,-2)}==set(perimeter_points(2)))


from collections import defaultdict
import tqdm

def solve2(d, max_dim=20):
    """
    Based on hint from redddit
    - Search the perimeter of each sensor (so positions at radius+1)
    - Find the positions of perimeters that have the most overlap e.g intersections of sensors
    - Finally check for each of these intersections (starting from most intersections) if they
      are out of range for all sensors
    """
    sensors = parse(d)

    def in_range(pos):
        for s in sensors:
            d = s.dist(*pos)
            if d <= s.radius():
                return True
        return False
    
    # there is a more optimized way to limit the search range
    # e.g. rotate coords with 45 degrees
    # new_x = old_x - old_y
    # new_y = old_x + old_y
    # and look for intersections in rectangular grid 
    # but I gave up and did brute-force over the perimeter
    all_perimeter_points = defaultdict(int)
    for s in tqdm.tqdm(sensors):
        r = s.radius()+1
        for pp in perimeter_points(r,s.sensor_x, s.sensor_y, max_dim):
            all_perimeter_points[pp] += 1
            # the unique location should be at an intersection of at least 4 sensors
            # otherwise there would be more positions
            if all_perimeter_points[pp] >= 4 and not in_range(pp):
                return (pp[0]*4000000)+pp[1]
                    

def test_example2():
    result = solve2(EXAMPLE_DATA)
    assert(56000011 == result)

def test_part2():
    print('This will take long time to run.... (about 3-4 minutes)')
    result = solve2(data(), 4000000)
    print('PART 2:', result)
    assert(12274327017867 == result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()