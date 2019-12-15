"""
Day 14 - Advent Of Code 2019
Pieter Kitslaar
"""

import numpy as np
import math
import networkx as nx

def parse_reactions(txt):
    reactions_graph = nx.DiGraph()
    reactions = []
    for l in txt.strip().splitlines():
        reaction = {'inputs': {}, 'outputs': {}}
        lhs, _, rhs = l.partition(' => ')
        for group, key in [(lhs, 'inputs'), (rhs, 'outputs')]:
            for p in group.split(','):
                amount, element = p.strip().split(' ')
                reaction[key][element] = int(amount)
        output_elements = reaction['outputs']
        assert(len(output_elements)==1)
        reaction['output_element'] = list(output_elements)[0]
        input_elements = reaction['inputs']
        for i_e in input_elements:
            for o_e in output_elements:
                reactions_graph.add_edge(i_e, o_e)
        reactions.append(reaction)
    element_order = list(nx.lexicographical_topological_sort(reactions_graph))
    reactions.sort(key = lambda r: element_order.index(r['output_element']))
    return reactions, element_order 
    

class ReactionTable:
    def __init__(self, reactions_, all_elements_, reverse=False):
        self.reactions = reactions_
        self.all_elements = all_elements_
        if reverse:
            self.reactions.reverse()
            self.all_elements.reverse()
        raw_table = []
        for react in self.reactions:
            elem_mutations = []
            r_inputs = react['inputs']
            r_outputs = react['outputs']
            for elem in self.all_elements:
                if elem in r_inputs:
                    elem_mutations.append(-r_inputs[elem])
                elif elem in r_outputs:
                    elem_mutations.append(r_outputs[elem])
                else:
                    elem_mutations.append(0)
            raw_table.append(elem_mutations)
        self.table = np.array(raw_table, dtype=np.int64)
        if reverse:
            self.table = -1*self.table

    def mix(self, num_reacts, summed_offset=0, debug=False):
        new_mix = None
        mixed = np.array(num_reacts)[:,np.newaxis]*self.table
        summed = np.sum(mixed, axis=0)
        summed[-1] += summed_offset
        if debug:
            print(summed)
        c_to_fix = -1
        c_value = 0
        for c, v  in enumerate(summed):
            if c > 0: # skip the ORE
                if v < 0:
                    c_to_fix = c
                    c_value = v
        #print('column to fix', c_to_fix)
        if c_to_fix > -1:
            # find reaction to create element of c
            r_index = -1
            r_factor = 0
            for i, r in enumerate(self.table):
                if r[c_to_fix] > 0:
                    r_factor = r[c_to_fix]
                    r_index = i
            fix_amount = math.ceil(abs(c_value)/r_factor)
            #print('reaction to use', r_index, 'amount', fix_amount)
            new_mix = num_reacts[:]
            new_mix[r_index] += fix_amount
        return summed, new_mix
    
    def solve(self, target_value = 1, summed_offset=0, debug=False):
        new_mix = [0]*len(self.reactions)
        new_mix[-1] = target_value
        all_mixes = [new_mix]
        all_summed = []
        while True:
            summed, new_mix = self.mix(new_mix, summed_offset=summed_offset, debug=debug)
            if debug:
                print(summed)
            all_summed.append(summed)
            if new_mix is None:
                break
            else:
                all_mixes.append(new_mix)
                
        return all_summed[-1]

ex1_txt ="""\
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

def test_ex1():
    ex1_data = parse_reactions(ex1_txt)
    ex1 = ReactionTable(*ex1_data)
    ex1_solution = ex1.solve()
    assert(ex1_solution[0] == -31)


ex2_txt ="""\
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""
def test_ex2():
    ex2_data = parse_reactions(ex2_txt)
    ex2 = ReactionTable(*ex2_data)
    ex2_solution = ex2.solve()
    assert(ex2_solution[0] == -165)

ex3_txt ="""\
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""
def test_ex3():
    ex3_data = parse_reactions(ex3_txt)
    ex3 = ReactionTable(*ex3_data)
    ex3_solution = ex3.solve()
    assert(ex3_solution[0] == -13312)

ex4_txt = """\
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""
def test_ex4():
    ex4_solution = ReactionTable(*parse_reactions(ex4_txt)).solve()
    assert(ex4_solution[0] == -180697)

ex5_txt = """\
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""
def test_ex5():
    ex5_solution = ReactionTable(*parse_reactions(ex5_txt)).solve()
    assert(ex5_solution[0] == -2210736)

def binarySearch(func, l, r, x): 
  
    while l <= r: 
  
        mid = int(l + (r - l)/2); 
          
        # Check if x is present at mid 
        if func(mid) == x: 
            return mid 
  
        # If x is greater, ignore left half 
        elif func(mid) < x: 
            l = mid + 1
  
        # If x is smaller, ignore right half 
        else: 
            r = mid - 1
      
    # If we reach here, then the element was not present 
    return -1, r

#
num_ore = 1000000000000

def test_binary_search_examples():
    ex3_p2 = ReactionTable(*parse_reactions(ex3_txt))
    ex2_p2_sol = binarySearch(lambda f: -ex3_p2.solve(f)[0], 0, num_ore, num_ore)
    assert(82892753 == ex2_p2_sol[1])

    ex4_p2 = ReactionTable(*parse_reactions(ex4_txt))
    ex4_p2_sol = binarySearch(lambda f: -ex4_p2.solve(f)[0], 0, num_ore, num_ore)
    assert(5586022 == ex4_p2_sol[1])

    ex5_p2 = ReactionTable(*parse_reactions(ex5_txt))
    ex5_p2_sol = binarySearch(lambda f: -ex5_p2.solve(f)[0], 0, num_ore, num_ore)
    assert(460664 == ex5_p2_sol[1])

def main():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        puzzle_txt = f.read()

    p1_solution = ReactionTable(*parse_reactions(puzzle_txt)).solve()
    print('Part 1:', -p1_solution[0])

    part2 = ReactionTable(*parse_reactions(puzzle_txt))
    part2_sol = binarySearch(lambda f: -part2.solve(f)[0], 0, num_ore, num_ore)
    print('Part 2:', part2_sol[1])
    assert(1935265 == part2_sol[1])

if __name__ == "__main__":
    main()
     