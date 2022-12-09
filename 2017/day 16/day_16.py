"""
Advent of Code 2017 - Day 16
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

def solve(moves_txt, programs_txt):
    programs = list(programs_txt.strip())
    for move in moves_txt.strip().split(','):
        if move[0] == 's':
            num_spin = int(move[1:])
            programs = programs[-num_spin:] + programs[:-num_spin]
        elif move[0] == 'x':
            posA, posB = map(int, move[1:].split('/'))
            programs[posA], programs[posB] = programs[posB], programs[posA]
        elif move[0] == 'p':
            nameA, nameB = move[1:].split('/')
            posA = programs.index(nameA)
            posB = programs.index(nameB)
            programs[posA], programs[posB] = programs[posB], programs[posA]
        else:
            raise ValueError(f"Unknown move {move}")
    return ''.join(programs)

def test_example():
    result = solve('s1,x3/4,pe/b', 'abcde')
    assert('baedc' == result)

PROGRAMS = 'abcdefghijklmnop'

def test_part1():
    result = solve(data(), PROGRAMS)
    print('PART 1:', result)
    assert('hmefajngplkidocb' == result)

def solve2(moves_txt, programs_txt, N=1000000000):
    # Check for cycle
    new_programs_txt = programs_txt
    for i in range(1,N):
        new_programs_txt = solve(moves_txt, new_programs_txt)        
        if new_programs_txt == programs_txt:
            break

    # found cycle
    new_programs_txt = programs_txt
    actual_moves = N % i # see how many actual moves are needed
    for i in range(actual_moves):
        new_programs_txt = solve(moves_txt, new_programs_txt)
    return new_programs_txt


def test_part2():
    result = solve2(data(), PROGRAMS)    
    print('PART 2:', result)
    assert('fbidepghmjklcnoa' == result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_part2()