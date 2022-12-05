"""
Advent of Code 2017 - Day 13
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

from collections import deque

EXAMPLE_DATA = """\
0: 3
1: 2
4: 4
6: 4
"""

class Scanner:
    def __init__(self, scan_range):
        self.scan_range = scan_range
        self.pos = deque([0]*self.scan_range)
        self.pos[0] = 1
        self.direction = 1

    def step(self):
        self.pos.rotate(self.direction)
        if self.pos[-1] == 1 or self.pos[0] == 1:
            # scanner at the end so reverse direction
            self.direction *= -1
    
    def at_top(self):
        return self.pos[0] == 1



def parse(d):
    firewall = {}
    for line in d.strip().splitlines():
        depth, scan_range = map(int, line.split(': '))
        firewall[depth] = Scanner(scan_range)
    return firewall


def solve(d):
    firewall = parse(d)
    max_pos = max(firewall)+1
    pos = -1
    severity = 0
    while pos < max_pos:
        pos += 1
        # check if we are caught
        try:
            scanner = firewall[pos]
            if scanner.at_top():
                # caught
                print(f'caught at {pos}')
                severity += pos*len(scanner.pos)
        except KeyError:
            pass
        for s in firewall.values():
            s.step()
    return severity


def test_example():
    assert(24 == solve(EXAMPLE_DATA))

def test_part1():
    result = solve(data())
    print('PART 1:', result)

def solve2(d):
    firewall = parse(d)
    # check for each scanner when we get cauth
    # - a scanner at depth 0 with range 3 is at position 0 at
    #   t=0,4,8,12,etc..
    # - given a delay T the moments the scanner at depth 0 catches the packet
    #   are when T % ((2*3) -2) == 0
    # - given a scanner at depth 1 with range 4 it will catch a packet starting at delay T
    #   at the time points (T+1) % ((2*4) -2) == 0
    caught = True
    T = -1
    while caught:
        caught = False
        T += 1
        for d,s in firewall.items():
            if ((T+d) % ((2*s.scan_range)-2)) == 0:
                # caught
                caught = True
                break
    return T

def test_example2():
    assert(10 == solve2(EXAMPLE_DATA))

def test_part2():
    result = solve2(data())
    print('PART 2:', result)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()
