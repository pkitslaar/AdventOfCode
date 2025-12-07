"""
Advent of Code 2025 - Day 02
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""


def invalid_ids(start, end, min_pair_digits=2, max_pair_digits=2):
    invalid_ids = []

    # max digits
    num_digits = [len(str(n)) for n in (start, end)]
    for N in range(min_pair_digits, max_pair_digits + 1):
        if N > max(num_digits):
            break
        num_even_digits = [n for n in num_digits if n % N == 0]
        max_num_digits = max(num_even_digits) if num_even_digits else 0
        if max_num_digits > 0:
            max_digits_per_pair = max_num_digits // N
            if max_digits_per_pair == 0:
                continue
            start_str = f"{start:0{max_num_digits}d}"
            end_str = f"{end:0{max_num_digits}d}"
            lowest_pair = (
                min(
                    int(str(start_str)[:max_digits_per_pair]),
                    int(str(start_str)[max_digits_per_pair:]),
                )
                if len(start_str) > max_digits_per_pair
                else int(str(start_str))
            )
            highest_pair = (
                max(
                    int(str(end_str)[max_digits_per_pair:]),
                    int(str(end_str)[:max_digits_per_pair]),
                )
                if len(end_str) > max_digits_per_pair
                else int(str(end_str))
            )
            if lowest_pair > highest_pair:
                raise ValueError("Logic error in determining lowest and highest pair")
            for pair in range(lowest_pair, highest_pair + 1):
                str_pair = f"{pair}" * N
                pair_value = int(str_pair)
                if pair_value < start or pair_value > end:
                    continue
                invalid_ids.append(pair_value)
    return invalid_ids


def test_invalid_ids():
    assert invalid_ids(11, 22) == [11, 22]
    assert invalid_ids(95, 115) == [99]
    assert invalid_ids(998, 1012) == [1010]
    assert invalid_ids(1188511880, 1188511890) == [1188511885]
    assert invalid_ids(222220, 222224) == [222222]
    assert invalid_ids(1698522, 1698528) == []
    assert invalid_ids(446443, 446449) == [446446]
    assert invalid_ids(38593856, 38593862) == [38593859]
    assert invalid_ids(565653, 565659) == []
    assert invalid_ids(824824821, 824824827) == []
    assert invalid_ids(2121212118, 2121212124) == []


def solve(data, part2=False):
    result = 0
    ranges = data.strip().split(",")
    for r in ranges:
        start, end = map(int, r.split("-"))
        if not part2:
            invalids = invalid_ids(start, end)
        else:
            invalids = invalid_ids_2(start, end)
        result += sum(invalids)
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 1227775554


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result > 10901503867
    assert result > 64215793219
    assert result == 64215794229


def invalid_ids_2(start, end):
    invalid_ids = []

    # check number of digits in start and end
    start_str = str(start)
    end_str = str(end)
    n_start = len(start_str)
    n_end = len(end_str)

    # create digit groups with same number of digits
    # ranges that span multiple digit lengths are split
    # so the logic can be applied more easily
    # for example: 95-115 becomes 95-99 and 100-115
    digit_groups = []
    for n in range(n_start, n_end + 1):
        if n == n_start and n == n_end:
            digit_groups.append((start_str, end_str))
        elif n == n_start:
            digit_groups.append((start_str, "9" * n))
        elif n == n_end:
            digit_groups.append(("1" + "0" * (n - 1), end_str))
        else:
            digit_groups.append(("1" + "0" * (n - 1), "9" * n))

    # for each digit group, find invalid ids
    for start_str, end_str in digit_groups:

        max_num_digits = len(start_str)
        sorted_groups = [int(start_str), int(end_str)]
        for n_digits in range(1, max_num_digits + 1):
            start_group = start_str[:n_digits]
            start_group_value = int(start_group)
            end_group = end_str[:n_digits]
            end_group_value = int(end_group)

            sorted_groups = [*sorted([start_group_value, end_group_value])]

            n_start_groups, start_remainder = divmod(len(start_str), n_digits)
            if n_start_groups > 1 and start_remainder == 0:
                for v in range(sorted_groups[0], sorted_groups[1] + 1):
                    first_group_value = int(str(v) * (n_start_groups))
                    if first_group_value >= start and first_group_value <= end:
                        invalid_ids.append(first_group_value)

            n_end_groups, end_remainder = divmod(len(end_str), n_digits)
            if n_end_groups > 1 and end_remainder == 0:
                for v in range(sorted_groups[0], sorted_groups[1] + 1):
                    last_group_value = int(str(v) * (n_end_groups))
                    if last_group_value >= start and last_group_value <= end:
                        invalid_ids.append(last_group_value)

    return [*sorted(set(invalid_ids))]


def test_invalid_ids_2():
    assert invalid_ids_2(11, 22) == [11, 22]
    assert invalid_ids_2(95, 115) == [99, 111]
    assert invalid_ids_2(998, 1012) == [999, 1010]
    assert invalid_ids_2(1188511880, 1188511890) == [1188511885]
    assert invalid_ids_2(222220, 222224) == [222222]
    assert invalid_ids_2(1698522, 1698528) == []
    assert invalid_ids_2(446443, 446449) == [446446]
    assert invalid_ids_2(38593856, 38593862) == [38593859]
    assert invalid_ids_2(565653, 565659) == [565656]
    assert invalid_ids_2(824824821, 824824827) == [824824824]
    assert invalid_ids_2(2121212118, 2121212124) == [2121212121]


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 4174379265


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result > 54116535122
    assert result > 85418738568
    assert result > 85418739566
    assert result == 85513235135


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
