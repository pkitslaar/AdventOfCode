import sys
from pathlib import Path
d5_dir = Path(__file__).parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))
from day_05 import run, txt_values

def test_intcode_basic():
    for in_, out_ in [("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),]:
        assert(txt_values(out_) == run(txt_values(in_))[1])

NORTH, SOUTH, WEST, EAST = range(1,5)
MOVE_NAME_TO_DIFF = {
    NORTH: ( 0, -1),
    SOUTH: ( 0,1),
    WEST:  (-1, 0), 
    EAST:  ( 1, 0),
}
DIFF_TO_MOVE = {v:k for k,v in MOVE_NAME_TO_DIFF.items()}

UNKNOWN, WALL, EMPTY, OXYGEN = range(-1,3)
STATUS_TO_TEXT = {
    UNKNOWN:'?',
    WALL: '#',
    EMPTY: '.',
    OXYGEN: 'O',
}

MANUAL_MODE, EXPLORE_MODE = range(2)

class ExplorationFinished(Exception):
    pass

class DroidControl():
    def __init__(self, mode = MANUAL_MODE):
        self.mode = mode
        self.next_move = None
        self.send_move = None
        self.current_pos = (0,0)
        self.path = [(0,0)]
        self.map = {
            (0,0): EMPTY,
        }
        self.oxyen_pos = None

        if self.mode == EXPLORE_MODE:
            self.explore_next_move()

    def explore_next_move(self):
        for direction in (NORTH, SOUTH, EAST, WEST):
            test_move = MOVE_NAME_TO_DIFF[direction]
            test_pos = self.current_pos[0]+test_move[0], self.current_pos[1]+test_move[1]
            test_v = self.map.get(test_pos, UNKNOWN)
            if test_v == UNKNOWN:
                self.next_move = direction
                return
        # no unknown direction found backtrack
        if len(self.path) > 1:
            prev_pos = self.path[-2]
            diff = prev_pos[0] - self.current_pos[0], prev_pos[1] - self.current_pos[1]
            self.next_move = DIFF_TO_MOVE[diff]
        else:
            print('Done exploring')
            raise ExplorationFinished()


    def set_next_move(self, m):
        self.next_move = m
        self.send_move = None

    def send_next_move(self):
        if not self.next_move:
            raise RuntimeError("No next move defined!")
        self.send_move = self.next_move
        self.next_move = None
        return self.send_move
    
    def receive_status(self, v):
        step = MOVE_NAME_TO_DIFF[self.send_move]
        self.send_move = None
        next_pos = self.current_pos[0]+step[0], self.current_pos[1]+step[1]
        if next_pos in self.map:
            assert(v == self.map[next_pos])

        if v == WALL:
            self.map[next_pos] = WALL
        elif v == EMPTY or v == OXYGEN:
            # we made a step
            self.current_pos = next_pos

            if self.current_pos in self.map:
                while self.path[-1] != self.current_pos:
                    self.path.pop()
            else:
                # unknown position to append to path
                self.path.append(self.current_pos)

            self.map[self.current_pos] = v

            if v == OXYGEN:
                self.oxyen_pos = self.current_pos
                print('Found oxygen at pos', self.current_pos, 'path length', len(self.path))
        else:
            raise ValueError("Unknow status", v)

        if self.mode == EXPLORE_MODE:
            self.explore_next_move()

    def draw(self, map_to_draw = None, x_range=(-2,3), y_range=(-3,3)):
        if map_to_draw is None:
            map_to_draw = self.map
        positions = list(map_to_draw)
        x_positions = [p[0] for p in positions] + list(x_range)
        y_positions = [p[1] for p in positions] + list(y_range)
        min_x, max_x = min(x_positions), max(x_positions)
        min_y, max_y = min(y_positions), max(y_positions)
        width =  max_x - min_x + 1
        height = max_y-min_y + 1
        print('min_x', min_x, 'max_x', max_x)
        print('min_y', min_x, 'max_y', max_x)
        print(width, height)
        grid = [[' ']*width for _ in range(height)]
        for p, v in map_to_draw.items():
            g_pos = p[0] - min_x, p[1] - min_y
            #print(p, g_pos)
            grid[g_pos[1]][g_pos[0]] = STATUS_TO_TEXT[v]
        grid[self.current_pos[1] - min_y][self.current_pos[0] - min_x] = 'D'
        for row in grid:
            print(''.join(row))
        print('path', self.path)

    def create_arrival_map(self, start_pos=(0,0)):
        arrival_map = {}
        front = [(0,start_pos)]
        while front:
            front.sort(reverse=True)
            fastest = front.pop()
            if fastest[1] not in arrival_map:
                arrival_map[fastest[1]] = fastest[0]
                for diff in MOVE_NAME_TO_DIFF.values():
                    test_pos = fastest[1][0] + diff[0], fastest[1][1] + diff[1]
                    test_v = self.map.get(test_pos)
                    assert(test_v is not None)
                    if test_v != WALL:
                        front.append((fastest[0]+1, test_pos))
        return arrival_map



def test_simple_grid():
    dc = DroidControl()
    dc.draw()

    # step 1
    dc.set_next_move(NORTH)
    assert(NORTH == dc.send_next_move())
    dc.receive_status(WALL)
    dc.draw()

    # step 2
    dc.set_next_move(EAST)
    assert(EAST == dc.send_next_move())
    dc.receive_status(EMPTY)
    dc.draw()

    # find additional walls
    dc.set_next_move(NORTH); dc.send_next_move(); dc.receive_status(WALL)
    dc.set_next_move(SOUTH); dc.send_next_move(); dc.receive_status(WALL)
    dc.set_next_move(EAST); dc.send_next_move(); dc.receive_status(WALL)
    dc.draw()

    # backtrack
    dc.set_next_move(WEST); dc.send_next_move(); dc.receive_status(EMPTY)
    dc.draw()

    #
    dc.set_next_move(WEST); dc.send_next_move(); dc.receive_status(WALL)
    dc.set_next_move(SOUTH); dc.send_next_move(); dc.receive_status(EMPTY)
    dc.set_next_move(SOUTH); dc.send_next_move(); dc.receive_status(WALL)
    dc.set_next_move(WEST); dc.send_next_move(); dc.receive_status(OXYGEN)
    dc.draw()

def main():
    test_simple_grid()
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_program = txt_values(f.read())

    dc = DroidControl(mode = EXPLORE_MODE)
    try:
        run(main_program, input_v=dc.send_next_move, output_cb=dc.receive_status, stop_on_output=False)
    except ExplorationFinished:
        pass
    #dc.draw()
    arrival = dc.create_arrival_map()
    print('Part 1:', arrival[dc.oxyen_pos])

    oxygen_arrival = dc.create_arrival_map(dc.oxyen_pos)
    print('Part 2:', max(oxygen_arrival.values()))

if __name__ == "__main__":
    main()

