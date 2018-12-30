# Advent of code - 2018
# Day 13
#
# Pieter Kitslaar
#

import numpy as np

LEFT, RIGHT = range(2)

def main():
    print('PART 1: EXAMPLE')
    assert((7,3) == part_1('test_data.txt'))
    print()
    
    print('PART 1: ASSIGNMENT')
    part_1('input.txt')
    print()
    
    print('PART 2: EXAMPLE')
    assert((6,4) == part_2('test_data_2.txt'))
    print()
    
    print('PART 2: ASSIGNMENT')
    part_2('input.txt')
    print()

def part_1(file_name):
    with open(file_name, 'r') as f:
        raw_test_data = f.read()
        
    data = split_blocks(raw_test_data)
    start_data = parse(data[0])
    final_data, crashed = tick_until_crash(start_data)
    
    crash_id = list(crashed)[0]
    crash_pos = final_data['carts_info'][crash_id]['pos']
    crash_y, crash_x  = crash_pos
    return crash_x, crash_y
    
def part_2(file_name):
    with open(file_name, 'r') as f:
        part_2_data = f.read()
    
    blocks = split_blocks(part_2_data)
    start = parse(blocks[0])
    
    return tick_until_one_left(start)
    
def tick_until_crash(start_data):
    prev_data = start_data
    while True:
        new_data, crashed = tick(prev_data)
        if crashed:
            break
        prev_data = new_data
    return new_data, crashed

def tick_until_one_left(start_data):
    prev_data = start_data
    final_tick = False
    while not final_tick:
        new_data, crashed = tick(prev_data, remove_crashed = True)
        if len(new_data['carts_info']) == 1:
                print('Only one cart left, this was the final tick')
                final_tick = True
        prev_data = new_data
    
    for cart in new_data['carts_info'].values():
        y, x = cart['pos']
        print('Cart left at position:', f'{x},{y}') 
        return (x, y)

def tick(prev_data, remove_crashed = False):
    # Copy data and deep copy 'carts_info'
    data = prev_data.copy()
    data['carts_info'] = {k:v.copy() for k,v in prev_data['carts_info'].items()}
    
    # Compute array for simple lookup for collision
    carts_array = compute_carts_array(data, encode = 'id')
    
    # keep track of crashed carts
    crashed_carts = set()
    
    # Order of carts movement is based on position
    # first y than x order (therefore we store the position as (y, x)
    # so it by default sorts without swapping values.
    sorted_ids = [v['id'] for v in sorted(data['carts_info'].values(), key = lambda v: v['pos'])] 
    for c_id in sorted_ids:
        # skip crashed carts
        if c_id in crashed_carts:
            continue
        
        # current info
        c_info = data['carts_info'][c_id]
        y, x = c_info['pos']
        c_direction = c_info['current_direction']
        
        # new position
        step = {'>': (1,0), '<': (-1,0), '^': (0,-1), 'v': (0,1)}[c_direction]
        new_x = x + step[0]
        new_y = y + step[1]
        c_info['pos'] = (new_y,new_x)
        
        # check for crash
        if carts_array[new_y][new_x] != 0:
            c_id_into = carts_array[new_y][new_x]
            print('cart', c_id, 'CRASHED into cart', c_id_into, 'at location', f"{new_x},{new_y}")
            crashed_carts.add(c_id)
            crashed_carts.add(c_id_into)
            if remove_crashed:
                # remove crashed (for part 2)
                del data['carts_info'][c_id]
                del data['carts_info'][c_id_into]
            else:
                # stop at first crash
                break
        else:
            # no crash, update the direction of the cart
            # based on the track at the new position
            new_track_value = chr(data['track'][new_y][new_x])
            turn_cart(c_info, new_track_value)
            
            # modify the carts_array for the next loop
            carts_array[new_y][new_x] = c_id
            carts_array[y][x] = 0
            
    return data, crashed_carts

def turn_cart(cart_info, current_track):
    current_dir = cart_info['current_direction']
    if current_track == '+':
        # intersection
        turn_cart_intersection(cart_info)
    elif current_track in '|-':
        pass # keep going straight
    else:
        # at corner of track
        # Depending on the current_track and current_direction
        # We need to turn a particular way
        turn = {
            '/':  {'^': RIGHT, 'v': RIGHT, '>': LEFT, '<': LEFT},
            '\\': {'v': LEFT, '^': LEFT, '>': RIGHT, '<': RIGHT},
        }[current_track][current_dir]
        cart_info['current_direction'] = get_turned_direction(current_dir, turn)

def turn_cart_intersection(cart_info):
    """Turn a cart that is currently at an intersection."""
    turn_order = cart_info['num_turns'] % 3 # we cycle through the turning orders
    current_dir = cart_info['current_direction']
    
    if turn_order == 0:
        new_dir = get_turned_direction(current_dir, LEFT)
    elif turn_order == 1:
        new_dir = current_dir # straight    
    elif turn_order == 2:
        new_dir = get_turned_direction(current_dir, RIGHT)
        
    cart_info['current_direction'] = new_dir
    cart_info['num_turns'] += 1

def get_turned_direction(current, left_or_right):
    """Lookup for result of turning the 'current' direction to LEFT or RIGHT."""
    return {
        ('<', LEFT): 'v',
        ('<', RIGHT): '^',
        ('^', LEFT): '<',
        ('^', RIGHT): '>',
        ('>', LEFT): '^',
        ('>', RIGHT): 'v',
        ('v', LEFT): '>',
        ('v', RIGHT): '<',
    }[(current, left_or_right)]


def parse(txt_data):
    # defines the underlying track
    # for a cart read from the input
    carts_to_track = {
        '>': '-',
        '<': '-',
        '^': '|',
        'v': '|',
    }
    
    data = {}
    elements = []
    data['carts_info'] = carts_info = {}
    for y, line in enumerate(txt_data.splitlines()):
        for x, c in enumerate(line):
            if c:
                if c in '><^v':
                    c_id = len(carts_info)+1
                    carts_info[c_id] = {
                        'id': c_id,
                        'current_direction': c, 
                         # we make y first so we can later easier sort
                         # in the order they should move
                        'pos': (y, x),
                        'num_turns': 0,
                    }
                    
                    # replace the cart with a underlying track
                    c = carts_to_track[c]
                elements.append((x,y,c))
    
    # create track of 2D array
    max_x = max(t[0] for t in elements)
    max_y = max(t[1] for t in elements)
    data['track'] = track = np.ndarray((max_y+1, max_x+1), dtype=np.int8)
    track[:] = 0
    for x, y, c in elements:
        track[y][x] = ord(c)
    
    return data

def print_track(data, carts_encode = 'direction'):
    track_array = data['track']
    if carts_encode:
        carts_array = compute_carts_array(data, carts_encode)
        track_array = np.where(carts_array > 0, carts_array, track_array)
    print_raw_track(track_array)

def print_raw_track(track_array):
    for r in track_array:
        try:
            print("".join([chr(c) for c in r]))
        except ValueError:
            print(r)
        
def compute_carts_array(data, encode = 'id'):
    carts_array = np.zeros_like(data['track'], dtype=np.int32)
    for c_id, c in data['carts_info'].items():
        y,x = c['pos']
        carts_array[y][x] = {'id': c_id, 'direction': ord(c['current_direction'])}[encode]
    return carts_array






def split_blocks(raw_txt):
    data_steps = [[]]
    current_block = data_steps[-1]
    for l in raw_txt.splitlines():
        if not l.strip(): # empty line start new block
            data_steps.append([])
            current_block = data_steps[-1]
        else:
            current_block.append(l)

    data = ["\n".join(l for l in block) for block in data_steps if block]
    return data


if __name__ == "__main__":
    main()