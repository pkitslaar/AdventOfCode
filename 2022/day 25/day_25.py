"""
Advent of Code 2022 - Day 25
Pieter Kitslaar
"""
from pathlib import Path
THIS_DIR = Path(__file__).parent

def data(fn='input.txt'):
    with open(THIS_DIR / fn) as f:
        return f.read()

TEST_TABLE = """\
  Decimal          SNAFU
        1              1
        2              2
        3             1=
        4             1-
        5             10
        6             11
        7             12
        8             2=
        9             2-
       10             20
       15            1=0
       20            1-0
     2022         1=11-2
    12345        1-0---0
314159265  1121-1110-1=0"""



P5 = [5**i for i in range(100)]
S_TO_D = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
D_TO_S = {v:k for k,v in S_TO_D.items()}

def snafu_to_decimal(snafu):
    result = 0
    for i, s in enumerate(reversed(snafu)):
        result += S_TO_D[s]*P5[i]
    return result

def decimal_to_snafu(decimal):
    remaining = decimal
    # find highest s number
    for i,v in enumerate(P5):
        if v > remaining:
            break
    else:
        # no break
        raise ValueError(f"No P5 value is bigger than {decimal} current highest is {P5[-1]}")
    assert(i > 0)
    current_i = i-1 # take one below

    num_s = []
    for i in range(current_i,-1,-1):
        num = remaining//P5[i]
        num_s.append(num)
        remaining = remaining % P5[i]

    correc_num_s = [*(s for s in reversed(num_s))]
    for i, s in enumerate(correc_num_s):
        if s > 2:
            correc_num_s[i] = s - 5
            if (i+1) == len(correc_num_s):
                correc_num_s.append(0)
            correc_num_s[i+1] += 1
            
    result = ''.join(D_TO_S[ns] for ns in reversed(correc_num_s))
    return result


def example_table():
    for line in TEST_TABLE.splitlines()[1:]:
        d, s = map(str.strip, line.strip().split())
        yield int(d), s

def test_snafu_to_decimal():
    for d, s in example_table():
        assert(d == snafu_to_decimal(s))

def test_decimal_to_snafu():
    for d, s in example_table():
        assert(s == decimal_to_snafu(d))

EXAMPLE_DATA = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

def solve(d):
    total = 0
    for s in d.splitlines():
        total += snafu_to_decimal(s)
    return decimal_to_snafu(total)

def test_example():
    result = solve(EXAMPLE_DATA)
    assert('2=-1=0' == result)

def test_part1():
    result = solve(data())
    print('PART 1:', result)

if __name__ == "__main__":
    test_snafu_to_decimal()
    test_decimal_to_snafu()
    test_example()
    test_part1()