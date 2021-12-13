"""
Advent of Code 2021 - Day 13
Pieter Kitslaar
"""

from pathlib import Path

example="""\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

FOLD = 'fold along '

def parse(txt):
    paper={}
    folds = []
    for line in txt.splitlines():
        l_strip = line.strip()
        if l_strip:
            if l_strip.startswith(FOLD):
                folds.append(l_strip[len(FOLD):])
            else:
                x,y = map(int,l_strip.split(','))
                paper[(x,y)]=1
    return paper, folds

def fold_paper(paper, fold):
    fold_dir, fold_line = fold.split('=')
    d = {'x':0,'y':1}[fold_dir]
    fold_line = int(fold_line)
    new_p = {}
    for pos in paper:
        fold_p = None
        if pos[d] < fold_line:
            fold_p = pos
        elif pos[d] > fold_line:
            fold_p = list(pos)
            fold_p[d] = fold_line-(pos[d]-fold_line)
            fold_p = tuple(fold_p)
        if fold_p:
            new_p[fold_p] = new_p.get(fold_p,0) + paper[pos]
    return new_p

def plot(paper):
    max_x = max(p[0] for p in paper)
    max_y = max(p[1] for p in paper)
    for y in range(max_y+1):
        for x in range(max_x+1):
            print('.#'[paper.get((x,y),0) > 0],end='')
        print()

def test_example():
    paper, folds = parse(example)
    new_p = fold_paper(paper, folds[0])
    assert 17 == len(new_p)
    new_p = fold_paper(new_p, folds[1])
    assert 16 == len(new_p)

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

def test_part1():
    paper, folds = parse(get_input())
    new_p = fold_paper(paper, folds[0])
    result = len(new_p)
    print('Part 1', result)

def test_part2():
    paper, folds = parse(get_input())
    for f in folds:
        paper = fold_paper(paper, f)
    print('Part 2:')
    plot(paper)

if __name__ == "__main__":
    test_example()
    test_part1()
    test_part2()