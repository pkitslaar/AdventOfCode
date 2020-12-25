"""
Advent of Code 2020 - Day 25
Pieter Kitslaar
"""

from pathlib import Path

def loop_step(subject_number, value):
    return (value*subject_number) % 20201227

def generate_values(subject_number):
    value = 1
    loop_size = 1
    while True:
        value = loop_step(subject_number, value)
        yield loop_size, value
        loop_size += 1

def find_publickey_loopsize(public_key):
    for loop_size, value in generate_values(7):
        if value == public_key:
            return loop_size

def compute_encryption_key(public_key, N):
    for loop_size, value in generate_values(public_key):
        if loop_size == N:
            return value

def test_example():
    assert(8 == find_publickey_loopsize(5764801))
    assert(11 == find_publickey_loopsize(17807724))
    assert(14897079 == compute_encryption_key(17807724, 8))
    assert(14897079 == compute_encryption_key(5764801, 11))


def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    pub_keys = list(map(int,get_input().splitlines()))
    first_loopsize = find_publickey_loopsize(pub_keys[0])
    encryption_key = compute_encryption_key(pub_keys[1], first_loopsize)
    print('Part 1:', encryption_key)

if __name__ == "__main__":
    test_example()
    test_part1()