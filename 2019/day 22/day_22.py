import itertools
import math
from functools import partial, lru_cache
from pathlib import Path
from tqdm import tqdm

def factory(x):
    return x

def apply_f(ab, x, N):
    return (ab['a']*x + ab['b']) % N

def deal_into_new_stack_ab(N):
    """
    Factored into f(x) = a*x + b (mod N)

    f(x) = N-1-x
         = -1*x + (N-1)
         = -1*x -1 + (N) (mod N)
         = -1*x -1

    """
    return dict(a=-1, b=-1)


def deal_into_new_stack(N, x):
    ab = deal_into_new_stack_ab(N)
    return apply_f(ab, x, N)

def test_deal_into_new_stack():
    deal_10 = partial(deal_into_new_stack, 10)
    d2 = deal_using_f(deal_10, range(10))
    assert(list(d2) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

def cut_N_cards_ab(N, cut):
    """
    Factored into f(x) = a*x + b (mod N)

    f(x) = x-cut (mod N)
         = 1*x - cut
    """
    return dict(a=1, b=-cut)

def cut_N_cards(N, cut, x):
    """
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    [3, 4, 5, 6, 7, 8, 9, 0, 1, 2] cut = 3
    [6, 7, 8, 9, 0, 1, 2, 3, 4, 5] cut =-4
    """
    ab = cut_N_cards_ab(N,cut)
    return apply_f(ab, x, N)

def test_cut_N_cards():
    cut_10_3 = partial(cut_N_cards, 10, 3)
    d2 = deal_using_f(cut_10_3, range(10))
    assert(list(d2) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

def test_cut_N_cards_negative():
    cut_10_n4 = partial(cut_N_cards, 10, -4)
    d2 = deal_using_f(cut_10_n4, range(10))
    assert(list(d2) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

def test_cut_7_cards_negative_3():
    cut_f = partial(cut_N_cards, 7, -3)
    d2 = deal_using_f(cut_f, range(7))
    assert(list(d2) ==  [4, 5, 6, 0, 1, 2, 3])

def test_cut_7_cards_n_3():
    cut_f = partial(cut_N_cards, 7, 3)
    d2 = deal_using_f(cut_f, range(7))
    assert(list(d2) ==  [3, 4, 5, 6, 0, 1, 2])

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

def deal_increment_ab(N, increment):
    """
    Factor into f(x) = a*x + b (mod N)

    f(x) = increment*x     (mod N)
         = increment*x + 0 (mod N)
    """
    return dict(a=increment, b=0)

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
    ab = deal_increment_ab(N, increment)
    new_position = apply_f(ab, x, N)
    return new_position

def deal_using_f(f, deck):
    new_positions = list(map(f, range(len(deck))))
    new_deck = [0]*len(deck)
    for i, p in enumerate(new_positions):
        new_deck[p] = deck[i]
    return new_deck

def test_deal_inc_11_3():
    deal_inc_11_3 = partial(deal_increment, 11, 3)
    d2 = deal_using_f(deal_inc_11_3, range(11))
    assert(list(d2) == [0, 4, 8, 1, 5, 9, 2, 6,10, 3, 7])

def test_deal_inc_10_1():
    deal_inc_10_1 = partial(deal_increment, 10, 1)
    d2 = deal_using_f(deal_inc_10_1, range(10))
    assert(list(d2) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


def test_deal_inc_11_2():
    deal_inc_11_2 = partial(deal_increment, 11, 2)
    d2 = deal_using_f(deal_inc_11_2, range(11))
    assert(list(d2) == [0, 6, 1, 7, 2, 8, 3, 9, 4,10, 5])

def test_deal_inc_10_3():
    deal_inc_10_3 = partial(deal_increment, 10, 3)
    d2 = deal_using_f(deal_inc_10_3, range(10))
    assert(list(d2) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3])

def test_deal_inc_10_7():
    deal_inc_10_7 = partial(deal_increment, 10, 7)
    d2 = deal_using_f(deal_inc_10_7, range(10))
    assert(list(d2) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])

def test_deal_inc_10_cards_9():
    deal_inc_10_9 = partial(deal_increment, 10, 9)
    #in_ = [8, 9, 0, 1, 2, 3, 4, 5, 6, 7]
    #out_= [8, 7, 6, 5, 4, 3, 2, 1,  0, 9]
    d2 = deal_using_f(deal_inc_10_9, range(10))
    assert(list(d2) == [0, 9, 8, 7, 6, 5, 4, 3, 2, 1])

def parse_funcs(txt, N):
    funcs_ab = []
    for l in txt.splitlines():
        if l.startswith('deal with increment'):
            num = int(l.rsplit(' ',1)[-1])
            funcs_ab.append(deal_increment_ab (N, num))
        elif l.startswith('cut'):
            num = int(l.rsplit(' ',1)[-1])
            funcs_ab.append(cut_N_cards_ab(N, num))
        elif l.startswith('deal into new stack'):
            funcs_ab.append(deal_into_new_stack_ab(N))
        else:
            raise ValueError('Unknown deal method', l)
    return funcs_ab

def solve_explicit(txt, num_cards=10):
    funcs_ab = parse_funcs(txt, num_cards)
    #funcs = [lambda x: apply_f(x=x, ab=f_ab, N=num_cards) for f_ab in funcs_ab]
    return list(solve2_explicit(funcs_ab, num_cards, range(num_cards)))

def solve2_explicit(funcs, N, x_seq):
    for f_ab in funcs:
        def f(x):
            return apply_f(f_ab, x, N)
        new_x_seq = deal_using_f(f, x_seq)
        x_seq = new_x_seq[:]
    return x_seq

def compose(ab, cd, num_cards):
    a,b,c,d = ab['a'], ab['b'], cd['a'], cd['b']
    return {
        'a': (a*c) % num_cards,
        'b': (b*c+d) % num_cards
    }

def solve_analytic_ab(txt, num_cards=10):
    funcs_ab = parse_funcs(txt, num_cards)
    ab = funcs_ab[0]
    for cd in funcs_ab[1:]:
        ab = compose(ab, cd, num_cards)
    return ab

def solve_analytic(txt, num_cards=10):
    ab = solve_analytic_ab(txt, num_cards)
    return solve2_explicit([ab], num_cards, range(num_cards))


example1 = """\
deal with increment 7
deal into new stack
deal into new stack
"""

def test_example1():
    for s_func in (solve_explicit, solve_analytic):
        d = s_func(example1, 10)
        assert(d == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7])

example2="""\
cut 6
deal with increment 7
deal into new stack
"""
#Result: 3 0 7 4 1 8 5 2 9 6
def test_example2():
    for s_func in (solve_explicit, solve_analytic):
        d = s_func(example2, 10)
        assert(d == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6])
    
example3="""\
deal with increment 7
deal with increment 9
cut -2
"""
#Result: 6 3 0 7 4 1 8 5 2 9
def test_example3():
    for s_func in (solve_explicit, solve_analytic):
        d = s_func(example3, 10)
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
    for s_func in (solve_explicit, solve_analytic):
        d = s_func(example4, 10)
        assert(d == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6])

def part1():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_input = f.read()
    if False:
        # Explicit
        d = solve_explicit(main_input, 10007)
        sol_part1 = d.index(2019)
        print('Part 1:', sol_part1)
        assert(7171 == sol_part1)

    # Analytic
    ab = solve_analytic_ab(main_input, 10007)
    sol_part1_analytic = apply_f(ab, 2019, 10007)
    print('Part 1 (analytic):', sol_part1_analytic)
    assert(7171 == sol_part1_analytic)

def pow_compose(f, k, N):
    g = dict(a=1, b=0)
    while k > 0:
        if k % 2 != 0:
            g = compose(g, f, N)
        k = k//2
        f = compose(f, f, N)
    return g


def part2():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_input = f.read()
    N = 119315717514047
    ab = solve_analytic_ab(main_input, N)

    # Now we have to resort to pure algebra to find the solution
    # to applying ab, num_repeats times
    # I took this from: https://codeforces.com/blog/entry/72593
    k = num_repeats = 101741582076661

    # This came from https://topaz.github.io/paste/#XQAAAQAgBQAAAAAAAAAzHIoib6pENkSmUIKIED8dy140D1lKWSMhNhZz+hjKgIgfJKPuwdqIBP14lxcYH/qI+6TyUGZUnsGhS4MQYaEtf9B1X3qIIO2JSejFjoJr8N1aCyeeRSnm53tWsBtER8F61O2YFrnp7zwG7y303D8WR4V0eGFqtDhF/vcF1cQdZLdxi/WhfyXZuWC+hs8WQCBmEtuId6/G0PeMA1Fr78xXt96Um/CIiLCievFE2XuRMAcBDB5We73jvDO95Cjg0CF2xgF4yt3v4RB9hmxa+gmt6t7wRI4vUIGoD8kX2k65BtmhZ7zSZk1Hh5p1obGZ6nuuFIHS7FpuSuv1faQW/FuXlcVmhJipxi37mvPNnroYrDM3PFeMw/2THdpUwlNQj0EDsslC7eSncZQPVBhPAHfYojh/LlqSf4DrfsM926hSS9Fdjarb9xBYjByQpAxLDcmDCMRFH5hkmLYTYDVguXbOCHcY+TFbl+G/37emZRFh/d+SkeGqbFSf64HJToM2I7N2zMrWP7NDDY5FWehD5gzKsJpEg34+sG7x2O82wO39qBlYHcYg1Gz4cLBrH1K1P+KWvEdcdj/NBtrl6yftMlCu6pH4WTGUe9oidaiRuQZOGtw71QsTQUuhpdoWO4mEH0U9+CiPZCZLaQolFDSky1J9nDhZZHy3+ETcUeDOfSu+HI3WuKC0AtIRPdG8B9GhtxZQKAx+5kyi/ek7A2JAY9SjrTuvRADxx5AikbHWXIsegZQkupAc2msammSkwY8dRMk0ilf5vh6kR0jHNbSi0g0KJLCJfqggeX24fKk5Mdh8ULZXnMfMZOmwEGfegByYbu91faLijfW4hoXCB1nlsWTPZEw2PCZqqhl9oc1q25H2YkkvKLxEZWl6a9eFuRzxhB840I1zdBjUVgfKd9/V4VdodzU2Z2e+VEh7RbJjQNFC/rG8dg==
    # Fermat's little theorem gives a simple inv:
    def inv(a, n): return pow(a, n-2, n)

    a, b = ab['a'], ab['b']
    A =  pow(a, k, N)
    B = (b*(A-1)*inv(a-1, N)) % N
    AB = {'a': A, 'b':B}
    
    # Now we want to find the reverse so we can see which
    # card ends up at position 2020
    # If f(x) = a*x + b
    # than the inverse f-1(x)
    # is f-1(x) = (x - B)/A
    sol = ((2020 - B)*inv(A,N)) % N
    print('Part 2:', sol)
    assert(73394009116480 == sol)


if __name__ == "__main__":
    part1()
    part2()