"""
Advent of Code 2022 - Day 24
Pieter Kitslaar
"""
from pathlib import Path
THIS_DIR = Path(__file__).parent

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

EXAMPLE_SMALL="""\
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

EXAMPLE_DATA="""\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

DIRS={'>': (1,0), '<': (-1, 0), 'v': (0,1), '^': (0,-1)}

from collections import namedtuple
class Blizzard(namedtuple("Blizzard", "pos dir")):
    pass

class Valley:

    def __init__(self, valley, blizzards):
        self.valley = valley
        self.blizzards = blizzards
        self.W = max([p[0] for p in self.valley])
        self.H = max([p[1] for p in self.valley])
        self.filled_valley = self._fill_map()

    def _fill_map(self):
        W, H = self.W, self.H
        valley = self.valley

        map_d = valley.copy()
        for b in self.blizzards:
            b_pos = b.pos
            m_v = map_d[b_pos]
            if m_v == '.':
                map_d[b_pos] = b.dir
            elif isinstance(m_v, int):
                map_d[b_pos] += 1
            elif m_v in '><v^':
                map_d[b_pos] = 2
            else:
                raise ValueError(f"Invalid map value {m_v} for blizzard at {b_pos}") 
        return map_d

    def print_map(self):
        for y in range(self.H+1):
            for x in range(self.W+1):
                print(self.filled_valley[(x,y)], end='')
            print()
        print()

    def move_blizzards(self):
        W, H = self.W, self.H
        blizzards = self.blizzards
        valley = self.valley
        new_blizzards = []
        for b in blizzards:
            b_pos, b_dir = b.pos, b.dir
            d=DIRS[b_dir]
            new_pos = (b_pos[0]+d[0], b_pos[1]+d[1])
            if new_pos[0]<1:
                new_pos = (W-1, new_pos[1])
            elif new_pos[0]>=W:
                new_pos = (1, new_pos[1])
            elif new_pos[1]<1:
                new_pos = (new_pos[0], H-1)
            elif new_pos[1]>=H:
                new_pos = (new_pos[0], 1)
            assert(valley[new_pos]=='.')
            new_blizzards.append(Blizzard(pos=new_pos, dir=b_dir))
        return Valley( 
            valley=self.valley,
            blizzards=tuple(new_blizzards)
        )

    def is_valid_position(self, pos):
        if self.filled_valley.get(pos,'#') == '.':
            return True
        return False

    @staticmethod
    def parse(d):
        valley = {}
        blizzards = []
        for y, line in enumerate(d.strip().splitlines()):
            for x, v in enumerate(line):
                if v in '.#':
                    valley[(x,y)]=v
                elif v in  '><v^':
                    valley[(x,y)]='.'
                    blizzards.append(Blizzard(pos=(x,y), dir=v))
                else:
                    raise ValueError(f"Unknow value {v}")
        start_pos = None
        end_pos = None
        for p,v in valley.items():
            if v == '.':
                if not start_pos:
                    start_pos = p
                else:
                    end_pos = p

        initial_valley = Valley(
            valley = valley,
            blizzards = tuple(blizzards),
        )

        additional_info = dict(
            blizzard_cycle=math.lcm(*[initial_valley.W-1, initial_valley.H-1]),
            start_pos = start_pos,
            end_pos = end_pos,
        )


        return additional_info, initial_valley

class State(namedtuple("State", "minute current_pos end_pos")):

    def __lt__(self, other):
        return self.sort_key() < other.sort_key()

    def sort_key(self):
        d_end = self.dist_end()
        return (self.minute, d_end)

    def accept_key(self):
        return (self.current_pos, self.minute)

    def dist_end(self):
        return abs(self.current_pos[0]-self.end_pos[0])+abs(self.current_pos[1]-self.end_pos[1])

import heapq
import math

def solve(d, part2=False):
    info, initial_valley = Valley.parse(d)
    blizzard_cycle = info['blizzard_cycle']


    start_pos = info['start_pos']
    end_pos = info['end_pos']

    all_valleys = {}
    all_valleys[0] = initial_valley
    if not part2:
        return find_path(all_valleys, blizzard_cycle, State(0, info['start_pos'], end_pos), end_pos)
    else:
        prev_minute = 0
        for (start, end) in [(start_pos, end_pos), (end_pos, start_pos), (start_pos, end_pos)]:
            end_minute = find_path(all_valleys, blizzard_cycle, State(prev_minute, start, end), end)
            print(start, end, end_minute)
            prev_minute = end_minute
        return end_minute
        



def find_path(all_valleys, blizzard_cycle, initial_state, end_pos):
    states = [initial_state]
    num_evaluations = 0
    accepted = {}
    while states:
        num_evaluations += 1
        current_state = heapq.heappop(states)
        current_valley = all_valleys[current_state.minute % blizzard_cycle]

        if not current_state.accept_key() in accepted or current_state < accepted[current_state.accept_key()]:
            accepted[current_state.accept_key()] = current_state
            if num_evaluations % 100 == 0:
                print(len(states), current_state.sort_key())
            if current_state.current_pos == end_pos:
                print('FOUND exit', current_state.minute)
                return current_state.minute
        else:
            continue


        new_state = current_state._replace(minute=current_state.minute+1)
        try:
            new_valley = all_valleys[new_state.minute % blizzard_cycle]
        except KeyError:
            new_valley = current_valley.move_blizzards()
            all_valleys[new_state.minute % blizzard_cycle] = new_valley

        new_states = []
        if new_valley.is_valid_position(new_state.current_pos):
            # keep current position
            new_states.append(new_state)
            #heapq.heappush(states, new_state)
        for D in DIRS.values():
            c_pos = new_state.current_pos
            new_pos = (c_pos[0]+D[0], c_pos[1]+D[1])
            if new_valley.is_valid_position(new_pos):
                new_states.append(new_state._replace(current_pos=new_pos))
        
        for ns in new_states:
            if not ns.accept_key() in accepted:
                heapq.heappush(states, ns)


def test_example_small():
    result = solve(EXAMPLE_SMALL)
    assert(10 == result)

def test_example():
    result = solve(EXAMPLE_DATA)
    assert(18 == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)
    assert(288 == result)

def solve2(d):
    return solve(d, part2=True)

def test_example2():
    result = solve2(EXAMPLE_DATA)
    assert(54 == result)

def test_part2():
    result = solve2(data())
    print('PART 2:', result)
    assert(861 == result)


if __name__ == "__main__":
    test_example_small()
    test_example()
    test_part1()
    test_example2()
    test_part2()


