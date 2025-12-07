"""
Advent of Code 2025 - Day 06
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +
"""

from functools import reduce


def solve(data, part2=False):
    result = 0

    grid = [line for line in data.splitlines()]
    num_rows = len(grid)
    num_cols = max(len(line) for line in grid)
    # make all lines equal length
    grid = [f"{line: <{num_cols}}" for line in grid]

    # find the split columns between problems
    split_columns = [-1]
    for col in range(num_cols):
        all_col = [grid[row][col] for row in range(num_rows)]
        if all(c == " " for c in all_col):
            split_columns.append(col)
    split_columns.append(num_cols)

    # extract problems
    problems = []
    for i in range(len(split_columns) - 1):
        prev_col = split_columns[i]
        next_col = split_columns[i + 1]
        col_values = []
        for row in range(num_rows):
            col_values.append([grid[row][c] for c in range(prev_col + 1, next_col)])
        problems.append(col_values)

    func_tabel = {
        "*": lambda vals: reduce(lambda x, y: x * y, vals),
        "+": lambda vals: sum(vals),
    }

    for problem_lines in problems:
        if not part2:
            # take rows as values
            values = [int("".join(line).strip()) for line in problem_lines[:-1]]
        else:
            # take columns as values
            values = []
            num_cols = len(problem_lines[0])
            for col in range(num_cols):
                col_value = [
                    problem_lines[row][col] for row in range(len(problem_lines) - 1)
                ]
                values.append(int("".join(col_value).strip()))
        # math symbol
        symbol = "".join(problem_lines[-1]).strip()
        result += func_tabel[symbol](values)

    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 4277556


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 5782351442566


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 3263827


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 10194584711842


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
