"""
Advent of Code 2017 - Day 20
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read()

EXAMPLE_DATA="""\
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""

import re

RE_COORDS = re.compile('(-?\d+),(-?\d+),(-?\d+)')

from collections import namedtuple

class Particle(namedtuple('Particle', "p v a")):
    def update(self):
        new_v = tuple(v+a for v,a in zip(self.v, self.a))        
        new_p = tuple(p+v for p,v in zip(self.p, self.v))
        return self._replace(p=new_p, v=new_v)
    
    def dist(self):
        return sum(abs(p) for p in self.p)
    


def to_coords(txt):
    if m:=RE_COORDS.search(txt):
        return [*map(int,m.groups())]

def solve(d):
    particles = []
    for i, line in enumerate(d.splitlines()):
        p,v,a = map(to_coords, line.split('>,'))
        particles.append((i,Particle(p,v,a)))

    particles.sort(key = lambda t: sum(abs(pi) for pi in t[1].a))
    print(particles[0])
    
    #for _ in range(5):
    #    particles.sort(key = lambda t: t[1].dist())
    #    print([(i,p.dist(), p) for i,p in particles])
    #    new_particles = []
    #    for i,p in particles:
    #        new_particles.append((i,p.update()))
    #    particles = new_particles
    #particles.sort(key = lambda t: t[1].dist())
    #return particles[0][0]


def test_example():
    result = solve(EXAMPLE_DATA)
    assert(0 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)

if __name__ == "__main__":
    #test_example()
    test_part1()
