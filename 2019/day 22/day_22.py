import itertools
import math
from functools import partial, lru_cache
from pathlib import Path
from tqdm import tqdm

def factory(x):
    return x

def deal_into_new_stack(N, x):
    return N-1-x

def test_deal_into_new_stack():
    d = factory(10)
    deal_10 = partial(deal_into_new_stack, 10)
    d2 = map(deal_10, range(10))
    assert(list(d2) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

def cut_N_cards(N, cut, x):
    """
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    [3, 4, 5, 6, 7, 8, 9, 0, 1, 2] cut = 3
    [6, 7, 8, 9, 0, 1, 2, 3, 4, 5] cut =-4
    """
    if cut > 0:
        return (x+cut) % N
    else:
        return (x+(N+cut)) % N

def test_cut_N_cards():
    cut_10_3 = partial(cut_N_cards, 10, 3)
    d2 = map(cut_10_3, range(10))
    assert(list(d2) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

def test_cut_N_cards_negative():
    cut_10_n4 = partial(cut_N_cards, 10, -4)
    d2 = map(cut_10_n4, range(10))
    assert(list(d2) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

increment_brute_cache = {0:0}
def deal_increment_brute(N, increment, x):
    cache = increment_brute_cache.setdefault(N, {}).setdefault(increment, {})
    try:
        return cache[x]
    except KeyError:
        for i in range(N):
            j = (i*increment) % N
            cache[j] = i
            if j == x:
                return i

increment_fast_cache = {0:0}
def deal_increment_fast(N, increment, x):
    cache = increment_fast_cache.setdefault(N, {}).setdefault(increment, {})
    try:
        return cache[x]
    except KeyError:
        n = 0
        while True:
            i = x+N*n
            j, remainder = divmod(i, increment)
            if remainder == 0:
                cache[x] = j
                return j
            n+=1

def deal_increment(N, increment, x):
    """
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] increment=1
    [0, 7, 4, 1, 8, 5, 2, 9, 6, 3] increment=3
    [0, 3, 6, 9, 2, 5, 8, 1, 4, 7] increment=7
    [0, 9, 8, 7, 6, 5, 4, 3, 2, 1] increment=9

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10]
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10] N=11, increment=1
    [0, 6, 1, 7, 2, 8, 3, 9, 4,10, 5] N=11, increment=2 
    [0, 4, 8, 1, 5, 9, 2, 6,10, 3, 7] N=11, increment=3
    [0, 3, 6, 9, 1, 4, 7,10, 2, 5, 8] N=11, increment=4
    [0, 9, 7, 5, 3, 1,10, 8, 6, 4, 2] N=11, increment=5
    [0, 2, 4, 6, 8,10, 1, 3, 5, 7, 9] N=11, increment=6
    [0, 8, 5, 2,10, 7, 4, 1, 9, 6, 3] N=11, increment=7
    [0, 7, 3,10, 6, 2, 9, 5, 1, 8, 4] N=11, increment=8
    [0, 5,10, 4, 9, 3, 8, 2, 7, 1, 6] N=11, increment=9
    [0,10, 9, 8, 7, 6, 5, 4, 3, 2, 1] N=11, increment=11
    """
    #bf = deal_increment_brute(N, increment, x)
    ff = deal_increment_fast(N, increment, x)
    #if(bf != ff):
    #    raise ValueError(f"For {N=} {increment=} {x=} {bf} != {ff}")
    return ff

def test_deal_inc_11_3():
    deal_inc_11_3 = partial(deal_increment, 11, 3)
    d2 = map(deal_inc_11_3, range(11))
    assert(list(d2) == [0, 4, 8, 1, 5, 9, 2, 6,10, 3, 7])

def test_deal_inc_10_1():
    deal_inc_10_1 = partial(deal_increment, 10, 1)
    d2 = map(deal_inc_10_1, range(10))
    assert(list(d2) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

def test_deal_inc_10_3():
    deal_inc_10_3 = partial(deal_increment, 10, 3)
    d2 = map(deal_inc_10_3, range(10))
    assert(list(d2) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3])

def test_deal_inc_10_7():
    deal_inc_10_7 = partial(deal_increment, 10, 7)
    d2 = map(deal_inc_10_7, range(10))
    assert(list(d2) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])

def test_deal_inc_10_cards_9():
    deal_inc_10_9 = partial(deal_increment, 10, 9)
    #in_ = [8, 9, 0, 1, 2, 3, 4, 5, 6, 7]
    #out_= [8, 7, 6, 5, 4, 3, 2, 1,  0, 9]
    d2 = map(deal_inc_10_9, range(10))
    assert(list(d2) == [0, 9, 8, 7, 6, 5, 4, 3, 2, 1])

def parse_funcs(txt, N):
    funcs = []
    for l in txt.splitlines():
        if l.startswith('deal with increment'):
            num = int(l.rsplit(' ',1)[-1])
            funcs.append(partial(deal_increment, N, num))
        elif l.startswith('cut'):
            num = int(l.rsplit(' ',1)[-1])
            funcs.append(partial(cut_N_cards, N, num))
        elif l.startswith('deal into new stack'):
            funcs.append(partial(deal_into_new_stack, N))
        else:
            raise ValueError('Unknown deal method', l)
    return reversed(funcs)

def solve(txt, num_cards=10):
    funcs = parse_funcs(txt, num_cards)
    return list(solve2(funcs, range(num_cards)))

def solve2(funcs, x_seq):
    for f in funcs:
        new_x_seq = map(f, x_seq)
        x_seq = new_x_seq
    return x_seq

example1 = """\
deal with increment 7
deal into new stack
deal into new stack
"""

def test_example1():
    d = solve(example1, 10)
    assert(d == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])

example2="""\
cut 6
deal with increment 7
deal into new stack
"""
#Result: 3 0 7 4 1 8 5 2 9 6
def test_example2():
    d = solve(example2, 10)
    assert(d == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6])

example3="""\
deal with increment 7
deal with increment 9
cut -2
"""
#Result: 6 3 0 7 4 1 8 5 2 9
def test_example3():
    d = solve(example3, 10)
    assert(d == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9])

example4="""\
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""
#Result: 9 2 5 8 1 4 7 0 3 6
def test_example4():
    d = solve(example4, 10)
    assert(d == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])

def part1():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_input = f.read()
    d = solve(main_input, 10007)
    sol_part1 = d.index(2019)
    print('Part 1:', sol_part1)
    assert(7171 == sol_part1)

def test_reverse_lookup_example4():
    #assert(d == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])
    funcs = list(parse_funcs(example4, 10))
    solutions = [list(range(10))]
    for i in range(100):
        solutions.append(list(solve2(funcs, solutions[-1])))

    for i in range(10):
        assert((solutions[1][i],) == reverse_lookup(funcs, 1, i))
        assert((solutions[2][i],) == reverse_lookup(funcs, 2, i))
        assert((solutions[4][i],) == reverse_lookup(funcs, 4, i))
        assert((solutions[5][i],) == reverse_lookup(funcs, 5, i))
        assert((solutions[9][i],) == reverse_lookup(funcs, 9, i))
        assert((solutions[99][i],) == reverse_lookup(funcs, 99, i))


def part2():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_input = f.read()
    funcs = list(parse_funcs(main_input, 119315717514047))
    num_repeats = 101741582076661
    sol = reverse_lookup(funcs, num_repeats, target_idx=2020)
    print('Part 2:', sol)

def reverse_lookup(funcs, num_repeats, target_idx):
    d = (target_idx,)
    cache = {}
    repeat_i = -1
    values = []
    for i in tqdm(range(num_repeats)):
        try:
            new_d = cache[d]
            repeat_i = i
            print('repeat after', i, 'shuffles')
            break
        except KeyError:
            new_d = d
            for f in funcs:
                new_d = tuple(map(f, new_d))
            cache[d] = new_d
        #print(d, new_d)
        d = new_d
        values.append(d)

    if repeat_i > -1:
        num_remaining = num_repeats % (repeat_i)
        d = (target_idx,)
        for i in range(num_remaining):
            d = cache[d]
        return d
    return d

if __name__ == "__main__":
    #test_deal_inc_11_3()
    part1()
    part2()