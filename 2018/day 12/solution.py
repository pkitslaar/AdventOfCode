# Advent of code - 2018
# Day 12
#
# Pieter Kitslaar
#

import numpy as np

EMPTY = -1
PLANT = 1

def to_arrays(data):
    """Turn the ASCII based state and rules into Numpy arrays.
    
    N.B. The array patterns are reversed with respect to the text
    version, since this is needed for the convolution.
    """
    array_data = data.copy()
    array_data['state'] = np.array([PLANT if c == '#' else EMPTY for c in data['state']])
    patterns = array_data['patterns'] = []
    for pattern, result in data['patterns_txt']:
        pattern_result = PLANT if result == '#' else EMPTY
        # we reverse the array pattern to make sure the convolution works correclty
        pattern_array = np.array([PLANT if c == '#' else EMPTY for c in reversed(pattern)])
        patterns.append((pattern_array, pattern_result))
    return array_data
    
def parse(data):
    """Process the format of the initial state and growth patterns."""
    initial_state = None
    patterns = []
    for line in data.splitlines():
        if not line.strip():
            continue
        if line.startswith('initial state:'):
            initial_state = line.split(':')[1].strip()
        else:
            pattern, result = [p.strip() for p in line.split('=>')]
            patterns.append((pattern, result))
    return to_arrays({'state': initial_state, 'patterns_txt': patterns, 'center': 0})

def prepare_new_state(data):
    """Create a copy of the data and updates the 'state' value
    always have enought EMPTY pots at the start and end to allow
    growth. Also updates the 'center' value to account for a shift
    of the state due to expansion or shrinkage.
    """
    old_state = data['state']
    
    insert_offset = 0
    center_offset = 0
    additional_size = 0
    
    # Check if enougth EMPTY pots at the start
    first_plant = np.argmax(old_state > EMPTY)
    if first_plant > 3:
        old_state = old_state[first_plant-3:]
        center_offset -= first_plant-3
    else:
        insert_offset += 3 - first_plant
        center_offset += 3 - first_plant
        additional_size += 3 - first_plant
    
    # Check for enough EMPTY pots at the end
    last_plant = len(old_state) - np.argmax(old_state[::-1] > EMPTY)
    num_empty_end = len(old_state) - last_plant
    if num_empty_end > 3:
        remove_part = num_empty_end - 3
        old_state = old_state[:-remove_part]
    else:
        additional_size += 3 - num_empty_end
    
    # Create the new state by starting with all pots as EMPTY
    # and copying in the old state
    new_state = EMPTY*np.ones(len(old_state)+additional_size, dtype=old_state.dtype)
    new_state[insert_offset:len(old_state)+insert_offset] = old_state # copy in old state
    
    # Create output and shift center
    new_data = data.copy()
    new_data['center'] += center_offset
    new_data['state'] = new_state
    return new_data

def print_state(data):
    state_array = data['state']
    print(" "*data['center'], '0', sep='')
    print(raw_state_txt(state_array))
    
def raw_state_txt(state_array):
    return "".join(["#" if i == PLANT else "." for i in state_array])
    
def do_step(data):    
    """Grow the state for one generation."""
    # make sure the new state has enough empty pots to allow growth
    new_data = prepare_new_state(data) 
    
    # Process all grow patterns
    pattern_states = []    
    for p, r in new_data['patterns']:
        # We perform a 'full' convolution to prevent boundary effects.
        # However, this means our output is larger than the input. 
        # Therefore we later shift the center to account for this.
        conv = np.convolve(new_data['state'] , p, 'full')
        match = r*(conv == 5)
        pattern_states.append(match)
    combined = np.vstack(pattern_states)
    
    # Find the summed result of the growth rules
    summed = np.sum(combined, axis=0)
    
    # Assume all pots empty first
    # and fill pots with plant if the growth rules resulted in a positive outcome
    new = EMPTY*np.ones_like(summed)
    new[summed > 0] = PLANT
    new_data['state'] = new
    new_data['center'] += 2 # Due to 'full' convolution earlier.
    return new_data
    
def grow(inital_data, num_generations):
    data = inital_data
    prev_data = data
    for step in range(num_generations):
        data = do_step(data)
        # Check if the outcome state is the same as previous step
        # If this is the case the outcome from now on will alwyas be
        # the same. The only difference is a shift of the center.
        # We can account for this shift till the end and quickly return.
        if data['state'].shape == prev_data['state'].shape:
            if np.all((data['state'] - prev_data['state']) == 0):
                center_delta = data['center'] - prev_data['center']
                steps_left = num_generations-step-1
                data['center'] += center_delta*steps_left
                break
        prev_data = data
    checksum = np.sum(np.nonzero(data['state'] == PLANT) - data['center'])
    return checksum

# Test example
with open('example.txt', 'r') as f:
    example_data = parse(f.read())
assert(325 == grow(example_data, 20))

# Assignment
with open('input.txt', 'r') as f:
    initial_test_data = parse(f.read())

print('PART 1:', grow(initial_test_data, 20))

NUM_GENERATIONS = 50000000000
print('PART 2:', grow(initial_test_data, NUM_GENERATIONS))