import numpy as np
import re
import heapq
from PIL import Image


SAND = 0
CLAY = 100
WATER_PASS = 200
WATER_REST = 225
SPRING = 255 
FRONT = 150 

CHAR_TABLE = {
    SAND: '.',
    CLAY: '#',
    WATER_REST: '~',
    WATER_PASS: '|',
    SPRING: '+',
    FRONT: '?',
}

class Slice(object):
    def __init__(self, grid, spring ):
        self.spring = spring
        self.grid = grid

    def save_image(self, name):
        im = Image.fromarray(self.grid)
        im.convert('RGB').save(name, 'BMP')

    def render(self):
        for r in self.grid:
            print(*[CHAR_TABLE[v] for v in r], sep='')
        print()

    def get_value(self, coord):
        return self.grid[coord[0]][coord[1]]

    def set_value(self, coord, v):
        self.grid[coord[0]][coord[1]] = v

    def offset(self, coord, x=0, y=0):
        return (coord[0]+y,coord[1]+x)

    def get_value_offset(self, *args, **kwargs):
        return self.get_value(self.offset(*args, **kwargs))

    def check_water_at_rest(self, pos):
        min_x_pos, max_x_pos = pos[1], pos[1]
        while min_x_pos > 0 and self.get_value((pos[0], min_x_pos)) == WATER_PASS:
            min_x_pos -= 1
        min_v = self.get_value((pos[0], min_x_pos))

        while max_x_pos < self.grid.shape[1] and self.get_value((pos[0], max_x_pos)) == WATER_PASS:
            max_x_pos += 1
        max_v = self.get_value((pos[0], max_x_pos))
        return min_v == max_v == CLAY, min_x_pos, max_x_pos

    def water_reached(self):
        return np.sum((self.grid == WATER_REST) | (self.grid == WATER_PASS))

    def water_retained(self):
        return np.sum(self.grid == WATER_REST)

    def fill(self):
        front = [(-self.spring[0], self.spring)]
        while front:
            priority_y, s = heapq.heappop(front)
            v = self.get_value(s)

            next_fronts = []
            v_below = self.get_value_offset(s,y=1)
            if v_below in (SAND, CLAY, WATER_REST, WATER_PASS):
                    if v != SPRING:
                        self.set_value(s, WATER_PASS)
                    if v_below == SAND:
                            next_fronts.append(self.offset(s,y=1))
                    elif v_below in (CLAY, WATER_REST):
                        check_s = s
                        is_at_rest, min_rest_x, max_rest_x = self.check_water_at_rest(check_s)
                        if is_at_rest:
                            while is_at_rest:
                                self.grid[check_s[0], min_rest_x+1:max_rest_x] = WATER_REST
                                for c_x in range(min_rest_x+1,max_rest_x):
                                    c = (check_s[0]-1, c_x)
                                    if self.get_value(c) == WATER_PASS:
                                        next_fronts.append(self.offset(c,x=1))
                                        next_fronts.append(self.offset(c,x=-1))
                                check_s = self.offset(check_s, y=-1)
                                is_at_rest, min_rest_x, max_rest_x = self.check_water_at_rest(check_s)
                        else:
                            next_fronts.append(self.offset(s,x=1))
                            next_fronts.append(self.offset(s,x=-1))
                
            for nf in next_fronts:
                if 0 <= nf[0]+1 < self.grid.shape[0]:
                    if 0 <= nf[1] < self.grid.shape[1]:
                        if self.get_value(nf) == SAND:
                            heapq.heappush(front, (-nf[0], nf))
                            self.set_value(nf, FRONT)

    @staticmethod
    def parse(data):
        regex = re.compile('([xy])=(\d+)\.{0,2}(\d*)')
        soil = []
        for l in data.splitlines():
            clay = {'type': CLAY, 'x': (None, None), 'y': (None, None)}
            soil.append(clay)
            for p in l.split(', '):
                m = regex.match(p)
                coord, start, end = m.groups()
                if not end:
                    end = start
                clay[coord] = (int(start), int(end)+1)
        min_x = min([c['x'][0] for c in soil])-1
        max_x = max([c['x'][1] for c in soil])+1
        min_y = min([c['y'][0] for c in soil])-1
        max_y = max([c['y'][1] for c in soil])+1
        spring = (min_y,500)
        soil.append({'type': SPRING, 'x': (spring[1],spring[1]+1), 'y': (spring[0],spring[0]+1)})
        w, h = max_x - min_x, max_y - min_y
        g = np.zeros((h,w), dtype=np.int)
        for c in soil:
            X, Y = c['x'], c['y']
            y_start = Y[0] - min_y
            y_end   = Y[1] - min_y
            x_start = X[0] - min_x
            x_end   = X[1] - min_x
            g[y_start:y_end, x_start:x_end] = c['type'] 
        return Slice(g, (spring[0]-min_y, spring[1] - min_x) )

def solve(data):
    s = Slice.parse(data)
    s.save_image('before.bmp')
    s.fill()
    s.save_image('after.bmp')
    print('PART 1: Num meters water reached', s.water_reached())
    print('PART 2: Num meters water retained', s.water_retained())

example_data = """\
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""

print('Example data')
solve(example_data)
print()

print('Input data')
with open('input.txt') as f:
    solve(f.read())
    
