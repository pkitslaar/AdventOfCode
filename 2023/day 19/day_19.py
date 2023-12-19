"""
Advent of Code 2023 - Day 19
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

from collections import namedtuple
from operator import gt, lt

OPS = {"<": lt, ">": gt}

Part = namedtuple("Part", "x m a s")


class Rule:
    def __init__(self, condition, target):
        self.condition = condition
        self.target = target

        if self.condition:
            self.part_element = self.condition[0]
            self.part_index = Part._fields.index(self.part_element)
            self.op_str = self.condition[1]
            self.op = OPS[self.op_str]
            self.op_value = int(self.condition[2:])

    def __repr__(self):
        return f"Rule({self.condition}, {self.target})"

    def apply(self, p: Part):
        if self.condition is None:
            return self.target
        if self.op(p[self.part_index], self.op_value):
            return self.target
        return None

    def apply_range(self, p: Part):
        if self.condition is None:
            return {self.target: p}
        p_min, p_max = p[self.part_index]
        match p_min, p_max, self.op_str, self.op_value,:
            case (a, _, ">", b) if a > b:
                # Complete range matching
                return {self.target: p}
            case (_, a, ">", b) if a <= b:
                # Complete range not matching
                return {None: p}
            case (_, _, ">", _):
                # Partial range
                non_match_p = p._replace(**{self.part_element: (p_min, self.op_value)})
                match_p = p._replace(**{self.part_element: (self.op_value + 1, p_max)})
                return {self.target: match_p, None: non_match_p}
            case (_, a, "<", b) if a < b:
                # p_max < op_value
                return {self.target: p}
            case (a, _, "<", b) if a >= b:
                # p_max >= op_value
                return {None: p}
            case (_, _, "<", _):
                # Partial range
                match_p = p._replace(**{self.part_element: (p_min, self.op_value - 1)})
                non_match_p = p._replace(**{self.part_element: (self.op_value, p_max)})
                return {self.target: match_p, None: non_match_p}
            case _:
                raise ValueError(f"Unknown situation: {self} {p}")


def test_rule():
    r = Rule("x<1416", "A")
    assert r.apply(Part(x=1415, m=0, a=0, s=0)) == "A"
    assert r.apply(Part(x=1415, m=1417, a=1418, s=1419)) == "A"
    assert r.apply(Part(x=1416, m=0, a=0, s=0)) == None
    assert r.apply(Part(x=1417, m=0, a=0, s=0)) == None
    assert r.apply(Part(x=1417, m=231, a=444, s=555)) == None

    r = Rule("m<1416", "A")
    assert r.apply(Part(x=0, m=1415, a=0, s=0)) == "A"
    assert r.apply(Part(x=0, m=1416, a=0, s=0)) == None
    assert r.apply(Part(x=0, m=1417, a=0, s=0)) == None

    r = Rule(None, "B")
    assert r.apply(Part(x=1415, m=0, a=0, s=0)) == "B"
    assert r.apply(Part(x=1415, m=1417, a=1418, s=1419)) == "B"
    assert r.apply(Part(x=1416, m=0, a=0, s=0)) == "B"
    assert r.apply(Part(x=1417, m=0, a=0, s=0)) == "B"
    assert r.apply(Part(x=1417, m=231, a=444, s=555)) == "B"


def parse_data(data):
    wf_lines, part_lines = data.split("\n\n")
    workflows = {}
    for line in wf_lines.splitlines():
        name, rules = line.split("{")
        rules = rules[:-1]
        wf_rules = []
        for r in rules.split(","):
            condition, target = r.split(":") if ":" in r else (None, r)
            wf_rules.append(Rule(condition, target))
        workflows[name] = wf_rules

    parts = []
    for line in part_lines.splitlines():
        p_info = {}
        for kv in line[1:-1].split(","):
            k, v = kv.split("=")
            p_info[k] = int(v)
        parts.append(Part(**p_info))
    return workflows, parts


def solve(data, part2=False):
    workflows, parts = parse_data(data)
    destinations = {"A": [], "R": []}
    if not part2:
        for p in parts:
            current = "in"
            while current not in "AR":
                for r in workflows[current]:
                    result = r.apply(p)
                    if result:
                        current = result
                        break
            destinations[current].append(p)
        result = sum(sum(p) for p in destinations["A"])
    else:
        R = (1, 4000)
        to_visit = [("in", Part(x=R, m=R, a=R, s=R))]
        destinations = {"A": [], "R": []}
        while to_visit:
            current, p = to_visit.pop()
            if current in "AR":
                destinations[current].append(p)
                continue
            current_p = p
            for r in workflows[current]:
                if current_p:
                    result = r.apply_range(current_p)
                    current_p = None
                    for target, p in result.items():
                        if target:
                            to_visit.append((target, p))
                        else:
                            current_p = p

        result = 0
        for p in destinations["A"]:
            this_combinations = (
                (p.x[1] - p.x[0] + 1)
                * (p.m[1] - p.m[0] + 1)
                * (p.a[1] - p.a[0] + 1)
                * (p.s[1] - p.s[0] + 1)
            )
            result += this_combinations

    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 19114


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 492702


def test_rule_apply_range():
    r = Rule("x<1416", "A")
    assert r.apply_range(Part(x=(0, 1415), m=(0, 10), a=(0, 10), s=(0, 10))) == {
        "A": Part(x=(0, 1415), m=(0, 10), a=(0, 10), s=(0, 10))
    }
    assert r.apply_range(Part(x=(1417, 2000), m=(0, 10), a=(0, 10), s=(0, 10))) == {
        None: Part(x=(1417, 2000), m=(0, 10), a=(0, 10), s=(0, 10))
    }

    assert r.apply_range(Part(x=(0, 1418), m=(0, 10), a=(0, 10), s=(0, 10))) == {
        "A": Part(x=(0, 1415), m=(0, 10), a=(0, 10), s=(0, 10)),
        None: Part(x=(1416, 1418), m=(0, 10), a=(0, 10), s=(0, 10)),
    }

    r = Rule("x>1416", "A")
    assert r.apply_range(Part(x=(0, 1415), m=(0, 10), a=(0, 10), s=(0, 10))) == {
        None: Part(x=(0, 1415), m=(0, 10), a=(0, 10), s=(0, 10))
    }
    assert r.apply_range(Part(x=(1417, 2000), m=(0, 10), a=(0, 10), s=(0, 10))) == {
        "A": Part(x=(1417, 2000), m=(0, 10), a=(0, 10), s=(0, 10))
    }

    assert r.apply_range(Part(x=(0, 1418), m=(0, 10), a=(0, 10), s=(0, 10))) == {
        None: Part(x=(0, 1416), m=(0, 10), a=(0, 10), s=(0, 10)),
        "A": Part(x=(1417, 1418), m=(0, 10), a=(0, 10), s=(0, 10)),
    }


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 167409079868000


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 138616621185978


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
