"""
Advent of Code 2021 - Day 07
Pieter Kitslaar
"""

from pathlib import Path

from collections import Counter
example = """16,1,2,0,4,2,7,1,2,14"""

def parse(txt):
    return list(map(int,txt.split(',')))

def solve1(initial):
    s_initial = list(sorted(initial))
    median = s_initial[len(s_initial)//2]
    fuel = sum([abs(v-median) for v in s_initial])
    return fuel, median

def test_example():
    initial = parse(example)
    fuel, position = solve1(initial)
    assert fuel == 37
    assert position == 2

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    initial = parse(get_input())
    fuel, position = solve1(initial)
    print('Part 1:', fuel, f'(at position {position})')
    assert 364898 == fuel
    assert 361 == position

def cost(pos):
    return sum([v for v in range(0, abs(pos)+1)])

def test_cost():
    assert 66 == cost(16-5)
    assert 10 == cost(1-5)

def total_cost(initial, pos):
    return sum([cost(p-pos)*count for p,count in Counter(initial).items()])

def test_total_cost():
    initial = parse(example)
    assert 168 == total_cost(initial, 5)
    assert 206 == total_cost(initial, 2)

def solve2(initial):
    # find an initial start position
    # lets use the solution to part 1
    _, prev_pos = solve1(initial)
    prev_cost = total_cost(initial, prev_pos)

    # cache for quick cost lookup
    costs_at_pos = {prev_pos: prev_cost}
    num_iterations = 0
    while True:
        for direction in (-1, 1):
            num_iterations += 1
            test_pos = prev_pos+direction
            try:
                # did we already compute this position
                test_cost = costs_at_pos[test_pos]
            except KeyError:
                test_cost = total_cost(initial, test_pos)
                costs_at_pos[test_pos] = test_cost

            if test_cost < prev_cost:
                prev_pos = test_pos
                prev_cost = test_cost
                break
        else:
            # no break
            print(f'found minimum after {num_iterations} iterations and {len(costs_at_pos)} computations')
            return prev_cost, prev_pos
    
def test_example2():
    fuel, position = solve2(parse(example))
    assert(fuel == 168)
    assert(position == 5)

def test_part2():
    fuel, position = solve2(parse(get_input()))
    print('Part 2:', fuel, f'(at position {position})')
    assert 104149091 == fuel
    assert 500 == position

if __name__ == "__main__":
    test_example()
    test_part1()
    test_cost()
    test_example2()
    test_part2()