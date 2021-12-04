"""
Advent of Code 2021 - Day 04
Pieter Kitslaar
"""

from pathlib import Path

example="""\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

def parse(txt):
    numbers = []
    board_numbers = []
    current_board_numbers = None
    for line in txt.splitlines():
        if not line.strip():
            current_board_numbers = None
        elif not numbers:
             numbers = list(map(int, line.split(",")))
        else:
            if current_board_numbers is None:
                board_numbers.append([])
                current_board_numbers = board_numbers[-1]
            current_board_numbers.append(list(map(int, line.split())))
    boards = []
    for bn in board_numbers:
        board = {}
        for irow, row in enumerate(bn):
            for icol, value in enumerate(row):
                board[value] = {'row': irow, 'col': icol, 'marked': False}
        boards.append(board)
    return numbers, irow+1, boards

def bingo(board, N=5):
    for direction in ('row', 'col'):
        for i in range(N):
            marked = [v for v, info in board.items() if info[direction] == i if info['marked']]
            if len(marked) == N:
                return True
    return False

def mark(board, value):
    try:
        value_info = board[value]
        value_info['marked'] = True
    except KeyError:
        pass
    return False

def test_parse():
    numbers, N, boards = parse(example)
    assert 5 == N

def play(numbers, N, boards):
    win_order = []
    for i, n in enumerate(numbers):
        new_boards = []
        for b in boards:
            mark(b, n)
            if bingo(b, N):
                win_order.append((b, n))
            else:
                new_boards.append(b)
        boards = new_boards
    return win_order

def score(board, last_played):
    unmarked = [v for v, info in board.items() if not info['marked']]
    return sum(unmarked)*last_played

def test_example():
    result = score(*play(*parse(example))[0])
    assert 4512 == result

def get_input():
    input_numbers = []
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    result = score(*play(*parse(get_input()))[0])
    print('Part 1:', result)
    assert 16674 == result

def test_example2():
    result = score(*play(*parse(example))[-1])
    assert 1924 == result

def test_part2():
    result = score(*play(*parse(get_input()))[-1])
    print('Part 2:', result)
    assert 7075 == result

if __name__ == "__main__":
    test_parse()    
    test_example()
    test_part1()
    test_example2()
    test_part2()
        