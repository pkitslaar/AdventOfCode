"""
Advent of Code 2020 - Day 22
Pieter Kitslaar
"""
from pathlib import Path
from collections import deque

example="""\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

def parse(txt):
    decks = {}
    current_deck = None
    for line in txt.splitlines():
        if not line.strip():
            continue
        elif line.startswith('Player '):
            current_deck = decks[int(line[7])] = deque()
        else:
            current_deck.append(int(line))
    return decks

def play_round(decks):
    top_cards = {deck.popleft():player for player,deck in decks.items()}
    higest_card = max(top_cards)
    winning_player = top_cards[higest_card]
    decks[winning_player].extend(sorted(top_cards, reverse=True))
    return decks

def winning_score(decks):
    winning_deck = [d for d in decks.values() if len(d) != 0][0]
    score = sum([v*(m+1) for m,v in enumerate(reversed(winning_deck))])
    return score


def play_part1(txt):
    decks = parse(txt)
    round_number = 0
    while all(len(d) > 0 for d in decks.values()):
        round_number += 1
        play_round(decks)
    score = winning_score(decks)
    return score

def test_example():
    score = play_part1(example)
    assert(306 == score)

def get_input(name='input.txt'):
    with open(Path(__file__).parent / name, 'r') as f:
        return f.read()   
    
def test_puzzle():
    score = play_part1(get_input())
    print('Part 1:', score)
    assert(32815 == score)

def top_card(deck):
    for c in deck:
        return c

def play_part2(decks, game=1):
    round_number = 0
    previous_round_decks = set()
    while all(len(d) > 0 for d in decks.values()):
        round_number += 1
        immutable_deck = tuple([(p,tuple(d)) for p,d in decks.items()])
        if previous_round_decks and immutable_deck in previous_round_decks:
            # found loop in configuration player 1 wins!
            return [1,2]
        elif any(len(d) < (top_card(d) +1) for d in decks.values()):
            # normal play
            play_round(decks)
        else:
            # recursion
            top_cards = {p:d.popleft() for p,d in decks.items()}

            # play recursive game
            new_decks = {p:deque(list(d)[:top_cards[p]]) for p,d in decks.items() }
            player_ranks = play_part2(new_decks, game=game+1)

            # put card at bottom of winners deck
            winning_player = player_ranks[0]
            decks[winning_player].extend([top_cards[p] for p in player_ranks])
        previous_round_decks.add(immutable_deck)

    players_rank = [t[0] for t in sorted(decks.items(), key=lambda t:t[1], reverse=True)]
    return players_rank

def test_example2():
    decks = parse(example)
    player_ranks = play_part2(decks)
    assert(2 == player_ranks[0])
    score = winning_score(decks)
    assert(291 == score)

def test_puzzle2():
    decks = parse(get_input())
    player_ranks = play_part2(decks)
    score = winning_score(decks)
    print('Part 2:', score)
    assert(30695 == score)

if __name__ == "__main__":
    test_example()
    test_puzzle()
    test_example2()
    test_puzzle2()