"""
Advent of Code 2023 - Day 04
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def parse(data):
    for card_i, line in enumerate(data.splitlines()):
        numbers = line.split(":")[1].split("|")
        winning = set(map(int, numbers[0].split()))
        own_numbers = set(map(int, numbers[1].split()))
        valid = own_numbers.intersection(winning)
        yield card_i + 1, valid


from collections import Counter, defaultdict


def solve(data, part2=False):
    if not part2:
        result = 0
        for card_i, valid in parse(data):
            if valid:
                card_score = 2 ** (len(valid) - 1) if len(valid) > 1 else 1
                result += card_score
    else:
        cards_num_win = {card_i: len(valid) for card_i, valid in parse(data)}
        total_cards = Counter(cards_num_win.keys())
        for card_i in sorted(cards_num_win.keys()):
            num_win = cards_num_win[card_i]
            for card_j in range(card_i + 1, card_i + 1 + num_win):
                total_cards[card_j] += total_cards[card_i]
        result = sum(total_cards.values())

    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 13


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 22897


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 30


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 5095824


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
