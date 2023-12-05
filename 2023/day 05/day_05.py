"""
Advent of Code 2023 - Day 05
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


class Mapping:
    def __init__(self, d_start, s_start, length):
        self.d_start = d_start
        self.s_start = s_start
        self.length = length

    def map_value(self, value):
        s_diff = value - self.s_start
        if s_diff < 0 or s_diff >= self.length:
            return value
        return self.d_start + s_diff

    def __repr__(self) -> str:
        return f"Mapping({self.d_start}, {self.s_start}, {self.length})"


def parse(data):
    seeds = []
    maps = {}
    current_map = None
    for line in data.splitlines():
        if not line.strip():
            continue
        if not seeds and line.startswith("seeds:"):
            seeds = [*map(int, line.split(":")[1].split())]
            continue
        if " map:" in line:
            map_name = line.split(":")[0].split()[0]
            current_map = maps[map_name] = []
            continue
        assert current_map is not None
        current_map.append(Mapping(*map(int, line.split())))
    # sort the mappings by the start of the range
    for mapping in maps.values():
        mapping.sort(key=lambda m: m.s_start)

    return seeds, maps


def map_value(value, mappings):
    for mapping in mappings:
        new_value = mapping.map_value(value)
        if new_value != value:
            break
        value = new_value
    return new_value


MAPPING_TEST_DATA = """\
seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
"""


def test_mapping():
    m = [Mapping(52, 50, 48), Mapping(50, 98, 2)]
    for l in MAPPING_TEST_DATA.splitlines():
        try:
            seed, soil = map(int, l.split())
            assert soil == map_value(seed, m)
        except ValueError:
            pass


def test_mapping2():
    """
    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.
    """
    seeds, maps = parse(EXAMPLE_DATA)
    seed_to_soil = maps["seed-to-soil"]
    assert 81 == map_value(79, seed_to_soil)
    assert 14 == map_value(14, seed_to_soil)
    assert 57 == map_value(55, seed_to_soil)
    assert 13 == map_value(13, seed_to_soil)


def map_value_cascade(value, maps):
    for mapping in maps:
        value = map_value(value, mapping)
    return value


def test_mapping_cascade():
    """
    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35
    """
    seeds, maps = parse(EXAMPLE_DATA)
    assert 82 == map_value_cascade(79, maps.values())
    assert 43 == map_value_cascade(14, maps.values())
    assert 86 == map_value_cascade(55, maps.values())
    assert 35 == map_value_cascade(13, maps.values())


def solve(data, part2=False):
    seeds, maps = parse(data)
    locations = [map_value_cascade(seed, maps.values()) for seed in seeds]
    return min(locations)


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 35


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 525792406


from collections import namedtuple

DestToSourceRange = namedtuple("DestToSourceRange", "d_start d_end s_start s_end ")


def compute_dest_to_source_ranges(mappings, dest_range_min, dest_range_max):
    dest_to_source_ranges = []
    mappings.sort(key=lambda m: m.d_start)
    for m in mappings:
        if m.d_start > dest_range_max:
            continue
        if m.d_start + m.length <= dest_range_min:
            continue
        if not dest_to_source_ranges:
            if dest_range_min < m.d_start:
                dest_to_source_ranges.append(
                    DestToSourceRange(
                        dest_range_min, m.d_start, dest_range_min, m.d_start
                    )
                )

        if dest_to_source_ranges:
            prev_r = dest_to_source_ranges[-1]
            d_diff = m.d_start - prev_r.d_end
            assert d_diff >= 0
            if d_diff > 1:
                dest_to_source_ranges.append(
                    DestToSourceRange(prev_r.d_end, m.d_start, prev_r.s_end, d_diff)
                )
        d_start = max([dest_range_min, m.d_start])
        d_end = min([dest_range_max, m.d_start + m.length])
        s_start = m.s_start + d_start - m.d_start
        s_end = s_start + (d_end - d_start)
        dest_to_source_ranges.append(DestToSourceRange(d_start, d_end, s_start, s_end))
    if dest_to_source_ranges:
        prev_r = dest_to_source_ranges[-1]
        d_diff = dest_range_max - prev_r.d_end
        assert d_diff >= 0
        if d_diff > 1:
            dest_to_source_ranges.append(
                DestToSourceRange(
                    prev_r.d_end,
                    dest_range_max,
                    prev_r.d_end,
                    dest_range_max,
                )
            )
    else:
        # no ranges matches to dest and source ranges are same
        dest_to_source_ranges.append(
            DestToSourceRange(
                dest_range_min,
                dest_range_max,
                dest_range_min,
                dest_range_max,
            )
        )
    return dest_to_source_ranges


def test_compute_dest_to_source_ranges():
    _, maps = parse(EXAMPLE_DATA)
    this_mappings = maps["humidity-to-location"]
    """
    humidity-to-location map:
    60 56 37
    56 93 4
    """
    dest_to_source_ranges = compute_dest_to_source_ranges(this_mappings, 0, 100)
    assert dest_to_source_ranges == [
        DestToSourceRange(d_start=0, d_end=56, s_start=0, s_end=56),
        DestToSourceRange(d_start=56, d_end=60, s_start=93, s_end=97),
        DestToSourceRange(d_start=60, d_end=97, s_start=56, s_end=93),
        DestToSourceRange(d_start=97, d_end=100, s_start=97, s_end=100),
    ]

    dest_to_source_ranges = compute_dest_to_source_ranges(this_mappings, 57, 95)
    assert dest_to_source_ranges == [
        DestToSourceRange(d_start=57, d_end=60, s_start=94, s_end=97),
        DestToSourceRange(d_start=60, d_end=95, s_start=56, s_end=91),
    ]


from heapq import heappush, heappop, heapify

HeapElement = namedtuple("HeapElement", "map_index d_to_s_range")


def solve2(data):
    seeds, maps = parse(data)
    seed_ranges = [(s, s + l) for s, l in zip(seeds[::2], seeds[1::2])]
    seed_ranges.sort(key=lambda r: r[0])
    dest_min = 0
    mapping_keys = list(maps.keys())

    dest_max = 2 * max(m.d_start + m.length for m in maps[mapping_keys[-1]])
    to_visit = [
        HeapElement(len(mapping_keys) - 1, r)
        for r in compute_dest_to_source_ranges(
            maps[mapping_keys[len(mapping_keys) - 1]], dest_min, dest_max
        )
    ]
    heapify(to_visit)
    found_range = None
    while to_visit and not found_range:
        current = heappop(to_visit)
        if current.map_index == 0:
            c_start, c_end = current.d_to_s_range.s_start, current.d_to_s_range.s_end
            for r_start, r_end in seed_ranges:
                # find if ranges overlap
                if r_start >= c_end:
                    continue
                if r_end <= c_start:
                    continue
                # find the overlapping range
                found_range = (max(r_start, c_start), min(r_end, c_end))
                break
        else:
            prev_map_index = current.map_index - 1
            for r in compute_dest_to_source_ranges(
                maps[mapping_keys[prev_map_index]],
                current.d_to_s_range.s_start,
                current.d_to_s_range.s_end,
            ):
                heappush(to_visit, HeapElement(prev_map_index, r))
    lowest_location = map_value_cascade(found_range[0], maps.values())
    return lowest_location


def test_example2():
    result = solve2(EXAMPLE_DATA)
    print(f"example 2: {result}")
    assert result == 46


def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result == 79004094


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
