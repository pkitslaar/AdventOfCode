"""
Advent of Code 2021 - Day 21
Pieter Kitslaar
"""

from pathlib import Path

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

example = """\
Player 1 starting position: 4
Player 2 starting position: 8"""

def parse(txt):
    positions = []
    for line in txt.splitlines():
        pos = int(line.strip().split(':')[-1])
        positions.append(pos)
    return positions

class DeterministicDice():
    def __init__(self,N=100):
        self.num_rolls = 0
        self.N = N
        self.value = 1
    
    def roll(self):
        self.num_rolls +=1
        v = self.value
        if v >= self.N:
            self.value = 1
        else:
            self.value += 1
        return v

def game(positions):
    dice = DeterministicDice()
    num_players = len(positions)
    scores = [0]*num_players
    turns = [0]*num_players
    
    has_winner = False
    while not has_winner:
        for i in range(num_players):
            turns[i]+=1
            steps = dice.roll()+dice.roll()+dice.roll()
             # compensate for zero-indexing
            new_pos = ((positions[i]-1+steps) % 10)+1
            scores[i] += new_pos
            positions[i] = new_pos
            if scores[i] >= 1000:
                has_winner = True
                break
    return min(scores)*dice.num_rolls
                
def test_example():
    result = game(parse(example))
    assert 739785 == result

def test_part1():
    result = game(parse(get_input()))
    print('Part 1', result)
    assert 920079 == result

from itertools import product
from collections import Counter
DIRAC_STEPS_COUNT = Counter(a+b+c for a,b,c in product([1,2,3],[1,2,3],[1,2,3]))
POS_TO_NEW_POS = {}
for pos in range(1,11):
    steps_to_new_pos = {}
    for steps in DIRAC_STEPS_COUNT:
        steps_to_new_pos[steps] = (((pos-1)+steps)%10)+1
    POS_TO_NEW_POS[pos] = steps_to_new_pos


from collections import namedtuple
GameState = namedtuple('GameState', 'score0 score1 position0 position1 nextPlayer')

def game2(positions):
    # dict per player with number of games per position
    wins = [0, 0]

    current_games = {
        # scores
        GameState(0,0,positions[0], positions[1], 0): 1
    }
    while current_games:
        new_games = {}
        for g, g_count in current_games.items():
            g_scores = [g.score0, g.score1]
            g_positions = [g.position0, g.position1]
            p_index = g.nextPlayer
            p_pos = g_positions[p_index]
            for steps, dirac_count in DIRAC_STEPS_COUNT.items():
                new_count = g_count*dirac_count
                new_pos = POS_TO_NEW_POS[p_pos][steps]
                new_score = g_scores[:]
                new_score[p_index] += new_pos
                if new_score[p_index] >= 21:
                    wins[p_index] += new_count
                else:
                    new_positions = g_positions[:]
                    new_positions[p_index] = new_pos
                    new_game = GameState(
                        score0=new_score[0], 
                        score1=new_score[1],
                        position0=new_positions[0],
                        position1=new_positions[1],
                        nextPlayer=int(not p_index)
                    )
                    new_games[new_game] = new_games.get(new_game, 0) + new_count
        current_games = new_games

    return wins

def test_example2():
    wins = game2(parse(example))
    assert wins[0] == 444356092776315
    assert wins[1] == 341960390180808

def test_part2():
    wins = game2(parse(get_input()))
    result = max(wins)
    print('Part 2', result)  
    assert 56852759190649 == result


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()