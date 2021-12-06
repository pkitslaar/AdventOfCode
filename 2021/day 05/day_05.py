"""
Advent of Code 2021 - Day 05
Pieter Kitslaar
"""

from pathlib import Path

example = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

def parse(txt, diagonal = False):
    for line in txt.splitlines():
        from_txt, to_txt = line.split(' -> ')
        start_pos = tuple(map(int, from_txt.split(',')))
        end_pos = tuple(map(int, to_txt.split(',')))
        if diagonal or start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1]:
            start_pos, end_pos = sorted([start_pos, end_pos])
            yield {'start': start_pos, 'end': end_pos}

def bresenham(x0, y0, x1, y1):
    dx =  abs(x1-x0);
    sx = 1 if x0<x1 else -1
    dy = -abs(y1-y0);
    sy = 1 if y0<y1 else -1
    err = dx+dy;  #/* error value e_xy */
    while True:  # /* loop */
        yield x0, y0
        if (x0 == x1 and y0 == y1):
            break
        e2 = 2*err
        if (e2 >= dy): # /* e_xy+e_x > 0 */
            err += dy
            x0 += sx
        
        if (e2 <= dx): # /* e_xy+e_y < 0 */
            err += dx;
            y0 += sy

def compute_grid(start_end_positions):
    g = {}
    for se in start_end_positions:
        x0, y0 = se['start']
        x1, y1 = se['end']
        for x, y in bresenham(x0, y0, x1, y1):
            g[(x,y)] = g.get((x,y), 0) + 1
    return g

def plot(grid):
    max_x = max(p[0] for p in grid)
    max_y = max(p[1] for p in grid)
    for y in range(max_y+1):
        for x in range(max_x+1):
            print(grid.get((x,y), '.'), end='')
        print()

def num_dangerous(grid):
    num = 0
    for _, n in grid.items():
        if n > 1:
            num += 1
    return num

def test_example():
    grid = compute_grid(parse(example))
    result = num_dangerous(grid)
    assert 5 == result

def get_input():
    input_numbers = []
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    grid = compute_grid(parse(get_input()))
    result = num_dangerous(grid)
    print('Part 1:', result)

def test_example2():
    grid = compute_grid(parse(example, diagonal=True))
    result = num_dangerous(grid)
    assert 12 == result

def test_part2():
    grid = compute_grid(parse(get_input(), diagonal=True))
    result = num_dangerous(grid)
    print('Part 2:', result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()