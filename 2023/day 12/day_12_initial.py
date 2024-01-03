"""
Advent of Code 2023 - Day 12
Pieter Kitslaar

These are the initial solutions I tried for day 12.
The final solution based on memoization is in day_12.py
"""

EXAMPLE_DATA = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

import itertools


def solve(data, part2=False):
    return solve_smart(data, part2=part2)


from heapq import heappush, heappop, heapify


def find_solutions(initial_springs, initial_n_broken):
    visited = set()
    to_visit = [(initial_springs, initial_n_broken, "")]
    heapify(to_visit)
    solutions = []
    while to_visit:
        springs, n_broken, current_solution = heappop(to_visit)
        if len(n_broken) == 0:
            # check that ther are no more known broken springs
            # rest of the solution should be working
            if springs.count("#") == 0:
                # found a solution
                solutions.append(current_solution + "." * len(springs))
            continue

        current_known = springs.count("#")
        if current_known > sum(n_broken):
            continue
        current_unknown = springs.count("?")
        if current_known + current_unknown < sum(n_broken):
            # not possible to fulfill this solution
            continue

        first_group = None
        for k, g in itertools.groupby(enumerate(springs), lambda t: t[1] != "."):
            if k:
                # group with # or ? that should satisfy first_to_find
                first_group = list(g)
                break

        if first_group:
            first_to_find = n_broken[0]
            group_str = "".join(c for i, c in first_group)
            group_start = first_group[0][0]
            if len(group_str) < first_to_find:
                # not enough to satisfy first_to_find
                continue
            for i in range(len(group_str) - first_to_find + 1):
                test_pattern = "." * i + "#" * first_to_find + "."
                for t, c in zip(test_pattern, group_str):
                    if c == "#" and t == ".":
                        # not possible to fulfill this solution
                        break
                else:
                    # no break, so this pattern is possible
                    full_pattern = "." * group_start + test_pattern
                    new_solution = current_solution + full_pattern
                    new_n_broken = n_broken[1:]
                    new_springs = springs[len(full_pattern) :]
                    heappush(to_visit, (new_springs, new_n_broken, new_solution))
    return len(solutions)


def find_solutions2(initial_springs, initial_n_broken):
    # visited = set()
    to_visit = [(initial_springs, initial_n_broken, "")]
    heapify(to_visit)
    solutions = set()
    # n_solutions = 0
    while to_visit:
        springs, n_broken, current_solution = heappop(to_visit)
        if len(n_broken) == 0 and springs.count("#") == 0:
            full_solution = (current_solution + "." * len(springs))[
                : len(initial_springs)
            ]
            solution_n_broken = tuple(
                [
                    len([*g[1]])
                    for g in itertools.groupby(full_solution, lambda c: c == "#")
                    if g[0]
                ]
            )
            # check that ther are no more known broken springs
            # rest of the solution should be working
            if solution_n_broken == initial_n_broken:
                # found a solution
                solutions.add(full_solution)
                # n_solutions += 1
            continue

        current_known = springs.count("#")
        if current_known > sum(n_broken):
            continue
        current_unknown = springs.count("?")
        if current_known + current_unknown < sum(n_broken):
            # not possible to fulfill this solution
            continue

        match springs[0]:
            case ".":
                new_solution = current_solution + "."
                new_n_broken = n_broken
                new_springs = springs[1:]
                heappush(to_visit, (new_springs, new_n_broken, new_solution))
            case "#":
                new_solution = current_solution + "#"
                if n_broken[0] > 1:
                    new_n_broken = tuple([n_broken[0] - 1] + list(n_broken[1:]))
                    new_springs = springs[1:]
                    heappush(to_visit, (new_springs, new_n_broken, new_solution))
                else:
                    new_n_broken = n_broken[1:]
                    new_springs = springs[1:]
                    if not new_springs or new_springs[0] != "#":
                        # end of a broken group to inject the separator "."
                        # new_solution = new_solution + "."
                        # new_springs = new_springs[1:]
                        heappush(to_visit, (new_springs, new_n_broken, new_solution))
            case "?":
                # add "." case
                new_solution = current_solution + "."
                new_n_broken = n_broken
                new_springs = springs[1:]
                heappush(to_visit, (new_springs, new_n_broken, new_solution))

                # add "#" case
                new_solution = current_solution + "#"
                if n_broken[0] > 1:
                    new_n_broken = tuple([n_broken[0] - 1] + list(n_broken[1:]))
                    new_springs = springs[1:]
                    heappush(to_visit, (new_springs, new_n_broken, new_solution))
                else:
                    new_n_broken = n_broken[1:]
                    new_springs = springs[1:]
                    if not new_springs or new_springs[0] != "#":
                        # end of a broken group to inject the separator "."
                        # new_solution = new_solution + "."
                        # new_springs = new_springs[1:]
                        heappush(to_visit, (new_springs, new_n_broken, new_solution))

    return solutions


from collections import Counter


def count_solutions(sub_solutions):
    result = sub_solutions[0]
    for next_c in sub_solutions[1:]:
        new_result = Counter()
        new_result[".."] = next_c[".."] * result.total()
        new_result[".#"] = next_c[".#"] * result.total()
        new_result["#."] = next_c["#."] * (result[".."] + result["#."])
        new_result["##"] = next_c["##"] * (result[".."] + result["#."])
        result = new_result
    return result


def solve_smart(data, part2=False):
    result = 0
    for row in data.splitlines():
        springs, n_broken = row.split()
        n_broken = tuple(map(int, n_broken.split(",")))
        s1 = find_solutions2(springs, n_broken)
        s1_n = Counter(f"{s[0]}{s[-1]}" for s in s1)
        n1 = s1_n.total()
        if part2:
            n_solutions = 0
            orig_s_e = find_solutions2(springs + "?", n_broken)
            s_e_n = Counter(f"{s[0]}{s[-1]}" for s in orig_s_e)
            s_e_total = count_solutions(
                [s_e_n.copy() for _ in range(4)] + [s1_n.copy()]
            )
            ne = s_e_total.total()

            orig_s_b = find_solutions2("?" + springs, n_broken)
            s_b_n = Counter(f"{s[0]}{s[-1]}" for s in orig_s_b)
            s_b_total = count_solutions(
                [s1_n.copy()] + [s_b_n.copy() for _ in range(4)]
            )
            nb = s_b_total.total()

            if ne > nb:
                n_solutions = ne
            else:
                n_solutions = nb
        else:
            n_solutions = n1
        result += n_solutions
    return result


def solve_naive(data, part2=False):
    result = 0
    n_checks = 0
    for row in data.splitlines():
        springs, n_broken = row.split()
        n_broken = [*map(int, n_broken.split(","))]
        total_broken = sum(n_broken)
        n_known_broken = sum(1 for c in springs if c == "#")
        n_unknown = sum(1 for c in springs if c == "?")
        n_working = sum(1 for c in springs if c == ".")
        assert n_known_broken + n_unknown + n_working == len(springs)

        n_broken_to_find = total_broken - n_known_broken
        if n_broken_to_find < 1:
            result += 1
            continue
        unknown_positions = [i for i, c in enumerate(springs) if c == "?"]
        # make bit pattern with each bit representing unknown spring
        # 0 = working, 1 = broken
        # e.g. 0b001011 = 3 working, 2 broken, 1 unknown
        max_bit_value = 2**n_unknown
        min_bit_value = int("1" * n_broken_to_find, 2)

        found_solutions = []
        for bit_mask_value in range(min_bit_value, max_bit_value):
            bit_mask = f"{bit_mask_value:0{n_unknown}b}"
            # check in bit mask if we have enough broken
            n_broken_in_pattern = sum(1 for c in bit_mask if c == "1")
            if n_broken_in_pattern != n_broken_to_find:
                continue
            # bit_mask_value = (2**n_unknown) >> (n_unknown - n_broken_to_find)
            # bit_mask = f"{bit_mask_value:0{n_unknown}b}"
            # visited = set()
            # for bit_mask in itertools.product(bit_mask, repeat=n_unknown):
            #    if bit_mask in visited:
            #        continue
            #    visited.add(bit_mask)

            n_checks += 1

            # fill in the bit mask
            this_solution = list(springs)
            for i, bit in zip(unknown_positions, bit_mask):
                this_solution[i] = "." if bit == "0" else "#"
            this_solution = "".join(this_solution)
            this_broken = [
                *filter(
                    lambda c: c > 0, (p.count("#") for p in this_solution.split("."))
                )
            ]
            if this_broken == n_broken:
                found_solutions.append(this_solution)
        result += len(found_solutions)
    print(f"{n_checks=}")
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 21


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 6949


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 525152


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    # check all previous submitted solutions
    assert result > 234188386562
    assert result > 1312901105636
    assert result > 1969035590859
    assert result == -1


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
