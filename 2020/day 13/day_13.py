"""
Advent of Code 2020 - Day 13
Pieter Kitslaar
"""

from pathlib import Path
from functools import reduce

example = """\
939
7,13,x,x,59,x,31,19"""

def parse(txt):
    earliest_txt, bus_ids_txt = txt.splitlines()
    earlist_time = int(earliest_txt)
    bus_ids = [int(i) for i in bus_ids_txt.split(',') if i.isnumeric()]
    return earlist_time, bus_ids

def solve(txt):
    earliest, bus_ids = parse(txt)
    time_to_next=[]
    for bus_id in bus_ids:
        time_since_last_bus = earliest % bus_id
        time_to_next_bus = bus_id - time_since_last_bus
        time_to_next.append((time_to_next_bus, bus_id))
    time_to_next.sort()
    return time_to_next

def test_example():
    time_to_next = solve(example)
    answer = time_to_next[0][0]*time_to_next[0][1]
    assert((5, 59) == time_to_next[0])
    assert(295 == answer)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    time_to_next = solve(get_input())
    answer = time_to_next[0][0]*time_to_next[0][1]
    print('Part 1:', answer)

# taken from https://www.geeksforgeeks.org/python-program-for-basic-and-extended-euclidean-algorithms-2/
def gcdExtended(a, b):  
    # Base Case  
    if a == 0 :   
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a)  
     
    # Update x and y using results of recursive  
    # call  
    x = y1 - (b//a) * x1  
    y = x1  
     
    return gcd,x,y 

def solve_chinese_remainder(system):
    system.sort(key = lambda t: t[1])
    N = reduce(lambda a,b:a*b, [s[1] for s in system])
    while len(system) > 1:
        a1, n1 =  system.pop()
        a2, n2 = system.pop()
        gdc, m1, m2 = gcdExtended(n1,n2)
        x = a1*m2*n2 + a2*m1*n1
        system.append((x, n1*n2))
    return x % N

def test_chinese_example():
    """
    Sun-tzu's original formulation: 
    x ≡ 2 (mod 3) 
    x ≡ 3 (mod 5) 
    x ≡ 2 (mod 7) 
    with the solution x = 23 + 105k, where k ∈ ℤ
    """
    # remainder (a_i)  modulo (n_i)
    system = [  (2, 3), 
                (3, 5), 
                (2, 7)]
    assert(23 == solve_chinese_remainder(system))

def test_wiki_example():
    """
    x ≡ 0 (mod 3) 
    x ≡ 3 (mod 4) 
    x ≡ 4 (mod 5)   
    with the solution x =   39
    """
    system = [(0, 3), (3, 4), (4, 5)]
    assert(39 == solve_chinese_remainder(system))

def parse2(txt):
    bus_ids_txt = txt
    if len(txt.splitlines()) > 1:
        _, bus_ids_txt = txt.splitlines()
    return [(i,int(d)) for i,d in enumerate(bus_ids_txt.split(',')) if d.isnumeric()]

def test_example2():
    infos = parse2(example)
    system = [(-i[0],i[1]) for i in infos]
        
    """
    t =   0 + i0 *   7 => t ~  0 (mod 7)
      =  -1 + i1 *  13 => t ~ -1 (mod 13)
      =  -4 + i2 *  59 => t ~ -4 (mod 59)
      =  -6 + i3 *  31 => t ~ -6 (mod 31)
      =  -7 + i4 *  19 => t ~ -7 (mod 19)
    """
    assert(( 0,  7) == system[0])
    assert((-1, 13) == system[1])
    assert((-4, 59) == system[2])
    assert((-6, 31) == system[3])
    assert((-7, 19) == system[4])
    assert(1068781 == solve_chinese_remainder(system))

def solve_part2(txt):
    infos = parse2(txt)
    system = [(-i[0],i[1]) for i in infos]
    return solve_chinese_remainder(system)

def test_additional_part2():
    assert(3417 == solve_part2("17,x,13,19"))
    assert(754018 == solve_part2("67,7,59,61"))
    assert(779210 == solve_part2("67,x,7,59,61"))
    assert(1261476 == solve_part2("67,7,x,59,61"))
    assert(1202161486 == solve_part2("1789,37,47,1889"))


def test_part2():
    answer = solve_part2(get_input())
    print('Part 2:', answer)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_chinese_example()
    test_wiki_example()
    test_example2()
    test_additional_part2
    test_part2()
