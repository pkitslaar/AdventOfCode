import re
group_names = ('id', 'x', 'y', 'w', 'h')
claim_re = re.compile('\#(\d+) \@ (\d+),(\d+): (\d+)x(\d+)')

claims = []
with open('input.txt', 'r') as f:
    for l in f:
        print(l)
        m = claim_re.match(l)
        m_d = dict(zip(group_names, m.groups()))
        claims.append(m_d)
