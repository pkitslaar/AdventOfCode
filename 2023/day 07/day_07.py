"""
Advent of Code 2023 - Day 07
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
from enum import Enum
from collections import Counter
from functools import total_ordering
from typing import Any

HandTypes = Enum(
    "HandTypes",
    "Unknown HighCard OnePair TwoPair ThreeOfAKind FullHouse FourOfAKind FiveOfAKind",
)


@total_ordering
class HandBase:
    CARD_VALUES = None

    def __init__(self, cards: str):
        self.cards: str = cards
        self.values = tuple([self.CARD_VALUES[c] for c in cards])
        self.card_counts = Counter(cards)
        self.kind = self._compute_kind()

    def __repr__(self) -> str:
        return f"Hand({self.cards})"

    def __lt__(self, other):
        if self.kind.value > other.kind.value:  # type: ignore
            return False
        if self.kind.value == other.kind.value:
            return self.values < other.values
        return True

    def __eq__(self, other) -> bool:
        if self.kind == other.kind:
            return self.values == other.values
        return False

    def _compute_kind(self):
        s_count = tuple(sorted(self.card_counts.values(), reverse=True))
        match s_count:
            case (5,):
                return HandTypes.FiveOfAKind
            case (4, 1):
                return HandTypes.FourOfAKind
            case (3, 2):
                return HandTypes.FullHouse
            case (3, 1, 1):
                return HandTypes.ThreeOfAKind
            case (2, 2, 1):
                return HandTypes.TwoPair
            case (2, 1, 1, 1):
                return HandTypes.OnePair
            case (1, 1, 1, 1, 1):
                return HandTypes.HighCard
            case _:
                return HandTypes.Unknown


class Hand(HandBase):
    CARD_VALUES = {c: v for v, c in enumerate("23456789TJQKA")}

    def _compute_kind(self):
        s_count = tuple(sorted(self.card_counts.values(), reverse=True))
        match s_count:
            case (5,):
                return HandTypes.FiveOfAKind
            case (4, 1):
                return HandTypes.FourOfAKind
            case (3, 2):
                return HandTypes.FullHouse
            case (3, 1, 1):
                return HandTypes.ThreeOfAKind
            case (2, 2, 1):
                return HandTypes.TwoPair
            case (2, 1, 1, 1):
                return HandTypes.OnePair
            case (1, 1, 1, 1, 1):
                return HandTypes.HighCard
            case _:
                return HandTypes.Unknown


def test_hand():
    a = Hand("23456")
    assert a.kind == HandTypes.HighCard
    assert Hand("23456") == Hand("23456")
    b = Hand("23467")
    assert b.kind == HandTypes.HighCard
    assert a < b
    c = Hand("22456")
    assert c.kind == HandTypes.OnePair
    assert c > b


def solve(data, part2=False):
    H = Hand2 if part2 else Hand
    hand_bids = []
    for line in data.splitlines():
        cards, bid = line.split()
        hand_bids.append((H(cards), int(bid)))
    hand_bids.sort()
    result = sum((rank + 1) * bid for rank, (_, bid) in enumerate(hand_bids))
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 6440


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 250120186


class Hand2(HandBase):
    CARD_VALUES = {c: v for v, c in enumerate("J23456789TQKA")}

    def _compute_kind(self):
        s_count = tuple(sorted(self.card_counts.values(), reverse=True))
        j_count = self.card_counts["J"]
        match s_count:
            case (5,):
                return HandTypes.FiveOfAKind
            case (4, 1):
                if j_count == 1 or j_count == 4:
                    return HandTypes.FiveOfAKind
                return HandTypes.FourOfAKind
            case (3, 2):
                if j_count == 2 or j_count == 3:
                    return HandTypes.FiveOfAKind
                return HandTypes.FullHouse
            case (3, 1, 1):
                if j_count == 1 or j_count == 3:
                    return HandTypes.FourOfAKind
                return HandTypes.ThreeOfAKind
            case (2, 2, 1):
                if j_count == 1:
                    return HandTypes.FullHouse
                elif j_count == 2:
                    return HandTypes.FourOfAKind
                return HandTypes.TwoPair
            case (2, 1, 1, 1):
                if j_count == 1 or j_count == 2:
                    return HandTypes.ThreeOfAKind
                return HandTypes.OnePair
            case (1, 1, 1, 1, 1):
                if j_count == 1:
                    return HandTypes.OnePair
                return HandTypes.HighCard
            case _:
                return HandTypes.Unknown


def test_hand2():
    assert Hand2("23456").kind == HandTypes.HighCard
    assert Hand2("2345J").kind == HandTypes.OnePair

    assert Hand2("22456").kind == HandTypes.OnePair
    assert Hand2("2245J").kind == HandTypes.ThreeOfAKind

    assert Hand2("22445").kind == HandTypes.TwoPair
    assert Hand2("2244J").kind == HandTypes.FullHouse
    assert Hand2("22JJ4").kind == HandTypes.FourOfAKind

    assert Hand2("22245").kind == HandTypes.ThreeOfAKind
    assert Hand2("2224J").kind == HandTypes.FourOfAKind
    assert Hand2("JJJ45").kind == HandTypes.FourOfAKind

    assert Hand2("2244J").kind == HandTypes.FullHouse


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 5905


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 250665248


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
