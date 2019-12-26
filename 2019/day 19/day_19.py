import sys
from pathlib import Path
d5_dir = Path(__file__).resolve().parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))
from day_05 import run, txt_values
from collections import deque

def test_intcode_basic():
    for in_, out_ in [("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),]:
        assert(txt_values(out_) == run(txt_values(in_))[1])

def droid_deploy(values):
        i = iter(values)
        def get_v():
            return next(i)
        return get_v

def part1():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_program = txt_values(f.read())

    def area_generator(width, height):
        for x in range(width):
            for y in range(height):
                yield x,y
    
    w, h = 50,50
    grid = [[' ']*w for _ in range(h)]
    num_affected = 0
    for x,y in area_generator(w,h):
        _, _, output = run(main_program, input_v = droid_deploy((x,y)), stop_on_output=False)
        grid[y][x] = output[-1]
        if output[-1] > 0:
            num_affected += 1
    print('\n'.join([''.join(map(str,r)) for r in grid]))
    print('Part 1:', num_affected)
    assert(160 == num_affected)

def print_values(values):
        y_coords = [y for y in values.keys()]
        x_coords = [x for y_row in values.values() for x in y_row]
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        grid = [['  ']*(1+max_x - min_x) for _ in range(min_y, max_y+1)]
        for y, y_row in values.items():
            for x,v in y_row.items():
                y_index = y - min_y
                x_index = x - min_x
                grid[y_index][x_index]=v
        
        print('y/x', ''.join('{0:2}'.format(x % 10) for x in range(min_x, max_x+1)))
        print('\n'.join('{0:>3} '.format(y_index+min_y) + ''.join(['{0:2}'.format(v) for v in r]) for y_index, r in enumerate(grid)))
        print('-'*80)

OUTSIDE, LEFT, RIGHT = range(3)

class IntCodeDroidControl:
    def __init__(self):
        with open(Path(__file__).parent / 'input.txt', 'r') as f:
           self.main_program = txt_values(f.read())
    
    def get_droid_value(self, x, y):
        _,_, output = run(self.main_program, input_v=droid_deploy((x,y)))
        v = output[-1]
        return v

part2_example="""\
#.......................................
.#......................................
..##....................................
...###..................................
....###.................................
.....####...............................
......#####.............................
......######............................
.......#######..........................
........########........................
.........#########......................
..........#########.....................
...........##########...................
...........############.................
............############................
.............#############..............
..............##############............
...............###############..........
................###############.........
................#################.......
.................########OOOOOOOOOO.....
..................#######OOOOOOOOOO#....
...................######OOOOOOOOOO###..
....................#####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
.....................####OOOOOOOOOO#####
......................###OOOOOOOOOO#####
.......................##OOOOOOOOOO#####
........................#OOOOOOOOOO#####
.........................OOOOOOOOOO#####
..........................##############
..........................##############
...........................#############
............................############
.............................###########"""

class GridDroidControl:
    def __init__(self, grid_txt):
        self.grid = [list(r) for r in grid_txt.strip().splitlines()]
    
    def get_droid_value(self,x,y):
        try:
            v = self.grid[y][x]
            return 0 if v=='.' else 1
        except IndexError:
            return -1

def solve_part2(start_pos, droid_control, ship_size):
    front_left = deque([(LEFT, start_pos)])
    front_right = deque([(RIGHT, start_pos)])
    values = {}
    front, next_front = front_left, front_right
    y_edge_and_width = {0: (0,0)}
    while front_left or front_right:
        if not front:
            front, next_front = next_front, front
            continue
        side, (x,y) = front.popleft()
        try:
            v = values[y][x]
        except KeyError:
            v = droid_control.get_droid_value(x,y)
            if v < 0:
                front, next_front = next_front, front
                continue
            values.setdefault(y, {})[x] = side if v > 0 else -side
        
        # check width of y-row
        y_row = values[y]
        left_edge = -1
        right_edge = -1
        for yx,yv in sorted(y_row.items()):
            if yv == -LEFT:
                left_edge = yx+1
            if yv == -RIGHT and right_edge < 0:
                right_edge = yx-1
            y_edge_and_width[y] = (left_edge, right_edge)
            if y > (ship_size-1):
                upper_y = y-(ship_size-1)
                if upper_y > start_pos[1]:
                    upper_left, upper_right = y_edge_and_width[upper_y]
                    if upper_right - left_edge+1 == ship_size:
                        print("UPPER", upper_y, upper_left, upper_right)
                        print("LOWER", y, left_edge, right_edge)
                        print("CORNER", left_edge, upper_y)
                        return 10000*left_edge + upper_y


        if side == LEFT:
            if v > 0:
                # current position is in the beam
                # move to left until outside of beam
                if x > 0:
                    l = (x-1, y)
                    lv = values.get(l[1], {}).get(l[0])
                    if lv is None or lv > 0:
                        # not known or left side is also in-the beam
                        # keep moving to the left to find the edge
                        front_left.append((LEFT, l))
                    else:
                        # left should now be outside of beam
                        # move down
                        assert(lv <= 0)
                        front_left.append((LEFT, (x+1,y+1)))
            else:
                # current position outside of beam
                # move to right to find inside of the beam
                r = (x+1,y)
                rv = values.get(r[1],{}).get(r[0])
                if rv is None or rv <= 0:
                    # unknown value to right or right is also outside of beam
                    # keep moving to the right
                    front_left.append((LEFT, r))
                else:
                    # right side should be in the beam
                    # so move down
                    assert(rv > 0)
                    front_left.append((LEFT, (x+1,y+1)))

        if side == RIGHT:
            if v > 0:
                # current position is in the beam
                # move to right until outside of beam
                r = (x+1, y)
                rv = values.get(r[1],{}).get(r[0])
                if rv is None or rv > 0:
                    # not known or right side is also in-the beam
                    # keep moving to the right to find the edge
                    front_right.append((RIGHT, r))
                else:
                    # right should now be outside of beam
                    # move down
                    assert(rv <= 0)
                    front_right.append((RIGHT, (x+1,y+1)))
            else:
                # current position outside of beam
                # move to left to find inside of the beam
                if x > 0:
                    l = (x-1,y)
                    lv = values.get(l[1], {}).get(l[0])
                    if lv is None or lv <= 0:
                        # unknown value to left or left is also outside of beam
                        # keep moving to the left
                        front_right.append((RIGHT, l))
                    else:
                        # left side should be in the beam
                        # so move down
                        assert(lv > 0)
                        front_right.append((RIGHT, (x+1,y+1)))
        front, next_front = next_front, front
    return values

def test_part_2_example():
    dc = GridDroidControl(part2_example)
    v = solve_part2(start_pos=(1,1), droid_control=dc, ship_size=10)
    print(v)
    assert(250020 == v)

def part2():
    sp = (5,7)
    dc = IntCodeDroidControl()
    v = solve_part2(start_pos=sp, droid_control=dc, ship_size=100)
    print('Part 2:', v)
    assert(9441282 == v)


if __name__ == "__main__":
    part1()
    part2()