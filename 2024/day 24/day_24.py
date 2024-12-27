"""
Advent of Code 2024 - Day 24
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""

import networkx as nx

def parse(data):
    G = nx.DiGraph()
    for line in data.strip().splitlines():
        if not line.strip():
            continue
        if '->' in line:
            a, b = line.split('->')
            a1, op, a2 = a.split()
            G.add_node(b.strip(), op=op, output=None)
            G.add_edge(a1.strip(), b.strip())
            G.add_edge(a2.strip(), b.strip())
        else:
            a, b = line.split(':')
            G.add_node(a.strip(), op=None, output=int(b.strip()))
    return G

OPS = {'AND': lambda a, b: a & b, 
       'OR': lambda a, b: a | b, 
       'XOR': lambda a, b: a ^ b}

def solve(data, part2=False):
    g : nx.DiGraph = parse(data)
    for n in nx.lexicographical_topological_sort(g):
        n_op = g.nodes[n]['op']
        inputs = [g.nodes[i]['output'] for i in g.predecessors(n)]
        if inputs:
            g.nodes[n]['output'] = OPS[n_op](inputs[0], inputs[1])
        #print(n, g.nodes[n]['op'], g.nodes[n]['output'], inputs)
    z_values = {n: g.nodes[n]['output'] for n in g.nodes if n.startswith('z')}
    z_bits = ''.join(str(v) for _, v in sorted(z_values.items(), reverse=True))
    return int(z_bits, 2)


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 4

EXAMPLE_DATA2 = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""

def test_example_larger():
    result = solve(EXAMPLE_DATA2)
    print(f"example: {result}")
    assert result == 2024

def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 47666458872582


EXAMPLE_DATA_PART2 = """\
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
"""	

def node_layer(n):
    if n[0] == 'x':
        return ord('a')+int(n[1:])
    elif n[0] == 'y':
        return ord('a')-1  
    elif n[0] == 'z':
        return ord('z')+1
    else:
        return ord(n[0])

def draw_graph(sub_g, start_node= None):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    x_values = {n:int(n[1:]) for n in sub_g.nodes if n[0] == 'x'}
    y_values = {n:int(n[1:]) for n in sub_g.nodes if n[0] == 'y'}

    pos = {}

    # define the positions of the x and y nodes on the left side of the graph
    for n_x, x in x_values.items():
       pos[n_x] = (-1, -1+2*x)
    for n_y, y in y_values.items():
       pos[n_y] = (-1,  -1+2*y+1)
    
    # define the nodes in between the x and y nodes and the z nodes on the right side of the graph
    # x position is based on the topological sort of the nodes
    # y position is the average of the y position of the predecessors
    sorted_free_nodes = [n for n in nx.lexicographical_topological_sort(sub_g, key = lambda n: sub_g.nodes[n]['op'] or n) if n[0] not in 'xyz']
    for n_i, n in enumerate(sorted_free_nodes):
        preds = list(sub_g.predecessors(n))
        avg_y = sum(pos[p][1] for p in preds)/len(preds) if len(preds) != 0 else 0
        pos[n] = (n_i, avg_y)

    # find the current maxium x position
    max_x = max(p[0] for p in pos.values())

    # position of the z_nodes on the right side of the graph
    z_values = {n:int(n[1:]) for n in sub_g.nodes if n[0] == 'z'}
    for n_z, z in z_values.items():
       pos[n_z] = (max_x+1, -1+2*z+0.5)

   
    x_nodes = {n for n in sub_g.nodes if n[0] == 'x'}
    y_nodes = {n for n in sub_g.nodes if n[0] == 'y'}
    z_nodes = {n for n in sub_g.nodes if n[0] == 'z'}
    props = {'node_size': 700, }

    nx.draw_networkx_nodes(sub_g, pos, nodelist=x_nodes, node_color='r', ax = ax, **props)
    nx.draw_networkx_nodes(sub_g, pos, nodelist=y_nodes, node_color='g', ax = ax, **props)
    nx.draw_networkx_nodes(sub_g, pos, nodelist=z_nodes, node_color='b', ax = ax, **props)
    nx.draw_networkx_nodes(sub_g, pos, nodelist=[n for n in sub_g.nodes if n[0] not in 'xyz'], node_color='y', ax = ax, **props)

    nx.draw_networkx_edges(sub_g, pos, ax = ax, arrows=True, **props)
    op_nodes = {n for n in sub_g.nodes if sub_g.nodes[n]['op']}
    nop_nodes = {n for n in sub_g.nodes if not sub_g.nodes[n]['op']}
    nx.draw_networkx_labels(sub_g, pos, labels={n:f"{n}\n{sub_g.nodes[n]['op']}\nin:{','.join(sub_g.predecessors(n))}" for n in op_nodes}, ax = ax)
    nx.draw_networkx_labels(sub_g, pos, labels={n:f"{n}\nin:{','.join(sub_g.predecessors(n))}" for n in nop_nodes}, ax = ax)

    plt.show()
    return

def all_predecessors(g, n):
    preds = set(g.predecessors(n))
    new_preds = set()
    for p in preds:
        new_preds.update(all_predecessors(g, p))
        #preds.update(all_predecessors(g, p))
    preds.update(new_preds)
    return preds

def find_suc_node(g, A, B, n_type):
    for suc in g.successors(A):
        if set(g.predecessors(suc)) == {A, B}:
            suc_type = g.nodes[suc]['op']
            if suc_type == n_type:
                return suc
            else:
                print(f"Found alternative succesor from {A} and {B} of type {suc_type}: {suc}")
    print(f"Could not find node of type {n_type} from {A} and {B}")
    return None

def solve2(data):
    """
    The network is a series of full adders and half adders.
    Need to look for connections of the operators that are not correct.
    """
    
    # Mannually found these swaps by rendering the connections and looking for the patterns
    # in the full-adder networks that did not match.
    #
    # Not sure how to easily find the swaps automatically. 
    swap_outputs = {
        frozenset({'tvp', 'ggh', 'XOR'}): 'z05',
        frozenset({'sgt', 'bhb', 'OR'}): 'jst',

        frozenset({'x10', 'y10', 'AND'}): 'gdf',
        frozenset({'x10', 'y10', 'XOR'}): 'mcm',

        frozenset({'x15', 'y15', 'AND'}): 'dnt',
        frozenset({'vhr', 'dvj', 'XOR'}): 'z15',

        frozenset({'kgr', 'vrg', 'XOR'}): 'z30',
        frozenset({'kgr', 'vrg', 'AND'}): 'gwc',


    }
    new_data_lines = []
    for dl in data.strip().splitlines():
        if ' -> ' in dl:
            pre_arrow, post_arrow = dl.split(' -> ')
            pre_set = frozenset(pre_arrow.split())
            try:
                new_post = swap_outputs[pre_set]
                print(f'Swapping connection {pre_arrow} from {post_arrow} to {new_post}')
                new_data_lines.append(f'{pre_arrow} -> {new_post}')
            except KeyError:
                new_data_lines.append(dl)
                pass
        else:
            new_data_lines.append(dl)

    g : nx.DiGraph = parse("\n".join(new_data_lines))


    # check the adders in the network and break if there are issues    
    adders = {}
    for z_node in sorted([n for n in g.nodes if n.startswith('z')]):
        z = int(z_node[1:])
        issue = False
        if z == 0:
            # half adder
            A = 'x00'
            B = 'y00'
            S = z
            C_out = find_suc_node(g, A, B, 'AND')
            assert C_out
            adders[z] = {'A': A, 'B': B, 'S': S, 'C_out': C_out}
        else:
            if z >= 45:
                continue

            # full adder
            A = f'x{z:02}'
            B = f'y{z:02}'
            C_in = adders[z-1]['C_out']
            if not C_in:
                issue = True
            AB_XOR = find_suc_node(g, A, B, 'XOR')
            if not AB_XOR:
                issue = True
            S = find_suc_node(g, AB_XOR, C_in, 'XOR')
            if S is None:
                issue = True
            elif S != z_node:
                print(f"S node is not the expected z node: {z}, S: {S}, z_node: {z_node}")
                issue = True
            #assert S == z_node
            AB_AND = find_suc_node(g, A, B, 'AND')
            if not AB_AND:
                issue = True
            AB_XOR_Cin_AND = find_suc_node(g, AB_XOR, C_in, 'AND')
            if not AB_XOR_Cin_AND:
                issue = True
            C_out = find_suc_node(g, AB_AND, AB_XOR_Cin_AND, 'OR')
            if not C_out:
                issue = True
            adders[z] = {'A': A, 'B': B, 'S': S, 'C_out': C_out, 'C_in': C_in}  

        print(adders[z])
        if issue:
            # found issue so render the network up to the next z node
            z_pred = set()
            for zi in range(z+2):
                this_z_node =  f"z{zi:02}"
                z_pred.update(all_predecessors(g,this_z_node))
                z_pred.add(this_z_node)
            for adder_info in adders.values():
                z_pred.update(set(adder_info.values()))
            sub_g = g.subgraph(z_pred)
            draw_graph(sub_g)
            return
        
    # No issues return the sorted list of swapped outputs
    return ",".join(sorted(swap_outputs.values()))



def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result == "dnt,gdf,gwc,jst,mcm,z05,z15,z30"


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()