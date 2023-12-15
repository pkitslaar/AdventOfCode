"""
Advent of Code 2023 - Day 15
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def HASH(text):
    value = 0
    for c in text:
        value += ord(c)
        value *= 17
        value %= 256
    return value


def test_HASH():
    assert HASH("HASH") == 52


import re

INSTRUCTION_RE = re.compile(r"([a-z]+)([=-])(\d*)")

from collections import namedtuple, defaultdict

Lens = namedtuple("Lens", "label focal_length")


def solve(data, part2=False):
    if not part2:
        return sum(HASH(part) for part in data.split(","))

    HASHMAP = defaultdict(list)
    for part in data.split(","):
        label, operation, value = INSTRUCTION_RE.match(part).groups()
        h_index = HASH(label)
        box = HASHMAP[h_index]
        if operation == "-":
            for i, lens in enumerate(box):
                if lens.label == label:
                    box.pop(i)
                    break
        elif operation == "=":
            for i, lens in enumerate(box):
                if lens.label == label:
                    box[i] = Lens(label, int(value))
                    break
            else:
                # no break
                box.append(Lens(label, int(value)))
    result = 0
    for h_index, box in HASHMAP.items():
        for lens_j, lens in enumerate(box):
            result += (h_index + 1) * (lens_j + 1) * lens.focal_length
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 1320


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 509784


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 145


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 230197


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read().strip()
