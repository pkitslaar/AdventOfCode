"""
Advent of Code 2021 - Day 20
Pieter Kitslaar
"""

from pathlib import Path

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()


example="""\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""

def parse(txt):
    algorithm_parts = []
    input_image_rows = []
    handle_input_image=False
    for line in txt.splitlines():
        if not line.strip():
            handle_input_image = True
        else:
            if handle_input_image:
                input_image_rows.append(line.strip())
            else:
                algorithm_parts.append(line.strip())
    algorithm = "".join(algorithm_parts)
    input_image = {}
    for y, row in enumerate(input_image_rows):
        for x, v in enumerate(row):
            if v == '#':
                input_image[(y,x)]=1
    return algorithm, input_image

def test_parse():
    algo, in_image = parse(example)
    assert len(algo) == 512

KERNEL= [
    (-1,-1), (-1,0), (-1,1),
    ( 0,-1), ( 0,0), ( 0,1),
    ( 1,-1), ( 1,0), ( 1,1)
]

def enhance(image, algorithm, out_bounds=None, out_bounds_value=None):
    new_image = {}
    y_coords, x_coords = zip(*image)
    min_y, max_y = min(y_coords), max(y_coords)
    min_x, max_x = min(x_coords), max(x_coords)
    for y in range(min_y-1,max_y+2):
        for x in range(min_x-1, max_x+2):
            bit_values = []
            for ky,kx in KERNEL:
                py, px = y+ky, x+kx
                v = image.get((py,px),0)
                if out_bounds:
                    if not in_bounds((py,px), out_bounds):
                        v = out_bounds_value
                bit_values.append(v)
            bit_string = "".join(map(str,bit_values))
            value = int(bit_string,2)
            if algorithm[value] == '#':
                new_image[(y,x)]=1
    return new_image

def im_bounds(image):
    y_coords, x_coords = zip(*image)
    min_y, max_y = min(y_coords), max(y_coords)
    min_x, max_x = min(x_coords), max(x_coords)
    return (min_y, min_x, max_y, max_x)

def plot(image, _max_x = None, _max_y=None):
    y_coords, x_coords = zip(*image)
    min_y, max_y = min(y_coords), _max_y or max(y_coords)+1
    min_x, max_x = min(x_coords), _max_x or max(x_coords)+1
    print(f"({min_y},{min_x})")
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            print('.#'[image.get((y,x),0)],end='')
        print()
    print(" "*(max_x-min_x),f"({max_y},{max_x})")


def test_example():
    algo, in_image = parse(example)
    out_image = enhance(enhance(in_image, algo), algo)
    assert len(out_image) == 35

def in_bounds(p, in_bounds):
    return in_bounds[0]<=p[0]<=in_bounds[2] and in_bounds[1]<=p[1]<=in_bounds[3]

def enhance_n_times(in_image, algo, N):
    last_image = in_image
    bounds = None
    # if the first element of algo is '#' (algo_0)
    # this means that when all pixels in the input image are empty
    # all pixels in the output image will be turned on
    # to simulate this in the 'infinite' image we toggel the logic
    # for retrieving values outside the current image to be 1
    # in the 'odd' phases of the loop
    algo_0 = int(algo[0] == '#')

    for i in range(N):
        if i % 2 == 0:
            last_image = enhance(last_image, algo)
        else:
            if algo_0:
                bounds = im_bounds(last_image) 
            last_image = enhance(last_image, algo, bounds, algo_0)
    return last_image

def test_part1():
    algo, in_image = parse(get_input())
    result = len(enhance_n_times(in_image, algo, 2))
    print('Part 1', result)
    assert 5765 == result

def test_example2():
    algo, in_image = parse(example)
    result = len(enhance_n_times(in_image, algo, 50))
    assert 3351 == result

def test_part2():
    algo, in_image = parse(get_input())
    result = len(enhance_n_times(in_image, algo, 50))
    print('Part 2', result)
    assert 18509 == result
    

if __name__ == "__main__":
    test_parse()
    test_example()
    test_part1()
    test_example2()
    test_part2()
