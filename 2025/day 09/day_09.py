"""
Advent of Code 2025 - Day 09
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

from itertools import combinations

def is_point_on_segment(p, p1, p2):
    return (p1[0] <= p[0] <= p2[0] or p2[0] <= p[0] <= p1[0]) and (p1[1] <= p[1] <= p2[1] or p2[1] <= p[1] <= p1[1])

def cross_product(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

from enum import Enum

class PointPosition(Enum):
    ON_EDGE = 0
    INSIDE = 1
    OUTSIDE = 2

def winding_number(polygon, point) -> PointPosition:
    winding_number = 0
    num_vertices = len(polygon)

    for i in range(num_vertices):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % num_vertices]

        if is_point_on_segment(point, p1, p2):
            return PointPosition.ON_EDGE

        if p1[1] <= point[1]:
            if p2[1] > point[1] and cross_product(p1, p2, point) > 0:
                winding_number += 1
        else:
            if p2[1] <= point[1] and cross_product(p1, p2, point) < 0:
                winding_number -= 1
    
    if winding_number == 0:
        return PointPosition.OUTSIDE

    return PointPosition.INSIDE

def point_in_polygon_winding(point, polygon) -> PointPosition:
    return winding_number(polygon, point)

def create_svg_with_polygons(polygons, filename="polygons.svg"):
    min_x = min(p[0] for polygon in polygons for p in polygon)
    max_x = max(p[0] for polygon in polygons for p in polygon)
    min_y = min(p[1] for polygon in polygons for p in polygon)
    max_y = max(p[1] for polygon in polygons for p in polygon)
    svg_elements = []
    svg_elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x-1} {min_y-1} {max_x - min_x + 2} {max_y - min_y + 2}">')
    for i, polygon in enumerate(polygons):
        color = f"hsl({(i * 137) % 360}, 70%, 70%)"
        points_str = " ".join(f"{p[0]},{p[1]}" for p in polygon)
        svg_elements.append(f'<polygon points="{points_str}" style="fill:{color};stroke:blue;stroke-width:1" />')
    svg_elements.append('</svg>')
    with open(filename, "w") as f:
        f.write("\n".join(svg_elements))

def solve(data, part2=False):
    result = 0
    tiles = []
    for line in data.splitlines():
        x, y = [int(v) for v in line.split(",")]
        tiles.append((x, y))



    areas = []
    for t1, t2 in combinations(tiles, 2):
        area = (abs(t1[0] - t2[0])+1) * (abs(t1[1] - t2[1])+1)
        areas.append((area, t1, t2))
     
    areas.sort(reverse=True, key=lambda x: x[0])
    if not part2:
        return areas[0][0]
    else:
        tile_perimeter_points = [tiles[0]]
        for t in tiles[1:] + [tiles[0]]:
            # add midpoints between t and last point
            last = tile_perimeter_points[-1]
            if t[0] == last[0]:
                tile_perimeter_points.append((t[0], (t[1] + last[1]) // 2))
            elif t[1] == last[1]:
                tile_perimeter_points.append(((t[0] + last[0]) // 2, t[1]))
            else:
                raise ValueError("Tiles are not aligned")
            tile_perimeter_points.append(t)


        for area, t1, t2 in areas:
            # create closed polygon from t1 and t2
            sorted_ts = sorted([t1, t2])
            t1, t2 = sorted_ts[0], sorted_ts[1]
            polygon = [
                (t1[0], t1[1]),
                (t2[0], t1[1]),
                (t2[0], t2[1]),
                (t1[0], t2[1]),
            ]
            if any(point_in_polygon_winding(p, tiles) == PointPosition.OUTSIDE for p in polygon):
                continue
            
            if any(point_in_polygon_winding(p, polygon) == PointPosition.INSIDE for p in tile_perimeter_points):
                continue

            visualize = False
            if visualize:
                create_svg_with_polygons([tiles, polygon], filename="tiles.svg")

            max_area = area
            break
    return max_area


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 50


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 4782896435


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 24


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result < 4609258448
    assert result == 1540060480


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()

if __name__ == "__main__":
    test_part2()