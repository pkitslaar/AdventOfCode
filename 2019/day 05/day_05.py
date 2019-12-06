"""
Day 5 puzzle - Advent of Code 2019
Pieter Kitslaar
"""
POSITION_MODE, IMMEDIATE_MODE = range(2)

def txt_values(txt):
    return [int(v) for v in txt.split(',')]

def handle_v(t, values):
    return t[0] if t[1] == IMMEDIATE_MODE else values[t[0]]

def run(in_values, input_v=0, noun_verb = None, assume_mode=POSITION_MODE, debug_output=False):
    outputs = []
    values = in_values[:]
    if noun_verb:
        noun, verb = noun_verb
        values[1] = noun
        values[2] = verb
    current_pos = 0
    while True:
        if debug_output:
            print(input_v, ["{0}{1}".format(v, ['','*'][i==current_pos]) for i,v in enumerate(values)])
        op_code = values[current_pos]
        param_modes = [assume_mode]*4 # assume immediate mode for all parameters
        if op_code > 99:
            op_code_digits = "{0:04}".format(op_code)            
            op_code = int(op_code_digits[-2:])
            for i, p_m in enumerate(reversed(op_code_digits[:-2])):
                param_modes[i] = int(p_m)
        if op_code < 99:
            if op_code == 1:
                # addition
                a, b, output = tuple(zip(values[current_pos+1:current_pos+4], param_modes))
                #assert(output[1]==0)
                values[output[0]] = handle_v(a, values) + handle_v(b,values)
                current_pos += 4
            elif op_code == 2:
                # multiply
                a, b, output = tuple(zip(values[current_pos+1:current_pos+4], param_modes))
                #assert(output[1]==0)
                values[output[0]] = handle_v(a,values) * handle_v(b,values)
                current_pos += 4
            elif op_code == 3:
                # set from input
                output = tuple(zip(values[current_pos+1:current_pos+2], param_modes))[0]
                #assert(output[1]==0)
                values[output[0]] = input_v
                current_pos += 2
            elif op_code == 4:
                # set to output
                a = tuple(zip(values[current_pos+1:current_pos+2],param_modes))[0]                
                outputs.append(handle_v(a, values))
                current_pos += 2
            elif op_code == 5:
                # jump if true
                a, b = tuple(zip(values[current_pos+1:current_pos+3],param_modes))
                if handle_v(a, values) != 0:                
                    current_pos = handle_v(b, values)
                else:
                    current_pos += 3
            elif op_code == 6:
                # jump if false
                a, b = tuple(zip(values[current_pos+1:current_pos+3],param_modes))
                if handle_v(a, values) == 0:                
                    current_pos = handle_v(b, values)
                else:
                    current_pos += 3
            elif op_code == 7:
                # less than
                a, b, output = tuple(zip(values[current_pos+1:current_pos+4],param_modes))
                #assert(output[1]==0)
                values[output[0]] = 1 if handle_v(a, values) < handle_v(b, values) else 0
                current_pos += 4
            elif op_code == 8:
                # equals
                a, b, output = tuple(zip(values[current_pos+1:current_pos+4],param_modes))
                #assert(output[1]==0)
                A = handle_v(a, values)
                B = handle_v(b, values)
                O = output[0]
                values[O] = 1 if A == B else 0
                current_pos += 4
            else:
                raise ValueError(f"Invalid op_code {op_code} at position {current_pos}")
        elif op_code == 99:
            break
        
    return values, outputs


if False:
    for in_, out_ in [
                ("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),
                ("1,0,0,0,99", "2,0,0,0,99"),
                ("2,3,0,3,99", "2,3,0,6,99"),
                ("2,4,4,5,99,0", "2,4,4,5,99,9801"),
                ("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"),
                
            ]:
        try:
            assert(txt_values(out_) == run(txt_values(in_))[0])
        except Exception as e:
            print(in_, out_)
            raise

def get_valid_output(output):
    if (all(v == 0 for v in output[:-1])):
        return output[-1]
    raise ValueError("Invalid output", output)

with open('input.txt', 'r') as f:
    input_data = txt_values(f.read())

# Part 1
if True:
    p1_values, p1_output = run(input_data, input_v=1)
    p1_result = get_valid_output(p1_output)
    print('Part 1:', p1_result)
    assert(13294380 == p1_result)

# Part 2
def compute_run2(code, input_v, assume_mode=POSITION_MODE, debug_output=False):
    values, outputs = run(code, input_v=input_v, assume_mode=assume_mode, debug_output=debug_output)    
    #print(values)
    #print(outputs)
    return get_valid_output(outputs)

# test equal to 8
assert(compute_run2([3,9,8,9,10,9,4,9,99,-1,8], input_v=8) == 1)
assert(compute_run2([3,9,8,9,10,9,4,9,99,-1,8], input_v=7) == 0)
assert(compute_run2([3,9,8,9,10,9,4,9,99,-1,8], input_v=9) == 0)

# test less than 8
assert(compute_run2([3,9,7,9,10,9,4,9,99,-1,8], input_v=8) == 0)
assert(compute_run2([3,9,7,9,10,9,4,9,99,-1,8], input_v=7) == 1)
assert(compute_run2([3,9,7,9,10,9,4,9,99,-1,8], input_v=9) == 0)

# equal to 8 IMMEDIATE
assert(compute_run2([3,3,1108,-1,8,3,4,3,99], input_v=8) == 1)
assert(compute_run2([3,3,1108,-1,8,3,4,3,99], input_v=7) == 0)
assert(compute_run2([3,3,1108,-1,8,3,4,3,99], input_v=9) == 0)

# less than 8 IMMEDIATE
assert(compute_run2([3,3,1107,-1,8,3,4,3,99], input_v=8) == 0)
assert(compute_run2([3,3,1107,-1,8,3,4,3,99], input_v=7) == 1)
assert(compute_run2([3,3,1107,-1,8,3,4,3,99], input_v=9) == 0)

# jump test POSITION MODE
assert(compute_run2([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], input_v=0) == 0)
assert(compute_run2([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], input_v=1) == 1)
assert(compute_run2([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], input_v=2) == 1)

# jump test IMMEDIATE MODE
assert(compute_run2([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], input_v=0) == 0)
assert(compute_run2([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], input_v=1) == 1)
assert(compute_run2([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], input_v=2) == 1)

# large example
large_data = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

assert(compute_run2(large_data, input_v=7) == 999) # below 8
assert(compute_run2(large_data, input_v=8) == 1000) # equal 8
assert(compute_run2(large_data, input_v=9) == 1001) # above 8

part2_result = compute_run2(input_data, input_v=5)
print('Part 2:', part2_result)
assert(11460760 == part2_result)