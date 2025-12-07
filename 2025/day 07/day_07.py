"""
Advent of Code 2025 - Day 07
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

from functools import reduce
from collections import Counter


def solve(data, part2=False):
    grid = {}
    start = None
    for row_idx, line in enumerate(data.splitlines()):
        for col_idx, char in enumerate(line):
            if char in ("^", "S"):
                if char == "S":
                    start = (row_idx, col_idx)
                else:
                    grid.setdefault(row_idx, {})[col_idx] = char

    num_rows = row_idx + 1
    row_beams = {start[0] + 1: {start[1]: [start]}}
    num_splits = 0
    beam_timelines = Counter()
    beam_timelines[(start[0] + 1, start[1])] = 1
    for row in range(start[0] + 2, num_rows):
        prev_rows_beams = row_beams[row - 1]
        row_splitter_columns = [*grid.get(row, {}).keys()]
        new_row_beams = {}
        for beam_col in prev_rows_beams:
            if beam_col in row_splitter_columns:
                num_splits += 1
                # split left
                new_row_beams.setdefault(beam_col - 1, []).append((row - 1, beam_col))
                beam_timelines[(row, beam_col - 1)] += beam_timelines[
                    (row - 1, beam_col)
                ]

                # split right
                new_row_beams.setdefault(beam_col + 1, []).append((row - 1, beam_col))
                beam_timelines[(row, beam_col + 1)] += beam_timelines[
                    (row - 1, beam_col)
                ]
            else:
                # continue straight
                new_row_beams.setdefault(beam_col, []).append((row - 1, beam_col))
                beam_timelines[(row, beam_col)] += beam_timelines[(row - 1, beam_col)]

        row_beams[row] = new_row_beams

    if not part2:
        return num_splits

    result = 0
    for beam_col in row_beams[num_rows - 1].keys():
        num_timelies = beam_timelines[(num_rows - 1, beam_col)]
        result += num_timelies
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 21


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 1615


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 40


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 43560947406326


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
