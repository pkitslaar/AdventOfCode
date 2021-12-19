"""
Advent of Code 2021 - Day 18
Pieter Kitslaar
"""

from pathlib import Path

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

import math

example="""\
[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]
"""

import ast
from collections import deque

def parse(txt):
    for line in txt.splitlines():
        yield ast.literal_eval(line)



import weakref
class Pair(dict):

    def create_child(self,**kwargs):
        return Pair(parent=weakref.ref(self), depth=self['depth']+1, **kwargs)

    def visit(self, func):
        func(self)
        l = self.get('left')
        if l:
            l.visit(func)
        r = self.get('right')
        if r:
            r.visit(func)

    def to_print(self):
        print_func = lambda p: print(' '*p['depth'], p['depth'], p.get('value'))
        self.visit(print_func)

    def to_list(self, containing_list=None):
        if containing_list is None:
            containing_list = []
        l = self.get('left')
        if l:
            if l.get('value') is None:
                l_list = []
                l.to_list(l_list)
                containing_list.append(l_list)
            else:
                containing_list.append(l['value'])
        r = self.get('right')
        if r:
            if r.get('value') is None:
                r_list = []
                r.to_list(r_list)
                containing_list.append(r_list)
            else:
                containing_list.append(r['value'])
        return containing_list

    def explode(self):
        return explode_tree(self)

    def split(self):
        return split_tree(self)

    def reduce(self):
        did_action = True
        while did_action:
            did_action = False
            for func in (explode_tree, split_tree):
                did_action = func(self)
                if did_action:
                    break
    
    def magnitude(self):
        v = self.get('value')
        if v is not None:
            return v
        else:
            return 3*self['left'].magnitude() + 2*self['right'].magnitude()


def tree(f,parent=None):
    if parent is None:
        parent=Pair(parent=None, depth=0, value=None, left=None, right=None)

    l,r=f
    parent['left']=tree(l, parent.create_child()) if isinstance(l,list) else parent.create_child(value=l)
    parent['right']=tree(r, parent.create_child()) if isinstance(r, list) else parent.create_child(value=r)
    return parent

def split_tree(t):
    node_list = []
    collect_func = lambda p: node_list.append(p)
    t.visit(collect_func)
    for n in node_list:
        n_v = n.get('value')
        if n_v is not None and n_v >= 10:
            del n['value']
            n['left']=n.create_child(value=math.floor(n_v/2))
            n['right']=n.create_child(value=math.ceil(n_v/2))
            return True
    return False

def explode_tree(t):
    node_list = []
    collect_func = lambda p: node_list.append(p)
    t.visit(collect_func)
    for i, n in enumerate(node_list):
        if n['depth']==4:
            v_left = n.get('left', {}).get('value')
            v_right = n.get('right', {}).get('value')
            if v_left is not None and v_right is not None:
                #print('explode', v_left, v_right)
                for l_i in range(i,0,-1):
                    l_n = node_list[l_i]
                    l_n_v = l_n.get('value')
                    if l_n_v is not None:
                        #print('adding left to', l_n_v)
                        l_n['value'] += v_left
                        break
                for r_i in range(i+3,len(node_list)):
                    r_n = node_list[r_i]
                    r_n_v = r_n.get('value')
                    if r_n_v is not None:
                        #print('adding right to', r_n_v)
                        r_n['value'] += v_right
                        break
                del n['left']
                del n['right']
                n['value'] = 0
                return True
    return False



def test_explode():
    for ex, answer in [ 
        ('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]', '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'),
        ('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]'),
        ('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]'),
        ('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]'),
        ('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
        ]:
        #print(ex)
        f = [*parse(ex)][0]
        #print(f)
        t = tree(f)
        did_explode = t.explode()
        result = t.to_list()
        assert did_explode
        expected = [*parse(answer)][0]
        #print('result    ', result)
        #print('expected  ', expected)
        assert result == expected
        #print('re-exploded', explode(result))

def test_split():
    for ex, answer in [ 
        ('[[[[0,7],4],[15,[0,13]]],[1,1]]', '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'),
        ('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]', '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]'),
        ('[[[[0,7],4],[[7,8],[13,0]]],[1,1]]', '[[[[0,7],4],[[7,8],[[6,7],0]]],[1,1]]'),

        ]:
        #print(ex)
        f = [*parse(ex)][0]
        t = tree(f)
        did_split = t.split()
        result = t.to_list()
        assert did_split
        #print('result    ', result)
        expected = [*parse(answer)][0]
        #print('expected  ', expected)
        assert result == expected


def test_reduce():
    for ex, answer in [
        ('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'),
        ]:
        f = [*parse(ex)][0]
        t = tree(f)
        t.reduce()
        result = t.to_list()
        expected = [*parse(answer)][0]
        assert result == expected

def add_reduce(pairs):
    current = []
    for p in pairs:
        #print('adding', p)
        current = [current, p] if current else p
        if len(current) > 1:
            #print(current)
            t = tree(current)
            t.reduce()
            current = t.to_list()
            #print(current)
    return current

example_a="""\
[1,1]
[2,2]
[3,3]
[4,4]
"""
example_a_added="""[[[[1,1],[2,2]],[3,3]],[4,4]]"""

example_b="""\
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
"""
example_b_added="""[[[[3,0],[5,3]],[4,4]],[5,5]]"""

example_c="""\
[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"""
example_c_added="""[[[[5,0],[7,4]],[5,5]],[6,6]]"""

example_d="""\
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]"""
example_d_added="""[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"""

example_e="""\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

example_e_added="""[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]"""



def test_examples1():
    for ex, answer in [
        (example_a, example_a_added),
        (example_b, example_b_added),
        (example_c, example_c_added),
        (example_d, example_d_added),
        (example_e, example_e_added),
        ]:
        result = add_reduce(parse(ex))
        print(result)
        expected = [*parse(answer)][0]
        print(expected)
        assert result == expected

def magnitude(f):
    t = tree(f)
    return t.magnitude()

def test_magnitude():
    for ex, answer in [
        ('[9,1]', 29),
        ('[1,9]', 21),
        ('[[9,1],[1,9]]', 129),
        ('[[1,2],[[3,4],5]]',143),
        ]:
        f = [*parse(ex)][0]
        m = magnitude(f)

def solve1(txt):
    added = add_reduce(parse(txt))
    return magnitude(added)

def test_solve1_example():
    assert 4140 == solve1(example_e)

def test_part1():
    result = solve1(get_input())
    print('Part 1', result)

def solve2(txt):
    all_pairs = [*parse(txt)]
    magnitudes = []
    for p_a in all_pairs:
        for p_b in all_pairs:
            added = add_reduce([p_a,p_b])
            magnitudes.append(magnitude(added))
    return max(magnitudes)

example_part2="""\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""

def test_solve2_example():
    result = solve2(example_part2)
    assert 3993 == result

def test_part2():
    result = solve2(get_input())
    print('Part 2', result)

if __name__ == "__main__":
    test_explode()
    test_split()
    test_reduce()
    test_examples1()
    test_magnitude()
    test_solve1_example()
    test_part1()
    test_solve2_example()
    test_part2()
