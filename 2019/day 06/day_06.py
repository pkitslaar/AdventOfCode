"""
Day 6 - Advent of Code 2019
Pieter Kitslaar
"""
import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path
import matplotlib.pyplot as plt

def txt_to_graph(txt):
    G = nx.Graph()
    for l in txt.splitlines():
        orbits, planet = l.split(')')
        G.add_edge(planet, orbits)
    return G

def graph_to_image(graph, file_name, **kwargs):
    plt.figure()
    nx.draw(graph, **kwargs)
    plt.savefig(file_name)

def total_orbits(graph):
    total = 0
    for n in graph.nodes:
        sp = shortest_path(graph, source=n, target='COM')[1:]
        total += len(sp)
    return total

example = txt_to_graph("""\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""")

graph_to_image(example, 'example.png', with_labels=True)
assert(42 == (total_orbits(example)))

# Part 1
with open('input.txt', 'r') as f:
    data = f.read()
main_graph = txt_to_graph(data)

graph_to_image(main_graph, 'main_graph.png', node_size=3, font_color='red', labels={n:n for n in ('YOU', 'SAN')})


print('Part 1:', total_orbits(main_graph))

# Part 2
example2 = txt_to_graph("""\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""
)

graph_to_image(example2, 'example2.png', with_labels=True)

def min_orbit_transfers(graph, from_, to_):
    from_orbitting = list(graph.adj[from_].keys())[0]
    to_orbitting = list(graph.adj[to_].keys())[0]
    from_o_2_to_o = shortest_path(graph,from_orbitting, to_orbitting)[1:]
    return len(from_o_2_to_o)

assert(4 == min_orbit_transfers(example2, 'YOU', 'SAN'))

print('Part 2:', min_orbit_transfers(main_graph, 'YOU', 'SAN'))
