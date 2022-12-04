"""
Advent of Code 2017 - Day 10
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

from collections import deque

def knot_hash(lengths, N=256):
    values = deque(range(N))
    state = dict(
        skip_size = 0,
        front_pos = 0
    )
    hash_internal(values, lengths, state)
    values.rotate(state['front_pos'])
    result = values.popleft() * values.popleft()
    return result

def hash_internal(values, lengths, state):
    N = len(values)
    skip_size = state['skip_size']
    front_pos = state['front_pos']
    for l in lengths:
        values_to_reverse = [values.popleft() for _ in range(l)]
        for v in values_to_reverse:
            values.appendleft(v)
        values.rotate(-(skip_size+l))
        front_pos = (front_pos + skip_size + l) % N
        skip_size += 1
    state['skip_size'] = skip_size
    state['front_pos'] = front_pos
    

def test_example():
    assert(12 == knot_hash([3,4,1,5], 5))

def test_part1():
    result = knot_hash(list(map(int,data().split(','))))
    print('PART 1:', result)
    assert(19591 == result)

def dense_hash(d, N=256):
    lengths = [ord(c) for c in d] + [17, 31, 73, 47, 23]
    values = deque(range(N))
    state = dict(
        skip_size = 0,
        front_pos = 0
    )
    for _ in range(64):
        hash_internal(values, lengths, state)
    values.rotate(state['front_pos'])

    result = []
    for i in range(16):
        block = [values.popleft() for _ in range(16)]
        r = block[0]
        for b in block[1:]:
            r = r ^ b
        result.append(f'{r:02x}')
    return ''.join(result)

def test_example2():
    assert('3efbe78a8d82f29979031a4aa0b16a9d' == dense_hash('1,2,3'))
    assert('63960835bcdc130f0b66d7ff4f6a5a8e' == dense_hash('1,2,4'))
    assert('a2582a3a0e66e6e86e3812dcb672a272' == dense_hash(''))
    assert('33efeb34ea91902bb2f59c9920caa6cd' == dense_hash('AoC 2017'))

def test_part2():
    result = dense_hash(data())
    print('PART 2:', result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()

        

