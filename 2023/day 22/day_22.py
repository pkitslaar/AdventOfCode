"""
Advent of Code 2023 - Day 22
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

from collections import namedtuple

Position = namedtuple("Position", "x y z")


class Brick(namedtuple("BrickBase", "name start end")):
    def intersects(self, other: "Brick"):
        return (
            (self.start.z <= other.end.z and self.end.z >= other.start.z)
            and (self.start.x <= other.end.x and self.end.x >= other.start.x)
            and (self.start.y <= other.end.y and self.end.y >= other.start.y)
        )

    def fall(self, new_start_z=None):
        if new_start_z is None:
            delta_z = -1
        else:
            delta_z = new_start_z - self.start.z
        return Brick(
            name=self.name,
            start=Position(self.start.x, self.start.y, self.start.z + delta_z),
            end=Position(self.end.x, self.end.y, self.end.z + delta_z),
        )


LETTERS = "ABCDEFGHIJ"

from collections import defaultdict


def solve(data, part2=False):
    bricks = []
    all_lines = [*data.splitlines()]
    for i, line in enumerate(all_lines):
        s, e = line.split("~")
        # create a nice name for the brick as identifier
        # names start as A, B, C into AA, AB, etc,..
        name = "".join([LETTERS[int(d)] for d in str(i)])
        bricks.append(
            Brick(
                name=name,
                start=Position(*map(int, s.split(","))),
                end=Position(*map(int, e.split(","))),
            )
        )

    # we start checking the falling of the bricks from the bottom up
    bricks.sort(key=lambda b: b.start.z)

    # keep track of which bricks have fallen and which bricks they rest on
    fallen_bricks = {}
    max_z = 1
    for brick in bricks:
        has_rested = False
        intersecting = []
        # place brick just above last highest fallen brick position
        # to speed up the falling checks
        if brick.start.z > (max_z + 1):
            brick = brick.fall(max_z + 1)
        while not has_rested:
            intersecting.clear()
            if brick.start.z == 1:
                has_rested = True
                break
            test_brick = brick.fall()
            for other in reversed(fallen_bricks):
                if test_brick.intersects(other):
                    intersecting.append(other)
                    has_rested = True
            if not intersecting:
                brick = test_brick

        fallen_bricks[brick] = intersecting[:]
        max_z = max(max_z, brick.end.z)

    # only use the names here
    rests_on = {b.name: [rb.name for rb in v] for b, v in fallen_bricks.items()}
    supports = defaultdict(list)
    for b, rbs in fallen_bricks.items():
        for r in rbs:
            supports[r.name].append(b.name)

    result = 0
    cannot_be_removed = set()
    for b in rests_on:
        # see which other bricks it supports
        b_supports = supports[b]
        can_be_removed = True
        for bs in b_supports:
            if rests_on[bs] == [b]:
                # bs is only supported by b
                can_be_removed = False
                break
        if can_be_removed:
            result += 1
        else:
            cannot_be_removed.add(b)

    if part2:
        result = 0
        for b in cannot_be_removed:
            fallen = set([b])
            next_to_check = [(0, s) for s in supports[b]]
            while next_to_check:
                t, nb = next_to_check.pop()
                can_also_fall = True
                for ro in rests_on[nb]:
                    if ro not in fallen:
                        can_also_fall = False
                        break
                if can_also_fall:
                    fallen.add(nb)
                    for s in supports[nb]:
                        if s not in fallen:
                            next_to_check.append((t + 1, s))
            result += len(fallen) - 1  # remove the removed brick from the count

    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 5


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 375


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 7


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 72352


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
