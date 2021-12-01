"""
Advent of Code 2021 - Day 01
Pieter Kitslaar
"""

from pathlib import Path

example_data = """\
199
200
208
210
200
207
240
269
260
263"""

def parse_data(txt):
    for line in txt.splitlines():
        if line.strip():
            yield int(line.strip())

def test_example():
    numbers = list(parse_data(example_data))
    assert get_num_increase(numbers) == 7

def get_num_increase(numbers):
    prev_n = numbers[0]
    num_increase = 0
    for n in numbers[1:]:
        if n > prev_n:
            num_increase +=1
        prev_n = n
    return num_increase

def get_input():
    input_numbers = []
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        for l in f:
            input_numbers.append(int(l.strip()))
    return input_numbers

def test_part1():
    answer = get_num_increase(get_input())
    print('part 1:', answer)
    assert 1233 == answer


def get_num_sliding_increases(numbers):
    num_increases = 0
    prev_sum = sum(numbers[:3])
    for start_i in range(1, len(numbers)-2):
        new_sum = sum(numbers[start_i:start_i+3])
        if new_sum > prev_sum:
            num_increases += 1
        prev_sum = new_sum
    return num_increases


def test_example_2():
    answer = get_num_sliding_increases(list(parse_data(example_data)))
    assert answer == 5

def test_part2():
    answer = get_num_sliding_increases(get_input())
    print('part 2:', answer)
    assert 1275 == answer


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example_2()
    test_part2()