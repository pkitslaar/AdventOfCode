"""
Advent of Code 2024 - Day 09
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
2333133121414131402
"""

def print_blocks(blocks):
    print()
    for b in blocks:
        for b_id, n in b.items():
            if b_id > -1:
                print(f"{b_id}"*n, end='')
        print("."*b.get(-1,0), end='')
    print()

DEBUG = False

from collections import defaultdict

def solve(data, part2=False):
    blocks = []
    for i, b in enumerate(data.strip()):
        n = int(b)
        # we encode free space with -1 the rest gets the file_id based on the index
        b_id = i // 2 if i % 2 == 0 else -1
        b_dict = defaultdict(int)
        #b_dict[-1] = 0
        b_dict[b_id] = n
        blocks.append(b_dict)

    if DEBUG:
        print_blocks(blocks)

    num_blocks = len(blocks)
    assert num_blocks % 2 == 1

    if not part2:
        current_file_index = num_blocks - 1
        current_free_index = 1
        while current_free_index < num_blocks and current_file_index > 0 and current_free_index < current_file_index:
            num_free = blocks[current_free_index].get(-1, 0)
            current_files = [*blocks[current_file_index].items()]
            assert len(current_files) == 1
            current_file_id, current_file_size= current_files[-1]
            num_to_move = min(num_free, current_file_size)
            blocks[current_file_index][current_file_id] -= num_to_move
            blocks[current_free_index][-1] -= num_to_move
            blocks[current_free_index][current_file_id] += num_to_move
            if blocks[current_file_index][current_file_id] == 0:
                current_file_index -= 2
            if blocks[current_free_index][-1] == 0:
                current_free_index += 2
    else:
        # only move whole files
        # check each file once
        left_free_index = 1
        for current_file_index in range(num_blocks - 1, -1, -2):
            current_files = [*blocks[current_file_index].items()]
            assert len(current_files) == 1
            current_file_id, current_file_size= current_files[-1]
            # find free space to the left
            for current_free_index in range(1,current_file_index,2):
                num_free = blocks[current_free_index].get(-1, 0)
                if num_free >= current_file_size:
                    blocks[current_free_index][current_file_id] += current_file_size
                    blocks[current_free_index][-1] -= current_file_size

                    blocks[current_file_index][current_file_id] -= current_file_size
                    blocks[current_file_index][-1] += current_file_size # fill with empty space
                    break # move to next file
            else:
                # no free space found for file
                pass

    if DEBUG:
        print_blocks(blocks)
        
    result = 0
    i = 0
    for b in blocks:
        for b_id, n in b.items():
            if b_id > -1:
                result += sum((i+j)*b_id for j in range(n))
                i += n
        i += b.get(-1,0) # skip empty space
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 1928


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 6399153661894


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 2858


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 6421724645083


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()