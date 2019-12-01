"""
Day 1 puzzle - Advent of Code 2019
Pieter Kitslaar
"""
from pathlib import Path

def check(value, expected):
    if value != expected:
        raise ValueError(f"Value {value} != expected {expected}")

def fuel_from_mass(mass):
    return int(mass/3) - 2

# Check examples
check(fuel_from_mass(12), 2)
check(fuel_from_mass(14), 2)
check(fuel_from_mass(1969), 654)
check(fuel_from_mass(100756), 33583)

# part 1
with open(Path(__file__).parent / 'input.txt', 'r') as f:
    modules_masses = [int(l) for l in f]

print('Part 1', sum([fuel_from_mass(m) for m in modules_masses]))

# part 2
def recursive_fuel(mass):
    total_fuel = 0
    current_mass = mass
    while current_mass > 0:
        fuel = fuel_from_mass(current_mass)
        current_mass = 0
        if fuel > 0:
            total_fuel += fuel
            current_mass = fuel
    return total_fuel

# Check examples
check(recursive_fuel(12), 2)
check(recursive_fuel(1969), 966)
check(recursive_fuel(100756), 50346)

print('Part 2', sum([recursive_fuel(m) for m in modules_masses]))