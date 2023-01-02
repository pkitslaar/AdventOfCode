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
    result = solve(EXAMPLE_DATA)
    assert(1651 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(1741 == result)

if __name__ == "__main__":
    test_example()
    test_part1()
