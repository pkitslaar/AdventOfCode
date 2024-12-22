"""
Advent of Code 2024 - Day 22
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
1
10
100
2024
"""

def mix(secret, value):
    return secret ^ value

def prune(secret):
    return secret % 16777216

def next_secret(secret):
    secret = prune(mix(secret, secret*64))
    secret = prune(mix(secret, secret // 32))
    return prune(mix(secret, secret*2048))

def test_next_secret():
    values = """\
    15887950
    16495136
    527345
    704524
    1553684
    12683156
    11100544
    12249484
    7753432
    5908254
    """
    secret = 123
    for v in map(int, values.strip().split()):
        secret = next_secret(secret)
        assert secret == v

from collections import Counter


def solve(data, part2=False):
    result = 0
    all_secrets = []
    for monkey, secret in enumerate(map(int, data.strip().splitlines())):
        monkey_secrets = [secret]
        for i in range(2000):
            secret = next_secret(secret)
            monkey_secrets.append(secret)
        all_secrets.append(monkey_secrets)
        if not part2:
            result += monkey_secrets[-1]

    if part2:
        change_value = Counter()
        for monkey_secrets in all_secrets:
            monkey_change_values = {}
            prices = [int(str(s)[-1]) for s in monkey_secrets]
            prev_price = prices[0]
            changes = []
            for p in prices[1:]:
                changes.append(p - prev_price)
                prev_price = p
                if len(changes) == 4:
                    cv_key = tuple(changes)
                    if not cv_key in monkey_change_values:
                        monkey_change_values[cv_key] = p
                    changes.pop(0)
            for cv_key, p in monkey_change_values.items():
                change_value[cv_key] += p
        result = change_value.most_common()[0][1]
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 37327623


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 17960270302

EXAMPLE_DATA2 = """\
1
2
3
2024
"""

def test_example2():
    result = solve(EXAMPLE_DATA2, part2=True)
    print(f"example 2: {result}")
    assert result == 23


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 2042


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()