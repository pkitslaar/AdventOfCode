"""
Advent of Code 2024 - Day 05
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

def parse(data):
    lines = data.splitlines()
    rules = []
    updates = []
    for line in lines:
        if '|' in line:
            a, b = line.split("|")
            rules.append((int(a), int(b)))
        elif ',' in line:
            updates.append([int(x) for x in line.split(",")])
    return rules, updates


def solve(data, part2=False):
    rules, updates = parse(data)
    result = 0
    for u in updates:
        u_set = set(u)
        u_rules = [r for r in rules if all(x in u_set for x in r)]
        u_rule_order = [(u.index(r[0]), u.index(r[1])) for r in u_rules]
        if all(a < b for a, b in u_rule_order):
            # correct order
            if not part2:
                result += u[len(u)//2]
        else:
            # incorrect order, for part2 we need to find the correct order
            if part2:
                order_correct = False

                # keep swapping until all rules are satisfied
                while not order_correct:
                    order_correct = True # assume correct until invalid order found
                    for low, high in u_rules:
                        low_index, high_index = u.index(low), u.index(high)
                        if low_index > high_index:
                            # incorrect order, move lowest before the highest
                            u[high_index], u[low_index] = u[low_index], u[high_index]
                            order_correct = False
                            break

                result += u[len(u)//2]
    
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 143


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 5329


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 123


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 5833


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()