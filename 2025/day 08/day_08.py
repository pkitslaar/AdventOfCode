"""
Advent of Code 2025 - Day 08
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

from collections import namedtuple

Point = namedtuple("Point", ["x", "y", "z"])


def d2(p1, p2):
    return (
        (p1.x - p2.x) * (p1.x - p2.x)
        + (p1.y - p2.y) * (p1.y - p2.y)
        + (p1.z - p2.z) * (p1.z - p2.z)
    )


from itertools import combinations


def solve(data, N=10, part2=False):
    result = 0
    junctions = []
    for line in data.splitlines():
        p = Point(*[int(v) for v in line.split(",")])
        junctions.append(p)

    distances = {}
    for p1, p2 in combinations(junctions, 2):
        distances[(p1, p2)] = d2(p1, p2)

    sorted_distances = [*sorted(distances.items(), key=lambda x: x[1])]
    if not part2:
        sorted_distances = sorted_distances[:N]

    circuits = [set([p]) for p in junctions]
    for (p1, p2), dist in sorted_distances:
        merge_circuits = []
        new_circuits = []
        for circuit in circuits:
            if p1 in circuit or p2 in circuit:
                merge_circuits.append(circuit)
            else:
                new_circuits.append(circuit)
        merged_circuit = set()
        for circuit in merge_circuits:
            merged_circuit.update(circuit)
        new_circuits.append(merged_circuit)
        circuits = new_circuits
        if len(circuits) == 1 and part2:
            return p1.x * p2.x

    circuit_sizes = [len(circuit) for circuit in circuits]
    circuit_sizes.sort(reverse=True)
    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 40


def test_part1():
    result = solve(data(), N=1000)
    print("Part 1:", result)
    assert result == 54180


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 25272


def test_part2():
    result = solve(data(), N=1000, part2=True)
    print("Part 2:", result)
    assert result == 25325968


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
