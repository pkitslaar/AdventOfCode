"""
Day 1 puzzle - Advent of Code 2019
Pieter Kitslaar
"""
def check(value, expected):
    if value != expected:
        raise ValueError(f"Value {value} != expected {expected}")

def fuel_from_mass(mass):
    return int(int(mass/3.0) - 2)

# Check examples
check(fuel_from_mass(12), 2)
check(fuel_from_mass(14), 2)
check(fuel_from_mass(1969), 654)
check(fuel_from_mass(100756), 33583)
