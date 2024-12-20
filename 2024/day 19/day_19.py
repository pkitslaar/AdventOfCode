"""
Advent of Code 2024 - Day 19
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

def parse(data):
    towels = []
    designs = []
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        if not towels:
            towels = [t.strip() for t in line.split(',')]
        else:
            designs.append(line.strip())
    return towels, designs

def solve_design(towels, design, solutions=None, level=0, early_exit=True):
    if solutions is None:
        solutions = []
    #these_towels = [t for t in towels if t in design]
    if not any(design.endswith(t) for t in towels):
        # no way to solve this design
        return solutions
    for towel in towels:
        if design.endswith(towel):
            #print(level, towel, design)
            if len(design) == len(towel):
                solutions.append([towel])
            else:
                sub_solutions = []
                if solve_design(towels, design[:-len(towel)], sub_solutions, level=level+1, early_exit=early_exit):
                    for s in sub_solutions:
                        solutions.append(s + [towel])
                        if early_exit:
                            break
        if early_exit and solutions:
            break # stop when first solution found
    return solutions

from functools import reduce

def solve(data, part2=False):
    result = 0
    towels, designs = parse(data)
    towels.sort(key=lambda x: len(x), reverse=True)

    towel_equivalents = {}
    if part2:
        for i, t in enumerate(towels):
            t_solution = solve_design(towels, t, early_exit=False)
            if t_solution:
                towel_equivalents[t] = t_solution

    num_designs = len(designs)
    for i, design in enumerate(designs):
        solutions = solve_design(towels, design, early_exit=True)
        print(i, design, len(solutions), 100*i/num_designs)
        if solutions:
            if part2:
                num_permutations = reduce(lambda x, y: x * y, (len(towel_equivalents[t]) for t in solutions[0]))
                result += num_permutations
            else:
                result += 1
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 6


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 324


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 16


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == -1


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
    
if __name__ == "__main__":
    #test_example()
    test_part1()
    #test_example2()
    #test_part2()
    #print("all tests pass")