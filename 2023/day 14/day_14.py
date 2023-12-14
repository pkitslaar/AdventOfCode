"""
Advent of Code 2023 - Day 14
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def to_rows(data):
    return [r.strip() for r in data.splitlines() if r.strip()]


def total_load(data):
    rows_west = to_rows(data)
    # now the rows are NORTH orientated
    result = 0
    # north is left side of the columns
    for value, row in zip(range(len(rows_west), 0, -1), rows_west):
        result += value * row.count("O")
    return result


def solve(data, part2=False):
    rows_west = to_rows(data)

    # currently the rows are WEST orientated, e.g. the left side if to the west
    # to tilt NORTH we need to rotate the rows 90 degrees clockwise
    rows_north = ["".join(row) for row in zip(*rows_west)]
    rows_north = [tilt_left(row) for row in rows_north]

    rows_west = ["".join(row) for row in zip(*rows_north)]
    result = total_load("\n".join(rows_west))
    return result


def tilt_left(row):
    new_row = []
    prev_fixed = -1
    for i, c in enumerate(row):
        if c == ".":
            new_row.append(c)
        if c == "#":
            prev_fixed = i
            new_row.append(c)
        if c == "O":
            if i - prev_fixed > 1:
                new_row.append(".")
                new_row[prev_fixed + 1] = "O"
                prev_fixed = prev_fixed + 1
            else:
                new_row.append(c)
                prev_fixed = i
    return "".join(new_row)


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 136


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 109833


def tilt_right(row):
    return tilt_left(row[::-1])[::-1]


def run_cyle(data):
    rows_west = to_rows(data)
    # first NORTH
    rows_north = ["".join(row) for row in zip(*rows_west)]
    rows_north = [tilt_left(row) for row in rows_north]

    # now WEST
    rows_west = ["".join(row) for row in zip(*rows_north)]
    rows_west = [tilt_left(row) for row in rows_west]

    # now SOUTH, we still orient to NORTH but title to right
    rows_north = ["".join(row) for row in zip(*rows_west)]
    rows_north = [tilt_right(row) for row in rows_north]

    # now EAST, we still orient WEST but title to right
    rows_west = ["".join(row) for row in zip(*rows_north)]
    rows_west = [tilt_right(row) for row in rows_west]
    return "\n".join(rows_west)


EXAMPLE_DATA_CYCLE_1 = """\
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""

EXAMPLE_DATA_CYCLE_2 = """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""

EXAMPLE_DATA_CYCLE_3 = """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""


def test_run_cycle():
    rw_1 = run_cyle(EXAMPLE_DATA)
    assert rw_1 == EXAMPLE_DATA_CYCLE_1
    rw_2 = run_cyle(rw_1)
    assert rw_2 == EXAMPLE_DATA_CYCLE_2
    rw_3 = run_cyle(rw_2)
    assert rw_3 == EXAMPLE_DATA_CYCLE_3


def solve2(data):
    N = 1_000_000_000

    current = data
    # prime the dictionary with the starting value
    prev_runs = {hash(current): (0, total_load(current))}

    for i in range(1, N + 1):
        new_data = run_cyle(current)
        n_hash = hash(new_data)
        try:
            existing_i, existing_load = prev_runs[n_hash]
            print(f"found cycle at {i=} with {existing_i=} and {existing_load=}")
            break
        except KeyError:
            prev_runs[n_hash] = (i, total_load(new_data))
        current = new_data

    # now we have found a the repeating cycle, we can compute the final load
    cycle_start = existing_i
    cycle_end = i
    cycle_length = cycle_end - cycle_start

    # final cycle number)
    final_cycle = cycle_start + ((N - cycle_start) % cycle_length)

    # find the value in the dictionary
    for (i, load) in prev_runs.values():
        if i == final_cycle:
            return load


def test_example2():
    result = solve2(EXAMPLE_DATA)
    print(f"example 2: {result}")
    assert result == 64


def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result == 99875


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
