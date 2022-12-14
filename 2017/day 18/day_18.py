"""
Advent of Code 2017 - Day 18
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

def data():
    with open(THIS_DIR / 'input.txt') as f:
        return f.read().strip()

EXAMPLE_DATA = """\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

from collections import defaultdict, deque

class Runner:
    def __init__(self):
        self.send_buffer = deque()
        self.num_send = 0
        self.waiting = False

    def run_code(self, d, p=0, part2=False):
        registers = defaultdict(int)
        registers['p'] = p
        last_freq = None
        recover_freq = None
        instructions = list(d.strip().splitlines())
        #if part2:
        #    _ = yield ('init', None)
        current_index = 0
        while 0 <= current_index < len(instructions):
            op, reg, *arg = instructions[current_index].split()
            arg = arg[0] if arg else '0'
            v = registers[arg] if arg.isalpha() else int(arg)
            if op == 'set':
                registers[reg] = v
            elif op == 'add':
                registers[reg] += v
            elif op == 'mul':
                registers[reg] *= v
            elif op == 'mod':
                registers[reg] = registers[reg] % v
            elif op == 'snd':
                if part2:
                    v = registers[reg] if reg.isalpha() else int(reg)
                    self.send_buffer.append(v)
                    #print(f'{p} send {v:6} at instruction {current_index:2} a={registers["a"]},b={registers["b"]} (send queue size {len(self.send_buffer)})')
                    self.num_send += 1
                    #_ = yield ('snd', v)
                    #print(p, 'snd <-', _)
                    #send_queue.append(v)
                else:
                    last_freq = registers[reg]
            elif op == 'rcv':
                if part2:
                    r = yield
                    while r is None:
                        #print(p, 'waiting in rcv')
                        self.waiting = True
                        r = yield
                    self.waiting = False
                    registers[reg] = r
                    
                else:
                    if registers[reg] != 0:
                        recover_freq = yield last_freq
                        break
            elif op == 'jgz':
                c = registers[reg] if reg.isalpha() else int(reg)
                if c > 0:
                    current_index += v-1
            else:
                raise ValueError(f"Unkown operation {op}")
            current_index += 1
        return recover_freq

def test_example():
    runner = Runner()
    iter = runner.run_code(EXAMPLE_DATA)
    result = next(iter)
    assert(4 == result)

def test_part1():
    runner = Runner()
    iter = runner.run_code(data())
    result = next(iter)
    print('PART 1:', result)
    assert(7071 == result)

EXAMPLE_DATA2="""\
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

def solve2(d):
    p0 = Runner()
    p0_iter = p0.run_code(d, p=0, part2=True)
    next(p0_iter)

    p1 = Runner()
    p1_iter = p1.run_code(d, p=1, part2=True)
    next(p1_iter)

    while True:
        try:
            if p1.send_buffer:
                while p1.send_buffer:
                    p0_iter.send(p1.send_buffer.popleft())
            else:
                p0_iter.send(None)
            
            if p0.send_buffer:
                while p0.send_buffer:
                    p1_iter.send(p0.send_buffer.popleft())
            else:
                p1_iter.send(None)
            if p0.waiting and p1.waiting:
                break
        except StopIteration:
            break
    return p1.num_send

def test_example2():
    result = solve2(EXAMPLE_DATA2)
    assert(3 == result)

def test_part2():
    result = solve2(data())
    print('PART 2:', result)
    assert(8001 == result)
        


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()


        

