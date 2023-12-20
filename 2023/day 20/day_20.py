"""
Advent of Code 2023 - Day 20
Pieter Kitslaar
"""


from enum import Enum
from typing import Optional


class Pulse(Enum):
    HIGH = "HIGH"
    LOW = "LOW"


class BaseModule:
    def __init__(self, name, destinations, sources):
        self.name = name
        self.destinations = destinations
        self.sources = sources

    def state_str(self):
        return f"{self.__class__.__name__}({self.name} {self.state_content()})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.destinations=} {self.sources=})"

    def state_content(self):
        return "EMPTY"

    def handle_input(self, pulse: Pulse, src: Optional["BaseModule"] = None):
        raise NotImplementedError()


class Output(BaseModule):
    def __init__(self, name, destinations, sources):
        super().__init__(name, destinations, sources)

    def handle_input(self, pulse: Pulse, src: Optional[BaseModule] = None):
        return []


class Broadcaster(BaseModule):
    def __init__(self, name, destinations, sources):
        super().__init__(name, destinations, sources)

    def handle_input(self, pulse: Pulse, src: Optional[BaseModule] = None):
        return [(dest, pulse) for dest in self.destinations]


class FlipFlop(BaseModule):
    def __init__(self, name, destinations, sources):
        super().__init__(name, destinations, sources)
        self.state = "OFF"

    def state_content(self):
        return self.state

    def handle_input(self, pulse: Pulse, src: Optional[BaseModule] = None):
        if pulse == Pulse.HIGH:
            return []  # do nothing
        else:
            if self.state == "OFF":
                self.state = "ON"
                return [(dest, Pulse.HIGH) for dest in self.destinations]
            else:
                self.state = "OFF"
                return [(dest, Pulse.LOW) for dest in self.destinations]


class Conjunct(BaseModule):
    def __init__(self, name, destinations, sources):
        super().__init__(name, destinations, sources)
        self.remembered = {s: Pulse.LOW for s in sources}

    def state_content(self):
        return str(self.remembered)

    def handle_input(self, pulse: Pulse, src: Optional[BaseModule]):
        self.remembered[src] = pulse
        if any(p == Pulse.LOW for p in self.remembered.values()):
            return [(des, Pulse.HIGH) for des in self.destinations]
        else:
            return [(des, Pulse.LOW) for des in self.destinations]


import networkx as nx


def parse(data):
    graph = nx.DiGraph()
    module_types = {}
    for line in data.splitlines():
        source_raw, _, dest = line.partition(" -> ")
        source, m_type = (
            (source_raw[1:], source_raw[0])
            if source_raw[0] in "&%"
            else (source_raw, None)
        )
        module_types[source] = m_type
        for d in dest.split(", "):
            graph.add_edge(source, d)

    modules = {}
    for n in graph.nodes:
        sources = list(graph.predecessors(n))
        destinations = list(graph.successors(n))
        m_type = module_types.get(n)
        if m_type == "%":
            modules[n] = FlipFlop(n, destinations, sources)
        elif m_type == "&":
            modules[n] = Conjunct(n, destinations, sources)
        elif n == "broadcaster":
            modules[n] = Broadcaster(n, destinations, sources)
        else:
            modules[n] = Output(n, destinations, sources)
    return modules, graph


from heapq import heappush, heappop, heapify
from collections import Counter


def module_states(modules):
    return "|".join(m.state_content() for m in modules.values())


def run_cycle(modules, N, start_pulse=(0, "button", Pulse.LOW, "broadcaster")):
    states = {}
    pulse_counts = []
    all_pulses = []
    loop_detected = False
    for iteration in range(N):
        s = module_states(modules)
        if s in states:
            # print(f"Loop detected at iteration {iteration} with state {s}")
            loop_detected = True
            break
        pulse_counts.append(Counter())
        states[s] = iteration

        pulses = [start_pulse]
        heapify(pulses)
        while pulses:
            current = heappop(pulses)
            all_pulses.append((iteration, current))
            t, source, pulse, destination = current
            # print(t, source, pulse, destination)
            pulse_counts[-1][pulse] += 1

            new_pulses = modules[destination].handle_input(pulse, source)
            for new_destination, new_pulse in new_pulses:
                heappush(pulses, (t + 1, destination, new_pulse, new_destination))
    return pulse_counts, loop_detected, all_pulses


def solve(data):
    modules, _ = parse(data)
    N = 1000

    pulse_counts, loop_detected, _ = run_cycle(modules, N)
    cycle_length = len(pulse_counts)

    total_counts = Counter()
    if loop_detected:
        total_cycles = N // cycle_length
        for c in pulse_counts:
            total_counts += {k: total_cycles * v for k, v in c.items()}

        remaining = N % cycle_length
        for p in pulse_counts[:remaining]:
            total_counts += p
    else:
        for p in pulse_counts:
            total_counts += p

    result = total_counts[Pulse.HIGH] * total_counts[Pulse.LOW]
    return result


EXAMPLE_DATA = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""


def test_example1a():
    result = solve(EXAMPLE_DATA)
    print(f"example 1a: {result}")
    assert result == 32000000


EXAMPLE_DATA2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


def test_example1b():
    result = solve(EXAMPLE_DATA2)
    print(f"example 1b: {result}")
    assert result == 11687500


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 670984704


from math import lcm


def solve2(data):
    modules, graph = parse(data)
    sub_graphs = {}
    rx_source = modules["rx"].sources[0]
    for sub_end in graph.predecessors(rx_source):
        sub = nx.ancestors(graph, sub_end)
        sub_graphs[sub_end] = sub

    # all the subgraphs should only have the broadcaster in common
    common_ancestors = set.intersection(*sub_graphs.values())
    assert common_ancestors == {"broadcaster"}

    # find the cycle length for each subgraph when the rx input is high
    rx_input_cycles = []
    for sub_end, sub in sub_graphs.items():
        modules, _ = parse(data)  # we reparse the data to get a fresh set of modules
        sub_start = [m for m in modules["broadcaster"].destinations if m in sub][0]
        sub_modules = {m: modules[m] for m in sub}
        sub_modules[sub_start] = modules[sub_start]
        sub_modules[sub_end] = modules[sub_end]
        sub_modules[rx_source] = modules[rx_source]
        sub_modules["rx"] = modules["rx"]
        _, loop_detected, pulses = run_cycle(
            sub_modules, 10000, (0, "broadcaster", Pulse.LOW, sub_start)
        )
        assert loop_detected
        rx_pulses = []
        rx_high_pulses = []
        for iteration, (t, source, pulse, destination) in pulses:
            if sub_end == source and destination == rx_source:
                rx_pulses.append((iteration, pulse))
                if pulse == Pulse.HIGH:
                    rx_high_pulses.append((iteration, pulse))
        assert len(rx_high_pulses) == 1
        rx_high_iteration = rx_high_pulses[0][0] + 1
        rx_input_cycles.append(rx_high_iteration)

    result = lcm(*rx_input_cycles)
    return result


def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result < 802081241309052
    assert result < 535893376784112
    assert result > 262775362119546
    assert result == 262775362119547


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
