from pathlib import Path
import itertools

base_pattern = [0, 1, 0, -1]

def generate_patterns(num_output):    
    for i in range(num_output):
        repeats = i+1
        new_base = itertools.chain(
            itertools.repeat(base_pattern[0], repeats),
            itertools.repeat(base_pattern[1], repeats),
            itertools.repeat(base_pattern[2], repeats),
            itertools.repeat(base_pattern[3], repeats),
        )
        output = itertools.islice(itertools.cycle(new_base), 1, num_output+1)                
        yield  output

def test_generate_patterns():
    first_8 = list(generate_patterns(8))            
    assert(list(first_8[0]) == [ 1,  0, -1,  0,  1,  0, -1,  0])
    assert(list(first_8[1]) == [ 0,  1,  1,  0,  0, -1, -1,  0])
    assert(list(first_8[2]) == [ 0,  0,  1,  1,  1,  0,  0,  0])
    assert(list(first_8[3]) == [ 0,  0,  0,  1,  1,  1,  1,  0])
    assert(list(first_8[4]) == [ 0,  0,  0,  0,  1,  1,  1,  1])
    assert(list(first_8[5]) == [ 0,  0,  0,  0,  0,  1,  1,  1])
    assert(list(first_8[6]) == [ 0,  0,  0,  0,  0,  0,  1,  1])
    assert(list(first_8[7]) == [ 0,  0,  0,  0,  0,  0,  0,  1])

def fft(raw_values, num_phases):        
    values = raw_values[:]    
    num_outputs = len(values)
    for i in range(1,num_phases+1):
        new_values = [int(str(sum(v*p for v,p in zip(values, bp)))[-1]) for bp in generate_patterns(num_outputs)]
        values = new_values
    return ''.join(map(str, values))

def txt_to_values(txt):
    return [int(e) for e in txt.strip()]

def test_fft():
    assert('01029498' == fft(txt_to_values('12345678'), 4))
    assert('24176176' == fft(txt_to_values('80871224585914546619083218645595'), 100)[:8])
    assert('73745418' == fft(txt_to_values('19617804207202209144916044189917'), 100)[:8])
    assert('52432133' == fft(txt_to_values('69317163492948606335995924319873'), 100)[:8])

def fft_part2(input_txt, repeat, num_phases):
    offset = int(input_txt[:7])
    original_len = len(input_txt)
    full_len = original_len*repeat
    remainder_len = full_len - offset
    assert(remainder_len < offset) # with this assumption the repeat pattern simply adds all remaining digits

    # get the last part of the repeated pattern
    # here we use the itetools.cycle to create an endlessly repeating concationation
    # of the input data
    # the itertools.islice next efficiently only returns the items starting at the 
    # computed offset until the full_len
    values = [int(d) for d in itertools.islice(itertools.cycle(input_txt), offset, full_len)]

    # To compute the phases we use the observation that all the coeficients at this point
    # are 1. Which means we can simply add all the numbers "to the right" of the output
    # position to obtain the number at that position
    for i in range(num_phases):
        # Start with an actual sum of values
        start_v = sum(values)
        new_values = [start_v] # this is the first element for the next phase
        for v in values[:-1]:
            # here we simply take the previous number for the new phase (e.g. the sum)
            # and subtract the number from the previous phase
            # This makes it much faster to compute than to re-sum all the items
            # to the right again
            new_values.append(new_values[-1] - v)
        
        # take the last digit as the final output
        values = [int(str(v)[-1]) for v in new_values]
    # compute the first 8 digits as the output
    return_value = ''.join(map(str, values[:8]))
    return return_value

def test_fft_part2():
    assert('84462026' == fft_part2('03036732577212944063491565474664', 10000, 100))
    assert('78725270' == fft_part2('02935109699940807407585447034323', 10000, 100))
    assert('53553731' == fft_part2('03081770884921959731165446850517', 10000, 100))

  
def main():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        puzzel_txt = f.read().strip()
    print(len(puzzel_txt), len(puzzel_txt)/4)
    part1_sol = fft(txt_to_values(puzzel_txt), 100)[:8]
    print('Part 1:', part1_sol)
    assert(part1_sol == '34694616')

    part2_sol = fft_part2(puzzel_txt, 10000, 100)
    print('Part 2:', part2_sol)

if __name__ == "__main__":
    main()
