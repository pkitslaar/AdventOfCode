"""
Advent of Code 2022 - Day 06
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()


def find_marker(d, N=4, offset=0):
    L = len(d)
    for i in range(N+offset,L):
        unique_chars = set(d[i-N:i])
        if len(unique_chars) == N:
            break
    else:
        # no break
        raise ValueError('No marker found')
    return i

def test_examples():
    assert(7 == find_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb'))
    assert(5 == find_marker('bvwbjplbgvbhsrlpgdmjqwftvncz'))
    assert(6 == find_marker('nppdvjthqldpwncqszvftbrmjlhg'))
    assert(10 == find_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'))
    assert(11 == find_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'))

def test_part1():
    result = find_marker(data())
    print('PART 1:', result)

def find_message(d):
    #packet_marker = find_marker(d)
    message_marker = find_marker(d,14)
    return message_marker

def test_examples2():
    assert(19 == find_message('mjqjpqmgbljsphdztnvjfqwrcgsmlb'))
    assert(23 == find_message('bvwbjplbgvbhsrlpgdmjqwftvncz'))
    assert(23 == find_message('nppdvjthqldpwncqszvftbrmjlhg'))
    assert(29 == find_message('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'))
    assert(26 == find_message('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'))

def test_part2():
    result = find_message(data())
    print('PART 2:', result)
    

if __name__ == "__main__":
    test_examples()
    test_part1()
    test_examples2()
    test_part2()