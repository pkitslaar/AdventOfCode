"""
Advent of Code 2022 - Day 02
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

# values
ROCK = 1
PAPER = 2
SCISSORS = 3

# outcomes
LOSE = 0
DRAW = 3
WIN = 6

#
OP_SHAPES = {'A': ROCK, 'B': PAPER, 'C': SCISSORS}

MY_SHAPES = {'X': ROCK, 'Y': PAPER, 'Z': SCISSORS}

RULES = {
    # my   op
    (ROCK, PAPER): LOSE,
    (ROCK, SCISSORS): WIN,
    (PAPER, ROCK): WIN,
    (PAPER, SCISSORS): LOSE,
    (SCISSORS, ROCK): LOSE,
    (SCISSORS, PAPER): WIN
}
RULES.update({(S,S):DRAW for S in (ROCK, PAPER, SCISSORS)})

def my_score_round(my_shape, op_shape):
    rule_score = RULES[(my_shape, op_shape)]
    return my_shape + rule_score

EXAMPLE_DATA="""\
A Y
B X
C Z"""

def solve(d):
    sum = 0
    for line in d.strip().splitlines():
        op_code, my_code = line.split()
        my_shape = MY_SHAPES[my_code]
        op_shape = OP_SHAPES[op_code]
        sum += my_score_round(my_shape, op_shape)
    return sum

def test_example():
    score = solve(EXAMPLE_DATA)
    assert(15 == score)
    
def test_part1():
    score = solve(data())
    print('PART 1:', score)
    assert(11666 == score)

#
SHAPE_TO_RESULT = {}
for shapeA in (ROCK, PAPER, SCISSORS):
    for wanted_result in (LOSE, DRAW, WIN):
        for shapeB in (ROCK, PAPER, SCISSORS):
            this_result = RULES[(shapeB, shapeA)]
            if this_result ==  wanted_result:
                SHAPE_TO_RESULT.setdefault(shapeA, {})[wanted_result] = shapeB
                break

def solve2(d):
    RESULT_CODE = {'X': LOSE, 'Y': DRAW, 'Z': WIN}
    sum = 0
    for line in d.strip().splitlines():
        op_code, result_code = line.split()
        op_shape = OP_SHAPES[op_code]
        wanted_result = RESULT_CODE[result_code]
        my_shape = SHAPE_TO_RESULT[op_shape][wanted_result]
        sum += wanted_result + my_shape
    return sum

def test_example2():
    score = solve2(EXAMPLE_DATA)
    assert(12 == score)

def test_part2():
    score = solve2(data())
    print('PART 2:', score)
    assert(12767 == score)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()