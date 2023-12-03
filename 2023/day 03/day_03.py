"""
Advent of Code 2023 - Day 03
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

from collections import OrderedDict
from itertools import groupby


def solve(data, part2=False):
    schematic_words = {}
    schematic_chars = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c != ".":
                schematic_chars[(x, y)] = c

                if not c.isdigit():
                    continue

                new_word = c
                # when adjacent to a previous word
                # append previous word, and remove the previous word
                if schematic_words.get((x - 1, y)):
                    new_word = schematic_words[(x - 1, y)] + c
                    del schematic_words[(x - 1, y)]

                schematic_words[(x, y)] = new_word

    # set the x coordinate to the start of the word for easier looping
    schematic_words = dict(
        ((x - len(w) + 1, y), w) for ((x, y), w) in schematic_words.items()
    )

    # find words not adjacent to a symbol
    NEIGHBORS = [
        (dx, dy)
        for dx in range(-1, 2)
        for dy in range(-1, 2)
        if not (dx == 0 and dy == 0)
    ]

    def is_adjacent_to_symbol(x, y, word):
        for wx in range(x, x + len(word)):
            for dx, dy in NEIGHBORS:
                n_char = schematic_chars.get((wx + dx, y + dy))
                if n_char and not n_char.isdigit():
                    return True
        return False

    part_numbers = []
    for (x, y), word in schematic_words.items():
        if is_adjacent_to_symbol(x, y, word):
            part_numbers.append(((x, y), word))

    if not part2:
        result = sum(int(n) for _, n in part_numbers)
        return result

    # part 2
    schematic_parts = {}
    for (x, y), word in schematic_words.items():
        for dx, c in enumerate(word):
            # we store the full word and coordinate at
            # the position of each character in the part
            # this allows us to easily find the parts
            schematic_parts[(x + dx, y)] = ((x, y), word)

    gear_rations = []
    for (x, y), c in schematic_chars.items():
        if c == "*":  # gear symbol
            part_numbers = set()
            for dx, dy in NEIGHBORS:
                try:
                    part_numbers.add(schematic_parts[(x + dx, y + dy)])
                except KeyError:
                    pass
            if len(part_numbers) == 2:
                # found a gear symbol between two parts
                # add their gear ratio to the list
                part1, part2 = part_numbers
                gear_rations.append(int(part1[1]) * int(part2[1]))

    result = sum(gear_rations)
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 4361


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 550064


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 467835


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 85010461


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
