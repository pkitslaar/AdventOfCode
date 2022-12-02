"""
Advent of Code 2017 - Day 03
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

def ring(n):
    r = 0
    ring_max = 1
    while n > ring_max:
        r += 1
        ring_max = (2*r+1)**2
    return r, ring_max


assert((0,1) == ring(1))
assert((1,9) == ring(2))
assert((2,25) == ring(12))
assert((2,25) == ring(23))

def n_to_pos(n):
    r, SE_VALUE = ring(n)
    # start at Southe East (SE) corner
    x = y = r

    # values at middle of each side
    #
    #    . . N . .
    #    . - - - .
    #    W - - - E
    #    . - - - .
    #    . . S . SE
    #
    side_values = {}
    side_values['S'] = SE_VALUE - r
    side_values['W'] = side_values['S'] - 2*r
    side_values['N'] = side_values['W'] - 2*r
    side_values['E'] = side_values['N'] - 2*r

    # find closest side
    dists = [(abs(n-v),k) for k,v in side_values.items()]
    dists.sort()
    closest_side = dists[0][1]
    signed_dist = n - side_values[closest_side]

    if closest_side == 'S':
        x = signed_dist
        y = -r
    elif closest_side == 'W':
        x = -r
        y = -signed_dist
    elif closest_side == 'N':
        x = - signed_dist
        y = r
    elif closest_side == 'E':
        x = r
        y = signed_dist
    else:
        raise ValueError(f'Unknown side {closest_side}')
    
    return x,y

assert((0,0) == n_to_pos(1))
assert((1,-1) == n_to_pos(9))
assert((2,-2) == n_to_pos(25))
assert((2, 2) == n_to_pos(13))

def n_to_dist(n):
    x, y = n_to_pos(n)
    return abs(x) + abs(y)

assert(0 == n_to_dist(1))
assert(3 == n_to_dist(12))
assert(2 == n_to_dist(23))
assert(31 == n_to_dist(1024))

def part1():
    d = n_to_dist(325489)
    print('PART 1:', d)
    assert(552 == d)

def solve2(n_stop):
    grid = {}
    ring = 0
    last_pos = (0,0)
    grid[last_pos] = 1
    while grid[last_pos] < n_stop:
        new_x = last_pos[0]
        new_y = last_pos[1]
        if last_pos == (ring,-ring):
            # start next ring
            ring += 1
            # start one step to right
            new_x += 1
        else:
            # find side we are on
  
            if last_pos[0] == ring: # east side
                if last_pos[1] < ring:
                    # step up
                    new_y += 1
                else:
                    # at the top so go left
                    new_x += -1
            elif last_pos[1] == ring: # north side
                if last_pos[0] > -ring:
                    # step to left
                    new_x += -1
                else:
                    # step down
                    new_y += -1
            elif last_pos[0] == -ring: # west side
                if last_pos[1] > -ring:
                    # step down
                    new_y += -1
                else:
                    # step right
                    new_x += 1
            elif last_pos[1] == -ring: # south side
                if last_pos[0] < ring:
                    # step right
                    new_x += 1
                else:
                    raise RuntimeError("At max_pos, this should not happen here")
            
        # compute new value
        new_pos = (new_x, new_y)
        assert(new_pos != last_pos)

        new_value = 0
        for N in [(-1, 1),(0, 1),(1, 1),
                  (-1, 0)       ,(1, 0),
                  (-1,-1),(0,-1),(1,-1)]:
            new_value += grid.get((new_pos[0]+N[0], new_pos[1]+N[1]),0)
        grid[new_pos] = new_value
        last_pos = new_pos
    return grid[last_pos]

def part2():
    result = solve2(325489)
    print('PART 2:', result)
    assert(330785 == result)
        
if __name__ == "__main__":
    part1()
    part2()
