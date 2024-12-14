"""
Advent of Code 2024 - Day 13
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

def parse(data):
    machines = [{}]
    for line in data.strip().splitlines():
        if not line.strip():
            machines.append({})
            continue
        key, value = line.split(": ")
        x_str, y_str = value.split(", ")
        x = int(x_str[2:]) if key == "Prize" else int(x_str[1:])
        y = int(y_str[2:]) if key == "Prize" else int(y_str[1:])
        machines[-1][key] = x,y
    return machines

from collections import namedtuple
from heapq import heappop, heappush

State = namedtuple("State", "cost n_a n_b x y")

def find_solution(machine, cost_a = 3, cost_b = 1, N=100):
    prize = machine["Prize"]
    a_delta = machine["Button A"]
    b_delta = machine["Button B"]

    queue = [State(0, 0, 0, 0, 0)]
    visited = set()
    while queue:
        current = heappop(queue)
        cost, n_a, n_b, x, y = current
        if current in visited:
            continue
        visited.add(current)
        if (x,y) == prize:
            return cost
        if n_a < N:
            # add new states for pushing buttons A
            heappush(queue, State(cost+cost_a, n_a+1, n_b, x+a_delta[0], y+a_delta[1]))
        if n_b < N:
            heappush(queue, State(cost+cost_b, n_a, n_b+1, x+b_delta[0], y+b_delta[1]))
    return -1 # no solution


def find_optimized(machine, cost_a = 3, cost_b = 1, maxN=100):
    prize = machine["Prize"]
    a_delta = machine["Button A"]
    b_delta = machine["Button B"]

    # Thanks to Github Co-Pilot for writing out the math for me

    # we need to solve the following equations:
    # a * a_delta[0] + b * b_delta[0] = prize[0]
    # a * a_delta[1] + b * b_delta[1] = prize[1]
    
    # we can solve this by multiplying the first equation by b_delta[1] and the second by b_delta[0]
    # a * a_delta[0] * b_delta[1] + b * b_delta[0] * b_delta[1] = prize[0] * b_delta[1]
    # a * a_delta[1] * b_delta[0] + b * b_delta[0] * b_delta[1] = prize[1] * b_delta[0]

    # subtract the two equations to get a:
    a = (prize[0] * b_delta[1] - prize[1] * b_delta[0]) / (a_delta[0] * b_delta[1] - a_delta[1] * b_delta[0])
    b = (prize[1] - a * a_delta[1]) / b_delta[1]

    if a - int(a) != 0 or b - int(b) != 0:
        # we want exact solutions for integer number of pushes
        return -1
    if a < 0 or b < 0:
        # we want positive number of pushes
        return -1
    if maxN > 0 and (a > maxN or b > maxN):
        # if a limit is defined (e.g. Part 1) we want to stay within that limit
        return -1
    
    # return the cost of the solution
    return int(a) * cost_a + int(b) * cost_b

def solve(data, part2=False):
    machines = parse(data)
    result = 0
    N = 100 if not part2 else -1
    for m in machines:
        if part2:
            # increase the prize for part 2
            INC = 10000000000000
            m['Prize'] = (m["Prize"][0] + INC, m["Prize"][1] + INC)
        min_cost = find_optimized(m, maxN=N)         
        if min_cost > -1:
            result += min_cost
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 480


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 29438


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 104958599303720


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()