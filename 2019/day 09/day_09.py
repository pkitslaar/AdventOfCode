"""
Day 9 puzzle - Advent of Code 2019
Pieter Kitslaar
"""
import sys
from pathlib import Path
d5_dir = Path(__file__).parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))
import importlib
import day_05
importlib.reload(day_05)
from day_05 import run, txt_values

for in_, out_ in [("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),]:
    assert(txt_values(out_) == run(txt_values(in_))[1])

ex1_in_values = txt_values('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99')
ex1_pos, ex1_out_values, ex1_output = run(ex1_in_values)
assert(ex1_in_values == ex1_output)

ex2_in_values = txt_values('1102,34915192,34915192,7,4,7,99,0')
_, _, ex2_output = run(ex2_in_values)
assert(16 == len(str(ex2_output[0])))

ex3_in_values = txt_values('104,1125899906842624,99')
_, _, ex3_output = run(ex3_in_values)
assert(1125899906842624 == ex3_output[0])

with open('input.txt', 'r') as f:
    data = txt_values(f.read())


_, _, part1_output = run(data, input_v=1)
print('Part 1:', part1_output[0])
assert(3063082071 == part1_output[0])

_, _, part2_output = run(data, input_v=2)
print('Part 2:', part2_output[0])
assert(81348 == part2_output[0])
