import sys
from pathlib import Path
d5_dir = Path(__file__).resolve().parents[1] / 'day 05'
assert(d5_dir.exists())
sys.path.append(str(d5_dir))
from day_05 import run, txt_values

with open(Path(__file__).parent / 'input.txt', 'r') as f:
    main_program = txt_values(f.read().strip())

def txt_input(txt):
    i = iter(txt)
    def get_v():
        return ord(next(i))
    return get_v

def part1():
    """
    ....@............
    ...@.@...........
    ..@...@..........
    #####.#..########
    ^C,D

    ........@........
    .......@.@.......
    ......@...@......
    #####.#..########
    ^B,D

    ......@..........
    .....@.@.........
    ....@...@........
    #####...#########
    ^A,^B,^C,D
    """

    instructions = "\n".join([p.strip().lstrip() for p in """\
    NOT C T
    NOT B J
    OR T J
    AND D J
    NOT A T
    AND B T
    AND C T
    AND D T
    OR T J
    WALK
    """.splitlines()])
    _, _, output = run(main_program, input_v=txt_input(instructions))
    chr_output = output
    num_output = None
    if output[-1] > 255:
        chr_output = output[:-1]
        num_output = output[-1]
    print(''.join(list(map(chr, chr_output))))
    if num_output:
        print('Part 1:', num_output)

def parse(txt):
    offset = None
    tiles = None
    jumps = None
    for l in txt.splitlines():
        if '#' in l:
            offset = l.index('#')
            tiles = [1 if t=='#' else 0 for t in l[offset:].strip()]
        if 'J' in l:
            jumps = [{'J':1, 'X':-1, ' ':0}[j]for j in l[offset:len(tiles)]]
            jumps += [0]*(len(tiles)-len(jumps))
    return tiles, jumps


def part2():
    a = """
    ......@...@......
    .....@.@.@.@.....
    ....@...@...@....
    #####.#.#..######
     XXXJ   J
        @  CD   H
            @ B D
    """
    A = parse(a)
    print(A)

    b = """
    ....@...@........
    ...@.@.@.@.......
    ..@...@...@......
    #####.#..########
    XXJ   J
      @  CD   H
          @ B D
    """
    B = parse(b)

    c = """
    .....@...@.......
    ....@.@.@.@......
    ...@...@...@.....
    #####..#.########
       @  CD
           @A  D
    """


    instructions = "\n".join([p.strip().lstrip() for p in """\
    NOT C J 
    AND D J 
    AND H J
    NOT B T 
    AND D T 
    OR T J
    NOT A T 
    OR T J
    RUN
    """.splitlines()])
    _, _, output = run(main_program, input_v=txt_input(instructions))
    chr_output = output
    num_output = None
    if output[-1] > 255:
        chr_output = output[:-1]
        num_output = output[-1]
    print(''.join(list(map(chr, chr_output))))
    if num_output:
        print('Part 2:', num_output)

if __name__ == "__main__":
    part1()
    part2()