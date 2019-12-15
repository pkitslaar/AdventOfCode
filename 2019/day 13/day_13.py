"""
Day 13 puzzle - Advent of Code 2019
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

# output states
X, Y, TILE_ID = range(3)
STATE_TO_TEXT = {X:'X',Y:'Y',TILE_ID:'TILE_ID'}

EMPTY, WALL, BLOCK, H_PADDLE, BALL = range(5)
TILE_TO_CHARACTER = {
    EMPTY:    ' ',
    WALL:     '#',
    BLOCK:    'B',
    H_PADDLE: '-',
    BALL:     '*',
}

class Arcade:
    def __init__(self):
        self.output_state = X
        self.received = []
        self.tiles = {}
        self.scores = []
        self.ball_position = None
        self.paddle_position = None

    def move_joystick(self):
        self.print_screen()
        if self.ball_position[0] > self.paddle_position[0]:
            return 1
        elif self.ball_position[0] < self.paddle_position[0]:
            return -1
        else:
            return 0
    
    def receive_output(self, s):
        self.received.append(s)
        self.output_state = (self.output_state + 1) % 3
        if len(self.received) == 3:
            if self.received[X] < 0 and self.received[Y] == 0:
                self.scores.append(self.received[TILE_ID])
            else:
                self.tiles[(self.received[X], self.received[Y])] = self.received[TILE_ID]
                if self.received[TILE_ID] == BALL:
                    self.ball_position = (self.received[X], self.received[Y])
                if self.received[TILE_ID] == H_PADDLE:
                    self.paddle_position = (self.received[X], self.received[Y])
            self.received.clear()
    
    def print_screen(self):
        x_values = [p[0] for p in self.tiles]
        y_values = [p[1] for p in self.tiles]
        width = max(x_values)+1
        heigth = max(y_values)+1
        grid = [[' ']*width for _ in range(heigth)]
        for (x,y), tile_id in self.tiles.items():
            grid[y][x] = TILE_TO_CHARACTER[tile_id]
        for r in grid:
            print(''.join(r))
        print('Score:', self.scores[-1] if self.scores else 0)

def main():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        puzzle_data = txt_values(f.read())

    game = Arcade()
    run(puzzle_data[:], output_cb=game.receive_output, stop_on_output=False)
    game.print_screen()
    part1_sol = len([t for t in game.tiles.values() if t == BLOCK])
    print('Part 1:', part1_sol)

    # PArt 2
    part2_data = puzzle_data[:]
    part2_data[0] = 2 # insert two quarters

    print('*'*80)
    print('PART 2')
    game = Arcade()
    run(part2_data, input_v=game.move_joystick, output_cb=game.receive_output, stop_on_output=False)
    game.print_screen()

if __name__ == "__main__":
    main()
