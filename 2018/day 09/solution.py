# Advent of code - 2018
# Day 9
#
# Pieter Kitslaar
#

import itertools
from collections import deque, defaultdict
import time

# Using a deque is much faster than 
#a list (goes from hours to seconds), trust me I have tried...
DEQUE = True 
circle_container = deque if DEQUE else list

def play_round(num_players):
    info = dict(
        player = '-', 
        marble = 0,
        circle = circle_container([0]),
        current = 0, # only needed for list solution, and printing for deque
        player_scores = defaultdict(int)
    )
    yield info
    circle = info['circle']
    while True:
        for player in range(1, num_players+1):
            info['player'] = player
            info['marble'] += 1
            marble = info['marble']
            if marble % 23 == 0:
                if not DEQUE:
                    # list 
                    remove_position = info['current']-7
                    if remove_position < 0:
                        remove_position += len(circle)
                    removed_marble = circle.pop(remove_position)
                    info['current'] = remove_position
                else:
                    # deque
                    circle.rotate(7)
                    removed_marble = circle.pop()
                    circle.rotate(-1)
                    info['current'] = len(circle)-1 # always last as current

                info['player_scores'][player] += marble + removed_marble
            else:
                if not DEQUE:
                    # list
                    insert_pos = (info['current']+1) % len(circle)
                    circle.insert(insert_pos+1, marble)
                    info['current'] = (insert_pos+1) % len(circle)
                else:
                    # deque
                    circle.rotate(-1)
                    circle.append(marble)
                    info['current'] = len(circle)-1  # always last as current
            yield info

def game(num_players, last_marble, debug_print = False):
    last_percentage = 0
    last_processed = 0
    last_time = time.clock()
    for r in play_round(num_players):
        if debug_print:
            circle = r['circle']
            current = r['current']
            formats = ['{0:^4}']*len(circle)
            formats[current] = '({0:^2})'
            circle_text = "".join([f.format(c) for f,c in zip(formats, circle)])
            print(r['player'], circle_text)
            
        # print percentages
        percentage = 100*(r['marble']/last_marble)
        if (percentage - last_percentage) > 1:
            # Compute performance statistics
            current_time = time.clock()
            current_processed = r['marble']
            num_processed = current_processed-last_processed
            speed = int(num_processed/(current_time - last_time)+0.5)
            num_left = last_marble - r['marble']
            estimated_time_left = num_left/speed
            estimated_time_unit = 'seconds'
            for divider, unit in [(60, 'minutes'), (60, 'hours'), (24, 'days')]:
                if estimated_time_left / divider > 1:
                    estimated_time_left /= divider
                    estimated_time_unit = unit
                else:
                    break
                    
            print(r['marble'], last_marble, f"{percentage:.0f}%", 
                  f"speed {speed} marbles/s, estimated time left {estimated_time_left:.1f}", 
                  estimated_time_unit)
                    
            last_percentage = percentage
            last_processed = current_processed
            last_time = current_time
                
        if r['marble'] == last_marble:
            break
         
    high_score = max(r['player_scores'].values()) 
    print(num_players, 'players', 'last_marble:', last_marble, 'high_score:', high_score)
    return high_score

# check examples
assert(game(9, 25, True) == 32)
assert(game(10, 1618) == 8317)
assert(game(13, 7999) == 146373) 
assert(game(17, 1104) == 2764)
assert(game(21, 6111) == 54718)
assert(game(30, 5807) == 37305)

# PART 1: 426 players; last marble is worth 72058 points
print('PART 1:')
game(426, 72058)

# PART 2: 426 players; last marble is worth 72058*100 points
# 100 times more points makes the list unworkable, but
# the deque performs fine.
# Insertion and deletion in list is O(n) but deque is O(1)
print('PART 2:')
game(426, 72058*100)
      
