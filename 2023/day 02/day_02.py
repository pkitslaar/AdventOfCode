"""
Advent of Code 2023 - Day 02
Pieter Kitslaar
"""
from pathlib import Path

THIS_DIR = Path(__file__).parent

from collections import defaultdict, Counter
from functools import reduce


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()


EXAMPLE_DATA = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def parse(data):
    for line in data.splitlines():
        game_id = int(line.split(":")[0].split()[-1])
        for reveal_set in line.split(":")[1].split(";"):
            for cubes in reveal_set.split(","):
                count_str, color = cubes.split()
                yield game_id, color, int(count_str)


def solve(data, part2=False):

    # count the maximum number of cubes of each color in each game
    game_color_count = defaultdict(Counter)
    for game_id, color, count in parse(data):
        if count > game_color_count[game_id][color]:
            game_color_count[game_id][color] = count

    if not part2:
        max_expected = Counter({"red": 12, "green": 13, "blue": 14})

        # find games that have more cubes than expected
        impossible_games = set()
        for game_id, game_set in game_color_count.items():
            if any(game_set[color] > max_expected[color] for color in game_set):
                impossible_games.add(game_id)

        possible_games = set(game_color_count) - impossible_games
        return sum(possible_games)

    # multiple the maximum number of cubes of each color in each game
    powers = [
        reduce(lambda a, b: a * b, game_set.values())
        for game_set in game_color_count.values()
    ]
    return sum(powers)


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 8


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 2207


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 2286


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 62241
