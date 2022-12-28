"""
Advent of Code 2022 - Day 19
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read().strip()

EXAMPLE_DATA="""\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""

import re


def parse(d):
    blueprints = {}
    for line in d.strip().splitlines():
        bp_txt, rest = line.split(':')
        bp_number = int(bp_txt.split()[-1])
        robots = {}
        for robot_txt in rest.split('.'):
            if not robot_txt:
                continue
            robot_type, robot_cost = robot_txt.split(' costs ')
            robot_type = robot_type.strip().split()[1]
            costs = {}
            for cost_part in robot_cost.split(' and '):
                c_amount, c_type = cost_part.strip().split()
                costs[c_type] = int(c_amount)
            robots[robot_type] = costs
        # since the factory can only create a single robot each minute
        # it does not make sense to have more robots that harvest a resource
        # than the maximum resource cost needed to build another robot
        max_robots = {}
        for rb_type in robots:
            max_cost = 0
            for costs in robots.values():
                try:
                    this_cost = costs[rb_type]
                    max_cost = max([max_cost, this_cost])
                except KeyError:
                    pass
                if max_cost > 0:
                    max_robots[rb_type] = max_cost


        blueprints[bp_number] = {'robot_costs': robots, 'max_robots': max_robots}
    return blueprints

import collections
import math


class Option:
    def __init__(self, bp, t, robots, resources):
        self.bp = bp
        self.t = t
        self.robots = robots
        self.resources = resources

    def __str__(self):
        return f"t={self.t} resource={self.resources.items()} robots={self.robots.items()}"

    def sort_key(self):
        return (

            -self.resources['geode'],
            #-self.robots['geode'],
            -(self.robots['obsidian'] > 0),
            -(self.robots['clay'] > 0),
                                                    
            -len(self.robots),
            self.resources['ore'],
                        #self.t,

        )

    def __lt__(self, other):
        return self.sort_key() < other.sort_key()

    def can_create_robot_with_resources(self, robot_type, resources):
        test_resources = resources.copy()
        for r,v in self.bp['robot_costs'][robot_type].items():
            test_resources[r] -= v
        if all(v >= 0 for v in test_resources.values()):
            # enough resources
            return True, test_resources
        return False, resources

    def max_geodes(self, END_T):
        """The maximum number of geodes to obtain assuming you are able to build a new geode robot eveyr minute"""
        max_geode = self.resources['geode']
        nr_geode = self.robots['geode']
        for _ in range(self.t+1, END_T+1):
            max_geode += nr_geode
            nr_geode+=1
        return max_geode

    
    def next_options(self, END_T):
        # assume we do nothing until end
        t_remaining = END_T - self.t
        if t_remaining > 0:
            next_resources = self.resources.copy()
            for r,n in self.robots.items():
                next_resources[r] += n*t_remaining
            yield Option(self.bp, END_T, self.robots.copy(), next_resources)

        for robot, cost in self.bp['robot_costs'].items():
            if robot in self.bp['max_robots']:
                if self.robots[robot] >= self.bp['max_robots'][robot]:
                    # don't build more than needed robot
                    continue
            
            can_build = True
            needed_times = []
            for r,c in cost.items():
                needed = c - self.resources[r]
                if needed > 0:
                    nr = self.robots[r]
                    if nr > 0:
                        needed_times.append(math.ceil(needed/nr))
                    else:
                        can_build = False
                else:
                    needed_times.append(0)

            if can_build:
                max_needed_time = max(needed_times)
                new_t = self.t + max_needed_time+1
                if new_t <= END_T:
                    new_resources = self.resources.copy()
                    for r,n in self.robots.items():
                        new_resources[r] += (n*max_needed_time)
                    new_robots = self.robots.copy()
                    new_robots[robot] += 1
                    for r,c in cost.items():
                        new_resources[r] -= c
                    assert(all(v >= 0 for v in new_resources.values()))
                    for r,n in self.robots.items():
                        new_resources[r] += n

                    yield Option(
                        self.bp,
                        new_t, 
                        new_robots,
                        new_resources
                        )


            
import heapq

def solve(d, part2=False):
    blueprint = parse(d)
    END_T = 24
    if part2:
        END_T = 32
        blueprint = {bp_num:bp for bp_num, bp in blueprint.items() if bp_num <= 3}

    result = 0 if not part2 else 1
    for bp_num, bp in blueprint.items():
        options = [Option(bp,
                    t=1,
                    robots=collections.defaultdict(int,{'ore':1}),
                    resources=collections.defaultdict(int,{'ore':1}))]

        max_geode = 0
        while options:
            this_option = heapq.heappop(options)
            if True:
                if this_option.resources['geode'] > max_geode:
                    max_geode = this_option.resources['geode']
                    if this_option.t == END_T:
                        print(this_option)
                    # remove any options that theoretically cannot reach above max_geode
                    options = [opt for opt in options if opt.max_geodes(END_T) >= max_geode]
                    heapq.heapify(options)

            if this_option.t < END_T:
                for new_option in this_option.next_options(END_T):
                    if new_option.max_geodes(END_T) >= max_geode:
                        heapq.heappush(options, new_option)
                    
        if not part2:
            result += bp_num*max_geode
        else:
            result *= max_geode
    return result



def test_example():
    result = solve(EXAMPLE_DATA)
    assert(33 == result)
    print('example OK')

def test_part1():
    print('Computing part 1')
    result = solve(data())
    print('PART 1:', result)
    assert(result == 1413) 

def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    assert(56*62 == result)
    print('example 2 OK')

def test_part2():
    result = solve(data(), part2=True)
    print('PART 2:', result)
    assert(21080 == result)

    
if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()