"""
Advent of Code 2025 - Day 10
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

def parse(data):
    
    machines = []
    for line in data.strip().splitlines():
        machine= {}
        parts = line.split()
        machine['lights'] = list(parts[0].strip('[]'))
        machine['buttons'] = [tuple(map(int, p.strip('()').split(','))) for p in parts[1:-1]]
        machine['buttons'].sort(key=lambda b: len(b), reverse=True)  # sort buttons by length ascending
        machine['joyltage'] = list(map(int, parts[-1].strip('{}').split(',')))
        
        machines.append(machine)
        
    return machines

from itertools import combinations_with_replacement, product

def solve_lights(machine):
    target_lights = machine['lights']
    num_presses = 1
    while True:
        for button_presses in combinations_with_replacement(machine['buttons'], r=num_presses):
            current_lights = ['.'] * len(target_lights)
            for button in button_presses:
                for pos in button:
                    # Toggle the light at position pos
                    current_lights[pos] = '#' if current_lights[pos] == '.' else '.'
            if current_lights == target_lights:
                return num_presses

        num_presses += 1

from heapq import heappop, heappush, heapify
from collections import Counter

import numpy as np
from scipy.optimize import nnls, milp, LinearConstraint, Bounds


def solve_joltage(machine):
    target_joltage = machine['joyltage']

    # button one hot
    button_one_hot = []
    for button in machine['buttons']:
        btn_oh = [0] * len(target_joltage)
        for digit in button:
            btn_oh[digit] = 1
        button_one_hot.append(tuple(btn_oh))
    

    # joltage[i] = n_b_0 * button_one_hot[0][i] + n_b_1 * button_one_hot[1][i] + ...
    # where n_b_x is the number of times button x is pressed
    # create system of linear equations to solve for n_b_x
    A = []
    for i in range(len(target_joltage)):
        row = []
        for btn_oh in button_one_hot:
            row.append(btn_oh[i])
        A.append(row)

    # convert to numpy arrays
    A_mat = np.array(A)
    b_vec = np.array(target_joltage)

    # solve milp problem to find integer solution
    res = milp(
        # objective: minimize total number of presses
        # This means we set the coefficients of the objective function to 1 for each variable
        c=np.ones(A_mat.shape[1]), 
        # subject to the constraints A_mat @ x = b_vec
        constraints=[LinearConstraint(A_mat, b_vec, b_vec)], 
        # Non-negativity
        bounds=Bounds(lb=0, ub=np.inf), 
        # Integrality constraints: all variables must be integers == 1
        integrality=np.ones(A_mat.shape[1], dtype=int))

    assert res.success, "No solution found for joltage problem"
    return int(np.sum(res.x))

def solve(data, part2=False):
    result = 0
    machines = parse(data)
    for machine in machines:
        if not part2:
            presses = solve_lights(machine)
            result += presses
        else:
            joltage = solve_joltage(machine)
            print(f"Machine joltage presses: {joltage}")
            result += joltage
            
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 7


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 436


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 33


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result > 11945
    assert result < 15143
    assert result < 15130
    assert result == 14999


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()

if __name__ == "__main__":
    test_example2()
    #test_part2()