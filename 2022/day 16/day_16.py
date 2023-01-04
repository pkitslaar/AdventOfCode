"""
Advent of Code 2022 - Day 16
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent


def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

import networkx as nx

EXAMPLE_DATA="""\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""

import re
VALVE_NAME=re.compile("([A-Z]{2})")
FLOW_RATE=re.compile("(\d+)")

def parse(d):
    graph = nx.Graph()
    for line in d.splitlines():
        room_info, tunnel_info = line.split(';')
        valve_name = VALVE_NAME.search(room_info).group(0)
        valve_flow = int(FLOW_RATE.search(room_info).group(0))
        connectes_to = VALVE_NAME.findall(tunnel_info)
        #print(valve_name, valve_flow, connectes_to)
        for n in connectes_to:
            graph.add_edge(valve_name, n)
        nx.set_node_attributes(graph, {valve_name: {'flow_rate': valve_flow}})
    return graph

import heapq


from collections import namedtuple

class R(namedtuple("R", "t_elapsed current_pos open_valves flow_rate total_flow")):
    def sort_key(self):
        return (self.t_elapsed, -self.flow_rate, -self.total_flow)
    def __lt__(self, other):
        return self.sort_key() < other.sort_key()

def solve(d, T_END=30):
    """
    Old (not optimized) solution for part1.

    Was not able to leverage this for part2.
    See older commits for previous solve2 version.
    """
    graph = parse(d)
    flow_attributes = nx.get_node_attributes(graph, "flow_rate")
    all_valves = list(flow_attributes)

    pressure_valves = set([n for n,f in flow_attributes.items() if f > 0])

    distances = {}
    for v in all_valves:
        for v2 in pressure_valves: # only want to travel to pressure values
            if v != v2:
                distances.setdefault(v, {})[v2] = nx.shortest_path_length(graph, v, v2)

    routes = [R(0,'AA',[],0,0)]
    accepted = {} # time to total flow
    while routes:
        current = heapq.heappop(routes)
        if not current.t_elapsed in accepted or current.total_flow > accepted[current.t_elapsed]:
            accepted[current.t_elapsed] = current.total_flow

        new_routes = []
        for n_pos, length in distances[current.current_pos].items():
            if n_pos not in current.open_valves:
                new_valves = current.open_valves + [n_pos]
                new_r = R(
                    t_elapsed = current.t_elapsed + length + 1, # move and time to open valve
                    current_pos = n_pos,
                    open_valves=new_valves,
                    flow_rate=sum(flow_attributes[v] for v in new_valves),
                    total_flow = current.total_flow + (length+1)*current.flow_rate
                )
                new_routes.append(new_r)

        # just wait here until time is over
        num_remainig = T_END - current.t_elapsed
        if num_remainig > 0 and current.open_valves:
            new_r = current._replace(
                t_elapsed = T_END, 
                total_flow = current.total_flow + num_remainig*current.flow_rate,
            )
            new_routes.append(new_r)
        
        for new_r in new_routes:
            if new_r.t_elapsed <= T_END:
                if not new_r.t_elapsed in accepted or accepted[new_r.t_elapsed] < new_r.total_flow:
                    heapq.heappush(routes, new_r)

    return max(accepted.values())            


def test_example():
    result = solve2(EXAMPLE_DATA)
    assert(1651 == result)

def test_part1():
    result = solve2(data())
    print('PART 1:', result)
    assert(1741 == result)

class R2(namedtuple("R2", "t_remaining current valves total_flow")):
    def sort_key(self):
        return (self.t_elapsed, -self.flow_rate, -self.total_flow)
    def __lt__(self, other):
        return self.sort_key() < other.sort_key()


def solve2(d, T_END=30, part2=False):
    """
    Original code was re-worked after lookin at solution at: 
    https://github.com/noah-clements/AoC2022/blob/master/day16/day16.py

    Main idea, I did not see was to key each state as a bit-pattern of the
    open valves and keep track of the maximum for each state.

    Later these maximum values per state can be used to find mutually exclusive states when finding the 
    solution for both me and the elephant (in PART 2)

    The older solve2 version did produce the correct answer but did not finish.
    I just used the highest max_flow value after a couple an two hours brute-force which
    happend to be the correct one.
    """
    graph = parse(d)
    flow_attributes = nx.get_node_attributes(graph, "flow_rate")
    all_valves = list(flow_attributes)

    pressure_valves = tuple([n for n,f in flow_attributes.items() if f > 0])
    valve_bits = {v:1<<i for i,v in enumerate(pressure_valves)}

    distances = {}
    for v in all_valves:
        for v2 in pressure_valves: # only want to travel to pressure values
            if v != v2:
                distances.setdefault(v, {})[v2] = nx.shortest_path_length(graph, v, v2)

    states = [R2(
        t_remaining=T_END,
        current='AA', # all workers start a 'AA' and have no route to go to
        valves = 0, # no valves are open
        total_flow=0)]

    max_flow = {} # per valve set
    while states:
        current = states.pop()

        max_flow[current.valves] = max([max_flow.get(current.valves, 0), current.total_flow])
        for v in pressure_valves:
            if not (valve_bits[v] & current.valves): # valve already open
                t_remaining = current.t_remaining - distances[current.current][v] -1 
                if t_remaining > 0:
                    states.append(
                        current._replace(
                            t_remaining = t_remaining,
                            current = v,
                            valves = current.valves | valve_bits[v],
                            total_flow = current.total_flow + flow_attributes[v]*t_remaining
                        )
                    ) 
    if not part2:
        return max(max_flow.values())
    else:
        # find maximum of sum of mutually exclusive solutions e.g. v1 and v2 have no common bits
        return max(f1+f2 for v1,f1 in max_flow.items() for v2,f2 in max_flow.items() if not v1 & v2)

def test_example2():
    result = solve2(EXAMPLE_DATA, T_END=26, part2=True)
    assert(1707 == result)

def test_part2():
    result = solve2(data(), T_END=26, part2=True)
    print('PART 2:', result)
    assert(2316 == result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()
