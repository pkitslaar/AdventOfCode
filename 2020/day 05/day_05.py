"""
Advent of Code 2020 - Day 05
Pieter Kitslaar
"""

from pathlib import Path

def partition(txt, start, end):
    for step in txt:
        mid = start + int(0.5*(end - start))
        if step in ('F','L'):
            end = mid
        else:
            start = mid
        #print(step, start, end)
    return start, end

def find_row(txt):
    return partition(txt, 0, 128)[0]

def find_column(txt):
    return partition(txt, 0, 8)[0]

def find_id(txt):
    row = find_row(txt[:7])
    col = find_column(txt[-3:])
    return col+row*8

def test_example1():
    test_txt = 'FBFBBFFRLR'
    assert(44 == find_row(test_txt[:7]))
    assert(5 == find_column(test_txt[-3:]))
    assert(357 == find_id(test_txt))

    assert(567 == find_id('BFFFBBFRRR'))
    assert(119 == find_id('FFFBBBFRRR'))


def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        for line in f:
            yield line.strip()

def test_part1():
    all_ids = [find_id(l) for l in get_input()]
    answer = max(all_ids)
    print('Part 1:', answer)

def test_part2():
    all_ids = set([find_id(l) for l in get_input()])
    known_ids = {col+(row*8) for row in range(1,127) for col in range(0,8)}
  
    # find all the initial missing
    missing_ids = known_ids - all_ids

    # We know that out ID+1 and ID-1 should not be missing
    # so lets remove the IDS that have a neighbor in the list
    neighbor_ids = {i+1 for i in missing_ids}.union({i-1 for i in missing_ids})
    final_missing = missing_ids - neighbor_ids
    assert({649} == final_missing)
    print('Part 2:', list(final_missing)[0])

if __name__ == "__main__":
    test_example1()
    test_part1()
    test_part2()