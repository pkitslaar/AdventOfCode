# Advent of code - 2018
# Day 8
#
# Pieter Kitslaar
#
from itertools import count

def empty(this_id = 0, parent=-1):
    return {'id': this_id, 
            'parent': parent, 
            'num_children': -1,
            'child_ids': [],
            'num_meta': -1,
            'meta': []}

def process(data, print_debug = False):
    max_id = count()
    nodes = {}
    stack = []
    def add_new_node(parent):
        n_id = next(max_id)
        n = empty(n_id, parent)
        nodes[n_id] = n
        stack.append(n)
        return n

    add_new_node(-1) # start with root 
    for c in data: 
        current = stack[-1]
        
        debug_line = None

        if current['num_children'] < 0:
            # start of header of new node
            current['num_children'] = c
            debug_line = f'{c:3}{" |"*(len(stack)-1)} {current["id"]:<3} NUM_CHILDREN'
        elif current['num_meta'] < 0:
            current['num_meta'] = c
            debug_line = f'{c:3}{" |"*(len(stack))} NUM_META'
            # end of header
            if current['num_children']:
                # this node has children so add them
                # and start processing these
                for i in range(current['num_children']):
                    child_n = add_new_node(parent = current['id'])
                    current['child_ids'].append(child_n['id'])
                current['child_ids'].reverse() # since we the first added gets processed last
        elif len(current['meta']) != current['num_meta']:
            current['meta'].append(c)
            debug_line = f'{c:3}{" |"*(len(stack))} META'
            if len(current['meta']) == current['num_meta']:
                stack.pop() # remove
        if debug_line and print_debug:
            print(debug_line)
    return nodes

def simple_meta_sum(nodes):
    return sum([sum(n['meta']) for n in nodes.values()]) 

def advanced_node_value(nodes, node_id, depth = 0):
    n = nodes[node_id]
    print(' '*depth, n)
    if n['num_children'] == 0:
        n['value'] = sum(n['meta'])
    else:
        value = 0
        for child_index in n['meta']:
            if child_index > 0 and (child_index-1) < len(n['child_ids']):
                child_id = n['child_ids'][child_index-1]
                value += advanced_node_value(nodes, child_id, depth+1)
        n['value'] = value

    print(' '*depth, n['value'])
    return n['value']
    

# Check example
example = [int(s.strip()) for s in '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split()]
example_nodes = process(example)
example_total_meta = simple_meta_sum(example_nodes)
assert(example_total_meta == 138)

# part 1
with open('input.txt', 'r') as f:
    data = map(int, f.read().split())

nodes = process(data, False)
total_meta = simple_meta_sum(nodes) 
print('PART 1:', total_meta)

example_root = [n for n in example_nodes.values() if n['parent'] == -1]
assert(len(example_root)==1)
print(advanced_node_value(example_nodes, example_root[0]['id']))

root = [n for n in nodes.values() if n['parent'] == -1]
assert(len(root)==1)
print(advanced_node_value(nodes, root[0]['id']))



                
        
             

        
        
