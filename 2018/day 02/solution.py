# Advent of code - 2018
# Day 2
#
# Pieter Kitslaar
#

from collections import Counter, defaultdict

# read the data
data = []
with open('input.txt', 'r') as f:
    for l in f:
        data.append(l.strip())

# global list which counts how often the same
# characters appear in the data 
counts_per_value = Counter()
for d in data:
    # count the occurse of each character
    char_counts = Counter(d)
    # add one to each occurence length
    counts_per_value.update({v:1 for v in char_counts.values()})
print(counts_per_value)
print(f'PART 1: {counts_per_value[2]} * {counts_per_value[3]} = {counts_per_value[2]*counts_per_value[3]}') # part 1
print()

# Check all lines have the same length
lengths_per_line_histogram = Counter([len(d) for d in data])
print(lengths_per_line_histogram)
assert(1 == len(lengths_per_line_histogram))
line_length = len(data[0])

# mask out every column
for i in range(line_length):
    mask_dict = defaultdict(list)
    for data_index, d in enumerate(data):
        mask_key = f'{d[:i]}{d[i+1:]}'
        mask_dict[mask_key].append((data_index, d))
        if len(mask_dict[mask_key]) > 1:
            # found solution
            print('PART 2: ', mask_key)

            # some more details (not needed for solution
            # but nice to see)
            print(' position in string', i,)
            print(' data entries (index, value):')
            for v in mask_dict[mask_key]:
                print(f' {v[0]:3} {v[1]}')
            indicator = list(' '*line_length)
            indicator[i] = '^'
            print(f'     {"".join(indicator)}')
            

    
