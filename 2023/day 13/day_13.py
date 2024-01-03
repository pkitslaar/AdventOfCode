"""
Advent of Code 2023 - Day 13
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def parse(data):
    pattern = []
    for line in data.splitlines():
        if not line:
            yield pattern
            pattern = []
            continue
        pattern.append(line)
    yield pattern


def compute_n_horizon(pattern, part2=False, prev_reflection=[]):
    n_horizon = []
    fixed_smudge = False
    for i in range(len(pattern)):
        this_n = 0
        top = [*reversed(pattern[:i])]
        bottom = pattern[i:]

        smudge_original = {}

        for j, (above, below) in enumerate(zip(top, bottom)):
            if above == below:
                this_n += 1
            else:
                if part2 and not smudge_original:
                    num_diff = sum(a != b for a, b in zip(above, below))
                    if num_diff == 1:
                        # fixed_smudge = True
                        this_n += 1
                        smudge_original[i - 1 - j] = pattern[i - 1 - j][
                            :
                        ]  # below # .append((i-1-j,below))
                        pattern[i - 1 - j] = below
                        continue
                if smudge_original:
                    # roll back any smudge fixes
                    for k in smudge_original:
                        pattern[k] = smudge_original[k]
                    fixed_smudge = False
        else:
            # no break
            if this_n > 0 and (this_n == len(bottom) or this_n == len(top)):
                if not part2 or not len(top) in prev_reflection:
                    n_horizon.append(len(top))
                    if smudge_original:
                        fixed_smudge = True
                        break
            else:
                # not a valid reflection
                # roll back any smudge fixes
                if smudge_original:
                    for k in smudge_original:
                        pattern[k] = smudge_original[k]
                        fixed_smudge = False
    assert len(n_horizon) <= 1
    return n_horizon, fixed_smudge, pattern


def solve(data, part2=False):
    result = 0
    for pattern in parse(data):
        # find horizontal reflection
        n_horizon, _, _ = compute_n_horizon(pattern, part2=False)
        n_horizon_orig = n_horizon[:]
        # transpose pattern
        pattern_t = list("".join(r) for r in zip(*pattern))
        n_vertical, _, _ = compute_n_horizon(pattern_t, part2=False)
        n_vertical_orig = n_vertical[:]

        if part2:
            n_horizon_new, h_fixed, new_pattern = compute_n_horizon(
                pattern[:], part2=True, prev_reflection=n_horizon_orig
            )
            if h_fixed:
                pattern = new_pattern
                n_horizon = list(set(n_horizon_new) - set(n_horizon_orig))
            else:
                n_horizon = []

            pattern_t = list("".join(r) for r in zip(*pattern))
            n_vertical_new, v_fixed, new_pattern_t = compute_n_horizon(
                pattern_t[:],
                part2=(part2 and not h_fixed),
                prev_reflection=n_vertical_orig,
            )
            if v_fixed:
                pattern_t = new_pattern_t
                n_vertical = list(set(n_vertical_new) - set(n_vertical_orig))

                if not h_fixed:
                    # compute the horizontal reflection
                    # based on the fix in the transposed pattern
                    pattern = list("".join(r) for r in zip(*pattern_t))
                    n_horizon, _, _ = compute_n_horizon(pattern, part2=False)
                    if n_horizon == n_horizon_orig:
                        n_horizon = []
                    else:
                        pattern = new_pattern
                        n_horizon = list(set(n_horizon_new) - set(n_horizon_orig))
            else:
                n_vertical = []

        result += 100 * min(n_horizon) if n_horizon else 0
        result += min(n_vertical) if n_vertical else 0
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 405


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 27505


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 400


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result > 13712
    assert result > 19587
    assert result < 24954
    assert result != 20671
    assert result != 20679
    assert result != 22901
    assert result == 22906


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
