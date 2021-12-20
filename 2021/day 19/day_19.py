"""
Advent of Code 2021 - Day 19
Pieter Kitslaar
"""

from pathlib import Path

def get_input():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        return f.read()

import numpy as np

A = [*map(np.array, [
 [[1, 0, 0],
  [0, 1, 0],
  [0, 0, 1]],

 [[0, 1, 0],
  [0, 0, 1],
  [1, 0, 0]],

 [[0, 0, 1],
  [1, 0, 0],
  [0, 1, 0]]
])]

B = [*map(np.array,[
 [[ 1, 0, 0],
  [ 0, 1, 0],
  [ 0, 0, 1]],

 [[-1, 0, 0],
  [ 0,-1, 0],
  [ 0, 0, 1]],

 [[-1, 0, 0],
  [ 0, 1, 0],
  [ 0, 0,-1]],

 [[ 1, 0, 0],
  [ 0,-1, 0],
  [ 0, 0,-1]]
])]

C = [*map(np.array,[
 [[ 1, 0, 0],
  [ 0, 1, 0],
  [ 0, 0, 1]],

 [[ 0, 0,-1],
  [ 0,-1, 0],
  [-1, 0, 0]]
])]

import itertools

I3=np.eye(3,dtype=np.int)
I2=np.eye(2,dtype=np.int)
orientation_matrices = [a@b@c for a,b,c in itertools.product(A,B,C)]

example_orientations="""\
--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 0 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 0 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 0 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8"""

def parse(txt):
    beacons_per_scnanner = []
    current_scanner = None
    for line in txt.splitlines():
        l_strip = line.strip()
        if not l_strip:
            continue
        if l_strip.startswith('---'):
            name = line[3:-3]
            current_scanner = []
            beacons_per_scnanner.append(current_scanner)
        else:
            current_scanner.append(np.array([*map(int,l_strip.split(','))]))
    return beacons_per_scnanner

def test_find_rotation():
    scanners = parse(example_orientations)
    base_beaons = {tuple(b) for b in scanners[0]}
    for scanner, beacons in enumerate(scanners[1:]):
        found_rotation = False
        for m in orientation_matrices:
            rotated_beacons = {tuple(b@m) for b in beacons}
            if base_beaons == rotated_beacons:
                found_rotation = True
                break
        assert found_rotation
            
example_2d="""\
--- scanner 0 ---
0,2
4,1
3,3

--- scanner 1 ---
-1,-1
-5,0
-2,1"""

example_large="""\
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

example_large_s0_s1 = """\
-618,-824,-621
-537,-823,-458
-447,-329,318
404,-588,-901
544,-627,-890
528,-643,409
-661,-816,-575
390,-675,-793
423,-701,434
-345,-311,381
459,-707,401
-485,-357,347"""

example_large_s1_s4 = """\
459,-707,401
-739,-1745,668
-485,-357,347
432,-2009,850
528,-643,409
423,-701,434
-345,-311,381
408,-1815,803
534,-1912,768
-687,-1600,576
-447,-329,318
-635,-1737,486"""


def beacon_center_permutations(beacons):
    for b_center in beacons:
        yield b_center, {tuple(b-b_center) for b in beacons}

def test_find_matches():
    scanner_beacons = parse(example_2d)
    b1, b2, m, common = find_matches(scanner_beacons[0], scanner_beacons[1], [I2], 3)
    assert tuple(b1) == (0,2)
    assert tuple(b2) == (-5,0)

def extended_bb(beacons):
    b_a = [tuple(b) for b in beacons]
    bb_a = np.array(min(b_a)), np.array(max(b_a))
    extended_bb_a = bb_a[0]-bb_a[1], bb_a[1]-bb_a[0]
    return extended_bb_a

def find_matches(beacons_a, beacons_b, matrices=orientation_matrices, N=12):
    for b1_center, b1_set in beacon_center_permutations(beacons_a):
        for m in matrices:
            b2_rot = [b@m for b in beacons_b]
            for b2_rot_center, b2_rot_set in beacon_center_permutations(b2_rot):
                common = b2_rot_set.intersection(b1_set) 
                if len(common) == N:
                    return (b1_center, b2_rot_center, b2_rot, common)

def parse_positions(txt):
    positions = []
    for line in txt.splitlines():
        positions.append(tuple(map(int,line.split(','))))
    return positions


def test_example():
    scanners = parse(example_large)
    s0_center, s1_rot_center, s1_rot, s0_s1_common = find_matches(scanners[0], scanners[1])
    s0_s1_common = {tuple(np.array(c)+s0_center) for c in s0_s1_common}
    s0_s1_common_expected = set(parse_positions(example_large_s0_s1))
    assert s0_s1_common == s0_s1_common_expected
    s1_pos = tuple(s0_center-s1_rot_center)
    assert s1_pos == (68,-1246,-43)
    s1_rel_s0 = [s+np.array(s1_pos) for s in s1_rot]

    s1_center, s4_rot_center, s4_rot, s1_s4_common = find_matches(s1_rel_s0, scanners[4])
    s4_pos = tuple(s1_center-s4_rot_center)
    assert s4_pos == (-20,-1133,1061)
    s1_s4_common = {tuple(np.array(c)+s1_center) for c in s1_s4_common}
    s1_s4_common_expected = set(parse_positions(example_large_s1_s4))
    assert s1_s4_common == s1_s4_common_expected
   

def solve1(scanners):
    num_scanners = len(scanners)
    matched_to_0 = {0}
    to_check = [0]
    all_beacons=set()
    while to_check:
        i = to_check.pop()
        all_beacons.update(tuple(p) for p in scanners[i])
        for j in range(num_scanners):
            if j in matched_to_0:
                continue
            m = find_matches(scanners[i], scanners[j])
            if m:
                i_center, j_rot_center, j_rot, i_j_common = m
                i_j_common = {tuple(np.array(c)+i_center) for c in i_j_common}
                all_beacons = all_beacons.union(i_j_common)
                j_pos = tuple(i_center-j_rot_center)
                print(j, j_pos)
                j_rel_i = [s+np.array(j_pos) for s in j_rot]
                scanners[j] = j_rel_i
                matched_to_0.add(j)
                to_check.append(j)
            #print(i,j, len(scanners), bool(m))

    return len(all_beacons)

def test_solve1():
    scanners = parse(example_large)
    result = solve1(scanners)
    assert 79 == result

def test_part1():
    print('Computing Part 1')
    scanners = parse(get_input())
    result = solve1(scanners)
    print('Part 1', result)
    assert 342 == result

part1_results="""\
0 (0, 0, 0)
5 (-1224, 129, -75)
1 (-1195, 1306, -26)
15 (-1315, -1101, -76)
8 (-1301, 1160, 1257)
24 (-2467, 1223, -47)
26 (-1215, 2542, 31)
6 (-1187, 2418, 1161)
7 (-1342, 2346, -1176)
17 (-71, 2457, -92)
18 (-1244, 3647, -74)
3 (-1273, 3668, -1161)
28 (-2547, 3702, -53)
4 (-3757, 3636, 29)
16 (-2495, 3697, -1224)
21 (-2538, 3721, 1107)
23 (-3754, 3674, -1246)
9 (-3688, 2399, -1283)
12 (-4961, 3567, -1140)
11 (-4878, 3698, -105)
25 (-4854, 2399, -1178)
27 (-3587, 2513, -104)
14 (-3684, 1322, 75)
13 (-85, 2423, -1263)
20 (1120, 2436, -1288)
10 (-1270, 2426, 2430)
2 (-1290, 2405, 3588)
22 (-2452, 1184, -1288)
19 (-2371, 1314, -2479)"""

example1_results="""\
0 (0, 0, 0)
1 (68, -1246, -43)
3 (-92, -2380, -20)
4 (-20, -1133, 1061)
2 (1105, -1205, 1229)"""

def solve2(txt):
    positions = []
    for line in txt.splitlines():
        pos_txt = line.split(' ',1)[-1]
        positions.append(tuple(map(int, pos_txt.strip()[1:-1].split(','))))
    num_pos = len(positions)
    distances = []
    for i in range(num_pos):
        p_i = positions[i]
        for j in range(i,num_pos):
            p_j = positions[j]
            dist = sum(abs(p_i[k]-p_j[k]) for k in range(len(p_i)))
            distances.append(dist)
    return max(distances)

def test_solve2():
    result = solve2(example1_results)
    print(result)

def test_part2():
    result = solve2(part1_results)
    print('Part 2', result)
    

if __name__ == "__main__":
    #test_find_rotation()
    test_find_matches()
    test_example()
    test_solve1()
    test_part1()
    test_solve2()
    test_part2()

