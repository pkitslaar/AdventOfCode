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

class R2(namedtuple("R2", "t_elapsed current_to_route open_valves valves_to_open flow_rate total_flow")):
    def sort_key(self):
        return (self.t_elapsed, -self.flow_rate, -self.total_flow)
    def __lt__(self, other):
        return self.sort_key() < other.sort_key()

import itertools

def solve2(d, n_workers = 2, T_END=26):
    graph = parse(d)
    flow_attributes = nx.get_node_attributes(graph, "flow_rate")
    all_valves = list(flow_attributes)

    pressure_valves = tuple([n for n,f in flow_attributes.items() if f > 0])
    max_flow_rate = sum(flow_attributes.values())

    distances = {}
    for v in all_valves:
        for v2 in pressure_valves: # only want to travel to pressure values
            if v != v2:
                distances.setdefault(v, {})[v2] = nx.shortest_path_length(graph, v, v2)


    OPT_OPEN_VALVE, OPT_MOVE_NEW_VALVE, OPT_MOVE, OPT_STAY = range(4)

    states = [R2(
        t_elapsed=0,
        current_to_route=tuple([('AA', None)]*n_workers), # all workers start a 'AA' and have no route to go to
        open_valves=(),
        valves_to_open=pressure_valves,
        flow_rate=0,
        total_flow=0)]


    num_skipped = 0
    num_visited = 0
    #visited = {} # time to total flow
    max_flow = 0
    while states:
        if num_visited % 100 == 0:
            print(max_flow, len(states), num_visited, num_skipped)
        current = states.pop()
        num_visited += 1
        #visited[current] = current.total_flow
        if current.total_flow > max_flow:
            max_flow = current.total_flow
      
        new_states = []
        n_workers = len(current.current_to_route)
        options = [OPT_STAY]*n_workers
        for i, c_2_r in enumerate(current.current_to_route):
            if c_2_r[1] == None: # no valve assigned
                if current.valves_to_open:
                    options[i] = OPT_MOVE_NEW_VALVE
                else:
                    options[i] = OPT_STAY
            elif len(c_2_r[1]) == 1 and c_2_r[0]==c_2_r[1][0]: # reached target
                assert(c_2_r[0] not in current.open_valves)
                options[i] = OPT_OPEN_VALVE
            else:
                options[i] = OPT_MOVE

        # base new state
        # - 1 minute passes
        # - total flow is increated with the current flow rate
        base_option = current._replace(
            t_elapsed=current.t_elapsed+1,
            total_flow = current.total_flow + current.flow_rate
        )

        # check if any workers need to
        # - move
        # - open a valve
        # - stay (e.g do nothing)
        for i, opt in enumerate(options):
            new_open_valves = list(base_option.open_valves)
            new_c_2_r = list(base_option.current_to_route) 
            new_flow_rate = base_option.flow_rate
            if opt == OPT_MOVE:
                c2r = base_option.current_to_route[i]
                r = c2r[1]
                n_c2r = (c2r[1][1], c2r[1][1:])
                new_c_2_r[i] = n_c2r
            elif opt == OPT_OPEN_VALVE:
                c2r = base_option.current_to_route[i]
                this_valve = c2r[0]
                new_c_2_r[i] = (this_valve, None) # mark to find new valve
                new_open_valves.append(this_valve)
                new_flow_rate += flow_attributes[this_valve]
            elif opt == OPT_STAY:
                # no need to update the base option
                continue
            
            # update the base option 
            base_option = base_option._replace(
                current_to_route = tuple(new_c_2_r),
                open_valves = tuple(new_open_valves),
                flow_rate = new_flow_rate
            )

        # check if any of the workers needs to move to a new valve
        workers_to_new_valve = [i for i,opt in enumerate(options) if opt==OPT_MOVE_NEW_VALVE]
        if workers_to_new_valve:
            valves_to_check = list(base_option.valves_to_open)
            while len(valves_to_check) < len(workers_to_new_valve):
                valves_to_check.append(None) # fill up with None up to the number of workers                
            for n_targets in itertools.permutations(valves_to_check, len(workers_to_new_valve)):
                new_c_2_r = list(base_option.current_to_route)
                for worker_i, target in zip(workers_to_new_valve, n_targets):
                    if target:
                        route = tuple(nx.shortest_path(graph, new_c_2_r[worker_i][0], target))
                        new_c_2_r[worker_i] = (route[1], route[1:])
                    else:
                        pass
                new_valves_to_open = tuple(set(base_option.valves_to_open) - set(n_targets))
                new_r = base_option._replace(
                    current_to_route=tuple(new_c_2_r),
                    valves_to_open= new_valves_to_open,
                )
                new_states.append(new_r)
        else:
            new_states.append(base_option)
        
        for new_r in new_states:
            num_skipped += 1
            if new_r.t_elapsed <= T_END:
                # check if the new state would be able to beat the current
                # max_flow if it would open all remaining valves for the remainder of the time
                t_valves_to_open = [(flow_attributes[v],v) for v in pressure_valves if v not in new_r.open_valves]
                t_valves_to_open.sort(reverse=True) # sort from highest flow_rate to lowest
                theoretical_max_flow = new_r.total_flow
                theoretical_flow_rate = new_r.flow_rate
                remaining_time = T_END - new_r.t_elapsed
                for _ in range(new_r.t_elapsed, T_END+1):
                    theoretical_max_flow += theoretical_flow_rate
                    for _ in range(n_workers):
                        if t_valves_to_open:
                            theoretical_flow_rate += t_valves_to_open.pop(0)[0]

                if theoretical_max_flow > max_flow:
                    states.append(new_r)
                    num_skipped -= 1
            

    return max_flow   

def test_example2():
    result = solve2(EXAMPLE_DATA)
    assert(1707 == result)

def test_part2():
    result = solve2(data())
    print('PART 2:', result)
    assert(2316 == result)

if __name__ == "__main__":
    #test_example()
    #test_part1()
    #test_example2()
    test_part2()
