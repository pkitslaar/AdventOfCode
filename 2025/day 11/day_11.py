"""
Advent of Code 2025 - Day 11
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

EXAMPLE_DATA_2 = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

import networkx as nx
from functools import lru_cache

# use lru_cache to memoize results to avoid recomputation 
# Got this tip from reddit
# when recursing to find number of paths
@lru_cache(maxsize=None)
def get_num_paths(g, source, target):
    result = 0
    # loop over successors of this source
    for successor in g.successors(source):
        if successor == target:
            result += 1
        else:
            result += get_num_paths(g, successor, target)
    return result
                

def test_get_num_paths():
    g = nx.DiGraph()
    g.add_edges_from([
        ('you', 'a'),
        ('you', 'b'),
        ('a', 'c'),
        ('a', 'd'),
        ('b', 'd'),
        ('c', 'out'),
        ('d', 'out'),
    ])
    #plot_graph(g, focus_nodes=())
    assert get_num_paths(g, 'you', 'a') == 1
    assert get_num_paths(g, 'you', 'b') == 1
    assert get_num_paths(g, 'you', 'c') == 1
    assert get_num_paths(g, 'you', 'd') == 2
    assert get_num_paths(g, 'you', 'out') == 3

def solve(data, part2=False):
    result = 0

    # create directed graph
    g  = nx.DiGraph()
    for line in data.strip().splitlines():
        source, targets = line.split(":")
        targets = targets.strip().split()
        for target in targets:
            g.add_edge(source.strip(), target.strip())
    # assert DAG
    assert nx.is_directed_acyclic_graph(g)

    num_paths = 0
    if not part2:
        # find all paths from 'you' to 'out'
        num_paths = get_num_paths(g, 'you', 'out')
    else:
        # find the number of paths that go through fft and dac
        # so either 
        # 1) svr -> fft -> dac -> out
        # 2) svr -> dac -> fft -> out
        # 
        for a, b in [('fft', 'dac'), ('dac', 'fft')]:
            # we want to find paths
            # svr -> a -> b -> out

            # if not paths between a and b, skip
            if not nx.has_path(g, a, b):
                continue

            # assert there are no paths from b to a (DAG)
            assert not nx.has_path(g, b, a)
            
            # first paths from svr to a
            n_svr_a = get_num_paths(g, 'svr', a)

            # paths that originate from a -> b 
            n_a_b = get_num_paths(g, a, b)

            # paths that originate from b -> out
            n_b_out = get_num_paths(g, b, 'out')

            # total paths is the product of the 3 sub-paths
            n_total = n_svr_a * n_a_b * n_b_out

            num_paths += n_total

    return num_paths


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 5


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 477


def test_example2():
    result = solve(EXAMPLE_DATA_2, part2=True)
    print(f"example 2: {result}")
    assert result == 2


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result != 2
    assert result > 406570283840
    assert result == 383307150903216


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()

if __name__ == "__main__":
    #test_example2()
    test_part2()