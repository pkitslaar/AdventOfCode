"""
Day 2 puzzle - Advent of Code 2019
Pieter Kitslaar
"""
def txt_values(txt):
    return [int(v) for v in txt.split(',')]

def run(in_values, noun_verb = None):
    values = in_values[:]
    if noun_verb:
        noun, verb = noun_verb
        values[1] = noun
        values[2] = verb
    current_pos = 0
    while True:
        op_code = values[current_pos]
        if op_code < 99:
            a, b, output = values[current_pos+1:current_pos+4]
            if op_code == 1:
                # addition
                values[output] = values[a] + values[b]
            elif op_code == 2:
                # multiply
                values[output] = values[a] * values[b]
            else:
                raise ValueError("Invalid op_code {op_code} at position {current_pos}")
        elif op_code == 99:
            break
        current_pos += 4
    return values

def test_examples():
    for in_, out_ in [
                ("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),
                ("1,0,0,0,99", "2,0,0,0,99"),
                ("2,3,0,3,99", "2,3,0,6,99"),
                ("2,4,4,5,99,0", "2,4,4,5,99,9801"),
                ("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"),
                
            ]:
        try:
            assert(txt_values(out_) == run(txt_values(in_)))
        except Exception as e:
            print(in_, out_)
            raise

def main():
    # Part 1
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        part1_txt = f.read()
    part1_data = txt_values(part1_txt)
    part1_output = run(part1_data, (12, 2))
    print(part1_output[0])

    # Part 2
    for noun in range(100):
        for verb in range(100):
            output = run(part1_data, (noun, verb))
            if output[0] == 19690720:
                print('noun', noun, 'verb', verb, 'result:', 100 * noun + verb)
                break
         