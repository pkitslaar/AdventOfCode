# Advent of code - 2018
# Day 7
#
# Pieter Kitslaar
#

import re
from collections import defaultdict
import string

pattern = re.compile('.* ([A-Z]) .* ([A-Z])')

# parse data
def parse(lines):
    depends = defaultdict(set)
    for line in lines:
            m = pattern.match(line)
            # get step and dependecy part
            step = m.group(2)
            dependecy = m.group(1)

            # record dependency
            depends[m.group(2)].add(m.group(1))
    return depends

def get_next_best_steps(depends, steps_to_test, finished): 
        # find all candidate steps 
        candidates = []
        for s in steps_to_test:
            try:
                s_dependency = depends[s]
                missing_deps = s_dependency - finished
                if not missing_deps:
                    candidates.append(s)
            except KeyError:
                # no dependecy defined
                # so always a candidate
                candidates.append(s)
        candidates.sort() # order alfabetically
        return candidates

# find best order
def best_order(depends, num_workers = 1, step_cost = None):
    # extract all steps from the dependency data
    steps_to_complete = set(depends)
    for v in depends.values():
        steps_to_complete.update(v)

    # setup the workers
    workers = {i:{} for i in range(num_workers)}

    order = []
    second = -1
    while steps_to_complete:
        second += 1

        # do work and check if it is  done 
        for w, step_info in workers.items():
            if step_info:
                step_info['time_left'] -= 1
                if step_info['time_left'] <= 0:
                    step = step_info['id']
                    step_info.clear()

                    order.append(step)
                    steps_to_test.remove(step)

        # fill work
        active = set(i['id'] for i in workers.values() if i)
        finished = set(order)
        next_candidates = [c for c in get_next_best_steps(depends, steps_to_complete, finished) if c not in active]
        if next_candidates:
            for w, step_info in workers.items():
                if not step_info:
                        # worker is free to work
                        step = next_candidates.pop(0)
                        step_info['id'] = step
                        step_info['time_left'] = step_cost[step] if step_cost else 1

                        if not next_candidates:
                            break

        # print status for debugging
        columns = [second]
        for w, step_info in workers.items():
            if step_info:
                columns.append(f"{step_info['id']}/{step_info['time_left']}")
            else:
                columns.append('.')
        columns.append(''.join(order) if order else '-')
        print('\t'.join(map(str, columns)))

    return order, second 


# Read the data
with open('input.txt', 'r') as f:
    challenge_depends = parse(f.readlines())

order, _ = best_order(challenge_depends, num_workers = 1, step_cost = None)
answer = ''.join(order)
print('PART 1:', answer)

# base cost of 60 and additional A=1, B=2 etc..
part2_cost = {letter:60+1+i for i, letter in enumerate(string.ascii_uppercase)}            
_, seconds = best_order(challenge_depends, num_workers = 5, step_cost = part2_cost)
print('PART 2:', seconds)

        
        
