"""
Advent of Code 2025 - Day 03
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""


def solve(data, part2=False):
    result = 0
    for bank in data.strip().splitlines():
        batteries = [int(d) for d in bank]
        battery_indices = [*enumerate(batteries)]
        battery_indices.sort(key=lambda x: x[1], reverse=True) # sort by battery joltage descending

        N = 2 if not part2 else 12  # number of batteries to select
        
        #
        found = [(-1,0)] # dummy initial value to simplify logic
        while len(found) -1 < N:
            num_to_be_found = N - len(found)
            max_index_allowed = len(batteries) - num_to_be_found - 1
            for idx, battery in battery_indices:
                last_index, last_battery = found[-1]
                if idx > last_index and idx <= max_index_allowed:
                    found.append((idx, battery))
                    break

        bank_joltage = int("".join(str(battery) for idx, battery in found))    
        result += bank_joltage
        
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 357


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 17613


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 3121910778619


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 175304218462560


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()