"""
Day 11 puzzle - Advent of Code 2019
Pieter Kitslaar
"""
import sys
from pathlib import Path
d5_dir = Path(__file__).parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))
from day_05 import run, txt_values

def test_intcode_basic():
    for in_, out_ in [("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),]:
        assert(txt_values(out_) == run(txt_values(in_))[1])


PAINT, MOVE = range(2)
BLACK, WHITE = range(2)
LEFT_90_DEGREES, RIGH_90_DEGREES = range(2)

NEW_DIRS = {
    ( 0, 1): {LEFT_90_DEGREES: (-1, 0), RIGH_90_DEGREES: ( 1, 0)}, #  UP
    ( 0,-1): {LEFT_90_DEGREES: ( 1, 0), RIGH_90_DEGREES: (-1, 0)}, # DOWN
    (-1, 0): {LEFT_90_DEGREES: ( 0,-1), RIGH_90_DEGREES: ( 0, 1)}, # LEFT
    ( 1, 0): {LEFT_90_DEGREES: ( 0, 1), RIGH_90_DEGREES: ( 0,-1)}, # RIGHT
}

class Robot:
    def __init__(self):
        self.current_pos = (0,0)
        self.current_dir = (0,1) # up
        self.panel_colors = {
        }
        self.state = PAINT

    def __repr__(self):
        return "Robot (pos={0}, dir={1}, state={2})\n{3}".format(
            self.current_pos, self.current_dir, self.state, self.panel_colors)

    def print_grid(self, width=5, height=5):
        if width < 0 and height < 0:
            x_values = [p[0] for p in self.panel_colors]            
            y_values = [p[1] for p in self.panel_colors]
            min_x, max_x = min(x_values), max(x_values)
            min_y, max_y = min(y_values), max(y_values)
            width = (max_x - min_x)+1
            height = (max_y - min_y)+1
            center =  abs(min_x), abs(max_y)                       
        else:
            center = int(0.5*width), int(0.5*height)

        grid = [['.']*width for _ in range(height)]
        
        COLOR_C = {BLACK: '.', WHITE: '#'}
        for pos, c in self.panel_colors.items():
            g_pos = center[0]+pos[0], center[1]-pos[1]
            assert(g_pos[0]>=0)
            assert(g_pos[1]>=0)
            grid[g_pos[1]][g_pos[0]] = COLOR_C[c]
        DIR_C = {(0,1): '^', (-1,0): '<', (0,-1): 'v', (1,0): '>'}
        grid[center[1]-self.current_pos[1]][center[0]+self.current_pos[0]] = DIR_C[self.current_dir]

        return "\n".join(["".join(r) for r in grid])
    
    def get_v(self):
        return self.panel_colors.get(self.current_pos, BLACK)
    
    def __call__(self, v):
        """Gets output from program"""
        if PAINT == self.state:
            self.panel_colors[self.current_pos] = v
        elif MOVE == self.state:
            new_dir = NEW_DIRS[self.current_dir][v]
            #print('current', self.current_dir, 'DIR', v, 'new_dir', new_dir)
            self.current_dir = new_dir
            self.current_pos = self.current_pos[0]+self.current_dir[0], self.current_pos[1]+self.current_dir[1]
        self.state = {PAINT: MOVE, MOVE: PAINT}[self.state]

def test_examples():
    r = Robot()
    print(r);print(r.print_grid())
    assert(BLACK == r.get_v())

    r(1);r(0) # WHITE, LEFT
    assert(BLACK == r.get_v())
    print(r);print(r.print_grid())

    r(0);r(0) # BLACK, LEFT
    assert(BLACK == r.get_v())
    print(r);print(r.print_grid())

    r(1);r(0) # WHITE, LEFT
    print(r);print(r.print_grid())

    r(1);r(0) # WHITE, LEFT
    print(r);print(r.print_grid())
    assert(WHITE == r.get_v())

    r(0);r(1) # BLACK, RIGHT
    r(1);r(0) # WHITE, LEFT
    r(1);r(0) # WHITE, LEFT
    print(r)
    assert(6 == len(r.panel_colors))

part2_expexted = """\
.#..#..##..####.###..#..#..##...##..####...
.#..#.#..#....#.#..#.#..#.#..#.#..#....#...
.####.#......#..#..#.#..#.#....#..#...#....
.#..#.#.....#...###..#..#.#.##.####..#.....
.#..#.#..#.#....#.#..#..#.#..#.#..#.#....>.
.#..#..##..####.#..#..##...###.#..#.####..."""


def main():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_program = txt_values(f.read())

    part1_robot = Robot()
    part1_output = run(main_program, input_v=part1_robot.get_v, output_cb=part1_robot, stop_on_output=False)
    part1_solution = len(part1_robot.panel_colors)
    print('Part 1:', part1_solution)
    assert(2478 == part1_solution)

    part2_robot = Robot()
    part2_robot.panel_colors[(0,0)] = WHITE
    part2_output = run(main_program, input_v=part2_robot.get_v, output_cb=part2_robot, stop_on_output=False)
    part2_solution = part2_robot.print_grid(width=-1, height=-1)
    print('Part 2:\n', part2_solution)
    assert(part2_expexted == part2_solution)

if __name__ == "__main__":
    main()

