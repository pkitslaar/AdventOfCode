"""
Advent of Code 2022 - Day 14
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent


def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

EXAMPLE_DATA = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

def line_points(p0, p1):
    if p0[0] == p1[0]:
        x = p0[0]
        min_y = min([p0[1],p1[1]])
        max_y = max([p0[1],p1[1]])
        for y in range(min_y, max_y+1):
            yield (x, y)
    elif p0[1] == p1[1]:
        y = p0[1]
        min_x = min([p0[0],p1[0]])
        max_x = max([p0[0],p1[0]])
        for x in range(min_x, max_x+1):
            yield (x, y)
    else:
        raise ValueError(f'No element of coords are equal {p0} {p1}')

def print_cave(cave):
    X = [p[0] for p in cave]
    Y = [p[1] for p in cave]
    minX, maxX = min(X), max(X)
    minY, maxY = min(Y), max(Y)
    for y in range(minY, maxY+1):
        for x in range(minX, maxX+1):
            print(cave.get((x,y),'.'), end='')
        print()

def parse(d):
    cave = {}
    for line in d.strip().splitlines():
        prev_p = None
        for p_txt in line.split('->'):
            current_p = tuple(map(int, p_txt.strip().split(',')))
            if prev_p:
                for p in line_points(prev_p, current_p):
                    cave[p]='#'
            prev_p = current_p
    X = [p[0] for p in cave]
    Y = [p[1] for p in cave]
    minX, maxX = min(X), max(X)
    minY, maxY = min(Y), max(Y)
    if False:
        print_cave(cave)
    return cave, (minX, maxX, minY, maxY)

def solve(d, part2=False):
    cave, (minX, maxX, minY, maxY) = parse(d)
    sand_reached_infinite = False
    while not sand_reached_infinite:
        sand_x, sand_y = (500,0)
        sand_at_rest = False
        while not sand_at_rest:
            if part2:
                if sand_y == maxY+2:
                    cave[(sand_x, sand_y)] = '#'
                    sand_at_rest = True
            else:
                if sand_x < minX or sand_x > maxX or sand_y > maxY:
                    sand_reached_infinite = True
                    break
            if not cave.get((sand_x, sand_y+1)):
                # try down
                sand_y += 1
            elif not cave.get((sand_x-1, sand_y+1)):
                sand_x -= 1
                sand_y += 1
            elif not cave.get((sand_x+1, sand_y+1)):
                sand_x += 1
                sand_y += 1
            else:
                # no where to go
                cave[(sand_x, sand_y)] = 'o'
                sand_at_rest = True
                if part2 and ((500,0) == (sand_x, sand_y)):
                    sand_at_rest = True
                    sand_reached_infinite = True
    #print_cave(cave)
    return sum(1 for v in cave.values() if v == 'o')



def test_example():
    result = solve(EXAMPLE_DATA)
    assert(24 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)

def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    assert(93 == result)

def test_part2():
    result = solve(data(), part2=True)
    print('PART 2:', result)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()
   