"""
Advent of Code 2022 - Day 11
Pieter Kitslaar
"""

from pathlib import Path
THIS_DIR = Path(__file__).parent

import math

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

EXAMPLE_DATA="""\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


from itertools import count
def parse(d):
    monkeys = []
    current_monkey = None
    item_id = count()
    for line in d.strip().splitlines():
        if line.startswith('Monkey '):
            monkeys.append({'id': len(monkeys), 'num_inspected':0})
            current_monkey = monkeys[-1]
        elif 'Starting items:' in line:
            current_monkey['items'] = [(next(item_id),v) for v in [int(v.strip()) for v in line.split(':')[-1].split(',')]]
        elif 'Operation:' in line:
            operation_text = line.split(':')[-1].split('=')[-1].strip()
            op_func = eval(f'lambda old: {operation_text}')
            current_monkey['operation'] = op_func
        elif 'Test:' in line:
            assert('divisible by' in line)
            current_monkey['test'] = int(line.split()[-1])
        elif 'If true:' in line:
            current_monkey['test_true'] = int(line.split()[-1])
        elif 'If false:' in line:
            current_monkey['test_false'] = int(line.split()[-1])
    return monkeys

def solve(monkeys, n_rounds = 20, part2=False):
    if part2:
        # This is the clue to solve part 2
        # I had to get some hints from a post on Reddit.
        #
        # To limit the numbers from exploding while keeping
        # all the division checks valid, we can get the modulo
        # of any new value with the  Common Multiple (cm)
        # of all the division check values.
        # 
        cm = math.prod([m['test'] for m in monkeys])

    for _ in range(n_rounds):
        for m in monkeys:
            for item_id, item_value in m['items']:
                new_value = m['operation'](item_value)
                if not part2:
                    new_value = new_value // 3
                else:
                    new_value = new_value % cm
                m['num_inspected'] += 1
                if new_value % m['test'] == 0:
                    next_m = monkeys[m['test_true']]
                else:
                    next_m = monkeys[m['test_false']]
                next_m['items'].append((item_id,new_value))
            m['items'] = []
   
    monkeys.sort(key = lambda m: m['num_inspected'], reverse=True)
    return monkeys[0]['num_inspected'] * monkeys[1]['num_inspected']

def test_example():
    result = solve(parse(EXAMPLE_DATA))
    assert(101*105 == result)

def test_part1():
    result = solve(parse(data()))
    print('PART 1:', result)
    assert(120756 == result)

def solve2(d):
    monkeys = parse(d)
    N = 10_000
    result = solve(monkeys, n_rounds=N, part2=True)
    return result

def test_example2():
    result = solve2(EXAMPLE_DATA)
    assert(2713310158 == result)

def test_part2():
    result = solve2(data())
    print('PART 2:', result)
    assert(39109444654 == result)


if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()