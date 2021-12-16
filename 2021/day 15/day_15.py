"""
Advent of Code 2021 - Day 15
Pieter Kitslaar
"""

from pathlib import Path
import networkx


def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

example="""\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

def parse(txt):
    grid = {}
    for y, row in enumerate(txt.splitlines()):
        for x, risk in enumerate(row):
            grid[(y,x)]=int(risk)
    return grid

def grid_to_graph(grid):
    g=networkx.DiGraph()
    for y,x in grid:
        for n in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny = y+n[0]
            nx = x+n[1]
            try:
                n_risk = grid[(ny,nx)]
                g.add_edge((y,x),(ny,nx), risk=n_risk)
            except KeyError:
                pass
    return g

def plot(grid):
    end_pos = max(grid)
    for y in range(end_pos[0]+1):
        for x in range(end_pos[1]+1):
            p = (y,x)
            print(grid[(y,x)],end='')
        print()

def solve(grid):
    g = grid_to_graph(grid)
    min_path = networkx.dijkstra_path(g,source=(0,0),target=max(grid), weight='risk')
    
    total_risk = sum(grid[p] for p in min_path[1:])
    return total_risk

def test_example():
    grid = parse(example)
    result = solve(grid)
    assert 40 == result

def test_part1():
    grid = parse(get_input())
    result = solve(grid)
    print('Part 1:', result)
    361 == result

def expand_grid(grid):
    max_pos = max(grid)
    new_grid = grid.copy()
    for (y,x), base_risk in grid.items():
        sub_grid = {(0,0): base_risk}
        for expand_Y in range(0,5):
            for expand_X in range(0,5):
                if (0,0) != (expand_Y, expand_X):
                    neighbor_risks = [
                        sub_grid.get((expand_Y-1, expand_X),0), 
                        sub_grid.get((expand_Y, expand_X-1),0)
                    ]
                    new_risk = max(neighbor_risks)+1
                    sub_grid[(expand_Y, expand_X)] = new_risk if new_risk < 10 else 1
        for (sub_y, sub_x), risk in sub_grid.items():
            full_y = y+sub_y*(max_pos[1]+1)
            full_x = x+sub_x*(max_pos[0]+1)
            new_grid[(full_y, full_x)] = risk
    return new_grid

expected_expanded="""\
11637517422274862853338597396444961841755517295286
13813736722492484783351359589446246169155735727126
21365113283247622439435873354154698446526571955763
36949315694715142671582625378269373648937148475914
74634171118574528222968563933317967414442817852555
13191281372421239248353234135946434524615754563572
13599124212461123532357223464346833457545794456865
31254216394236532741534764385264587549637569865174
12931385212314249632342535174345364628545647573965
23119445813422155692453326671356443778246755488935
22748628533385973964449618417555172952866628316397
24924847833513595894462461691557357271266846838237
32476224394358733541546984465265719557637682166874
47151426715826253782693736489371484759148259586125
85745282229685639333179674144428178525553928963666
24212392483532341359464345246157545635726865674683
24611235323572234643468334575457944568656815567976
42365327415347643852645875496375698651748671976285
23142496323425351743453646285456475739656758684176
34221556924533266713564437782467554889357866599146
33859739644496184175551729528666283163977739427418
35135958944624616915573572712668468382377957949348
43587335415469844652657195576376821668748793277985
58262537826937364893714847591482595861259361697236
96856393331796741444281785255539289636664139174777
35323413594643452461575456357268656746837976785794
35722346434683345754579445686568155679767926678187
53476438526458754963756986517486719762859782187396
34253517434536462854564757396567586841767869795287
45332667135644377824675548893578665991468977611257
44961841755517295286662831639777394274188841538529
46246169155735727126684683823779579493488168151459
54698446526571955763768216687487932779859814388196
69373648937148475914825958612593616972361472718347
17967414442817852555392896366641391747775241285888
46434524615754563572686567468379767857948187896815
46833457545794456865681556797679266781878137789298
64587549637569865174867197628597821873961893298417
45364628545647573965675868417678697952878971816398
56443778246755488935786659914689776112579188722368
55172952866628316397773942741888415385299952649631
57357271266846838237795794934881681514599279262561
65719557637682166874879327798598143881961925499217
71484759148259586125936169723614727183472583829458
28178525553928963666413917477752412858886352396999
57545635726865674683797678579481878968159298917926
57944568656815567976792667818781377892989248891319
75698651748671976285978218739618932984172914319528
56475739656758684176786979528789718163989182927419
67554889357866599146897761125791887223681299833479"""

def test_example2():
    grid = parse(example)
    new_grid = expand_grid(grid)
    expected_grid = parse(expected_expanded)
    assert new_grid == expected_grid
    result = solve(new_grid)
    assert 315 == result

def test_part2():
    grid = parse(get_input())
    new_grid = expand_grid(grid)
    result = solve(new_grid)
    print('Part 2:', result)
    assert 2838 == result

if __name__ == "__main__":
    test_example()
    test_part1()
    test_example2()
    test_part2()
