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

from functools import lru_cache

# the magic solution that makes the problem tractable
@lru_cache(maxsize=None)
def solve_design(towels, design, early_exit=True):
    num_solutions = 0
    for towel in towels:
        if design.endswith(towel):
            if len(design) == len(towel):
                num_solutions += 1
            else:
                num_solutions += solve_design(towels, design[:-len(towel)], early_exit=early_exit)
        if early_exit and num_solutions:
            break # stop when first solution found
    return num_solutions



def solve(data, part2=False):
    result = 0
    towels, designs = parse(data)
    towels.sort(key=lambda x: len(x), reverse=True)
    towels = tuple(towels)

    for i, design in enumerate(designs):
        solve_design.cache_clear() # clear cache for each design
        num_solutions = solve_design(towels, design, early_exit=not part2)
        result += num_solutions
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
    assert result == 575227823167869


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