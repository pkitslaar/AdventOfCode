"""
Advent of Code 2020 - Day 23
Pieter Kitslaar
"""

from collections import deque
import tqdm

def create_cups2(input_value):
    """Create a linked-list of cups where each entry points to the one next to it (clock wise).
    We use 1-based indexing for easier indexing with labels.

    cups[1] = 5  means clockwise from 1 is 5
    """
    cup_labels = list(map(int, input_value)) if isinstance(input_value, str) else input_value
    cups = [-1]*(len(cup_labels)+1)
    prev_cup = cup_labels[-1]
    for c in cup_labels:
        cups[prev_cup] = c
        prev_cup = c

    return cups, cup_labels[0]

def cups2_to_txt(cups2):
    cup_lables = [1]
    while len(cup_lables) + 1 < len(cups2):
        cup_lables.append(cups2[cup_lables[-1]])
    return cup_lables

def play_round2(cups, current):
    max_cup_label = len(cups)-1
    
    pickup = []
    prev = current
    for i in range(3):
        pickup.append(cups[prev])
        prev = pickup[-1]

    next_current = cups[pickup[-1]]
    cups[current] = next_current
    
    destination = (current - 1) or max_cup_label
    while destination in pickup:
        destination = (destination - 1) or max_cup_label

    current_next_to_destination = cups[destination]
    cups[destination] = pickup[0]
    cups[pickup[-1]] = current_next_to_destination
    return next_current

def play_game2(input_value, num_rounds, return_cups=False, show_progress=False):
    cups, current = create_cups2(input_value)
    for i in tqdm.tqdm(range(num_rounds)) if show_progress else range(num_rounds):
        current = play_round2(cups, current)
    if return_cups:
        return cups
    return ''.join(map(str, cups2_to_txt(cups)))[1:]

def test_example():
    assert('92658374' == play_game2('389125467', 10))
    assert('67384529' == play_game2('389125467', 100))    

def solve2(txt):
    more_cups = list(map(int,txt))
    more_cups.extend(range(10, 1_000_001))
    cups = play_game2(more_cups, 10_000_000, return_cups=True, show_progress=True)
    first_value = cups[1]
    second_value = cups[first_value]
    return first_value*second_value

def test_example2():
    assert(149245887792 == solve2('389125467'))

def test_puzzle():
    answer = play_game2('589174263', 100)
    print('Part 1:', answer)
    assert('43896725' == answer)
    
    answer = solve2('589174263')
    print('Part 2:', answer)
    assert(2911418906 == answer)

if __name__ == "__main__":
    test_example()
    test_example2()
    test_puzzle()
