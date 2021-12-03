"""
Advent of Code 2021 - Day 03
Pieter Kitslaar
"""

from pathlib import Path

from collections import Counter

example = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

def parse(txt):
    for line in txt.splitlines():
        yield tuple(line.strip())

def collect(stream_of_bits, num_bits_per_value=5):
    bit_counters=[Counter() for _ in range(num_bits_per_value)]
    for bits in stream_of_bits:
        #print(bits)
        for i, b in enumerate(bits):
            #print(i, b)
            bit_counters[i].update(b)
    return bit_counters

def gamma_rate(collected_bits):
    bits = [c.most_common()[0][0] for c in collected_bits]
    return int(''.join(bits),2)

def epsilon_rate(collected_bits):
    bits = [c.most_common()[-1][0] for c in collected_bits]
    return int(''.join(bits),2)

def test_example():
    collected_bits = collect(parse(example))
    gr = gamma_rate(collected_bits)
    assert 22 == gr
    er = epsilon_rate(collected_bits)
    assert 9 == er
    power_consumption = gr*er
    assert 198 == gr*er

def get_input():
    input_numbers = []
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    collected_bits = collect(parse(get_input()), 12)
    gr = gamma_rate(collected_bits)
    assert 394 == gr
    er = epsilon_rate(collected_bits)
    assert 3701 == er
    power_consumption = gr*er
    assert 1458194 == gr*er
    print('Part 1', power_consumption)

def collect2(stream_of_bits, most_common_index, equal_value):
    all_values= list(stream_of_bits)
    remaining_values = all_values
    start_bits = []
    while len(remaining_values) > 1:
        bit_counter = Counter()
        check_bit = len(start_bits)
        for v in remaining_values:
            bit_counter.update(v[check_bit])
        most_common = bit_counter.most_common()
        most_common_value, most_common_count = most_common[most_common_index]
        if len(most_common) > 1 and all(most_common_count == c[1] for c in most_common):
            most_common_value = equal_value
        start_bits.append(most_common_value)
        remaining_values = [v for v in remaining_values if v[check_bit] == most_common_value]
    return int(''.join(remaining_values[0]),2)

def test_example2():
    oxygen = collect2(parse(example), 0, '1') # oxygen
    assert 23 == oxygen
    co2 = collect2(parse(example),-1, '0') # co2
    assert 10 == co2
    assert 230 == oxygen*co2

def test_part2():
    oxygen = collect2(parse(get_input()), 0, '1') # oxygen
    co2 = collect2(parse(get_input()),-1, '0') # co2
    print('Part 2:', oxygen*co2)
    assert(2829354 == oxygen*co2)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()