"""
Advent of Code 2024 - Day 12
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
AAAA
BBCD
BBCC
EEEC
"""

EXAMPLE_DATA2 = """\
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

EXAMPLE_DATA3 = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

def parse(data):
    garden = {}
    for y, line in enumerate(data.strip().splitlines()):
        for x, c in enumerate(line):
            garden[(x,y)] = c
    W = x+1
    H = y+1
    return garden, W, H

from collections import defaultdict

def to_regions(garden):
    region_id = 0
    regions = {}
    for (x,y), p in garden.items():
        n_regions = set()
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            n_pos = (x+dx, y+dy)
            if n_pos in garden and garden[n_pos] == p:
                try:
                    n_regions.add(regions[(x+dx, y+dy)])
                except KeyError:
                    pass

        # assign region id based on neighbours or create new region
        if n_regions:
            n_id = min(n_regions)
            regions[(x,y)] = n_id
        else:
            regions[(x,y)] = region_id
            region_id += 1

        # if we find different region ids as neighbours, merge them
        if len(n_regions) > 1:
            n_id = min(n_regions)
            for (x_,y_), r in regions.items():
                if r in n_regions:
                    regions[(x_,y_)] = n_id
    return regions

def solve(data, part2=False):
    garden, W, H = parse(data)
    regions = to_regions(garden)

    region_area = defaultdict(int)
    region_perimeter = defaultdict(list)
    for (x,y), p in regions.items():
        region_area[p] += 1
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            n_pos = (x+dx, y+dy)
            if n_pos not in regions or regions[n_pos] != p:
                region_perimeter[p].append((n_pos, (dx,dy)))
    result = 0
    if not part2:
        result = sum(len(region_perimeter[p])*a for p,a in region_area.items())
    else:
        for r, area in region_area.items():
            n_sides = 0
            # devide the perimeter into types
            # e.g all the upper, lower and left and right edges
            perimeter_types = defaultdict(list)
            for pos, (dx,dy) in region_perimeter[r]:
                perimeter_types[(dx,dy)].append(pos)
            
            for p_type, p_positions in perimeter_types.items():
                p_type_grid = {p:1 for p in p_positions} # create a grid with this perimeter
                p_type_regions = to_regions(p_type_grid) # find the regions in this grid
                n_p_type_regions = len(set(p_type_regions.values())) # count the regions
                n_sides += n_p_type_regions
            
            result += n_sides * area
    return result


def test_example():
    assert solve(EXAMPLE_DATA) == 140
    assert solve(EXAMPLE_DATA2) == 772
    assert solve(EXAMPLE_DATA3) == 1930


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 1533024


def test_example2():
    assert solve(EXAMPLE_DATA, part2=True) == 80
    assert solve(EXAMPLE_DATA3, part2=True) == 1206


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 910066


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()