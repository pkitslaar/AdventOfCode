from pathlib import Path
import networkx as nx
from matplotlib import pyplot as plt
import heapq

example = """\
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z  
"""

INNER, OUTER = ('INNER', 'OUTER')

def parse_map(map_txt, add_portal_edges=True):
    grid = {}
    graph = nx.Graph()
    portal_coord_to_name = {}
    portal_coord_to_type = {}
    portal_name_to_coords = {}
    for y, row in enumerate(map_txt.splitlines()):
        for x, c in enumerate(row):
            grid[(x,y)] = c
    
    wall_coords = [p for p,v in grid.items() if v == '#']
    wall_x_coords = [p[0] for p in wall_coords]
    wall_min_x, wall_max_x = min(wall_x_coords), max(wall_x_coords)
    wall_y_coords = [p[1] for p in wall_coords]
    wall_min_y, wall_max_y = min(wall_y_coords), max(wall_y_coords)
    for (x,y),c in grid.items():
            if c == '.':
                if grid.get((x-1,y)) == '.':
                    graph.add_edge((x,y), (x-1,y))
                if grid.get((x,y-1)) == '.':
                    graph.add_edge((x,y), (x,y-1))
                for pa,pb,p_type in [
                        ((x-2,y),(x-1,y), OUTER if x-1 < wall_min_x else INNER), # left neighbor
                        ((x+1,y),(x+2,y), OUTER if x+1 > wall_max_x else INNER), # right neighbor
                        ((x,y-2),(x,y-1), OUTER if y-1 < wall_min_y else INNER), # lower neighbor
                        ((x,y+1),(x,y+2), OUTER if y+1 > wall_max_y else INNER), # upper neighbor
                        ]:
                    if grid.get(pa,'').isupper() and grid.get(pb,'').isupper():
                        name = grid[pa] + grid[pb]
                        portal_coord_to_name[(x,y)] = name
                        portal_coord_to_type[(x,y)] = p_type
                        portal_name_to_coords.setdefault(name, []).append((x,y))
                        #graph.add_node(pa, name=name)
                        #graph.add_edge(pa, (x,y))
    if add_portal_edges:
        for pn, coords in portal_name_to_coords.items():
            assert(len(coords) < 3)
            if len(coords) == 2:
                graph.add_edge(coords[0], coords[1], edge_type='portal')
        
    #nx.draw(graph, labels=portal_coord_to_type, with_show_labels=True, pos={n:(n[0],-n[1]) for n in graph.nodes()})
    #plt.show()
    return graph, portal_name_to_coords, portal_coord_to_name, portal_coord_to_type

def test_example():
    g, portal_names, _ ,_ = parse_map(example)
    p = nx.shortest_path(g, portal_names['AA'][0], portal_names['ZZ'][0] )[1:]
    len_path = len(p)
    assert(23 == len_path)


larger_example="""\
                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P  
"""

def test_larger_example():
    g, portal_names, _, _ = parse_map(larger_example)
    p = nx.shortest_path(g, portal_names['AA'][0], portal_names['ZZ'][0] )[1:]
    len_path = len(p)
    assert(58 == len_path)

example_part_2 = """\
             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                   """


def solve_recursive(g, portal_name_to_coords, portal_coord_to_name, portal_coord_to_type):
    p2p = {}
    for pc in portal_coord_to_type:
        all_target_distance = nx.single_source_dijkstra(g, pc)[0]
        p2p[pc] = {t:d for t,d in all_target_distance.items() if t != pc and t in portal_coord_to_type}
    
    
    #
    start_coord = portal_name_to_coords['AA'][0] 
    final_coord = portal_name_to_coords['ZZ'][0]

    STEPS, LEVEL, COORD, NAME, TYPE = range(5)
    front = [(0, 0, portal_name_to_coords['AA'][0], 'AA', OUTER)]
    heapq.heapify(front)
    fastest = {}
    while front:
        current = heapq.heappop(front)
        current_key = (current[LEVEL], current[COORD])
        best_time = fastest.get(current_key)
        if best_time is None or best_time > current[STEPS]:
            fastest[current_key] = current[STEPS]
        else:
            continue

        if current[LEVEL] == 0 and current[COORD] == final_coord:
            return current[STEPS]
        candidate_targets = []

        # move within the same level
        for t, d in p2p[current[COORD]].items():
            t_type = portal_coord_to_type[t]
            t_name = portal_coord_to_name[t]
            if current[LEVEL] == 0:
                if t_type == INNER or t_name in ('AA', 'ZZ'):
                    candidate_targets.append((current[STEPS]+d, current[LEVEL], t, t_name, t_type))
            else:
                if t_name not in ('AA', 'ZZ'):
                    candidate_targets.append((current[STEPS]+d, current[LEVEL], t, t_name, t_type))
        
        if current[TYPE] == OUTER and current[LEVEL] > 0:
            # move to upper level
            other_side = [t for t in portal_name_to_coords[current[NAME]] if t != current[COORD]][0]
            candidate_targets.append((current[STEPS]+1, current[LEVEL]-1, other_side, portal_coord_to_name[other_side], portal_coord_to_type[other_side]))
        elif current[TYPE] == INNER:
            # move to lower level
            other_side = [t for t in portal_name_to_coords[current[NAME]] if t != current[COORD]][0]
            candidate_targets.append((current[STEPS]+1, current[LEVEL]+1, other_side, portal_coord_to_name[other_side], portal_coord_to_type[other_side]))
        
        for ct in candidate_targets:
            ct_key = (ct[LEVEL], ct[COORD])
            ct_time = fastest.get(ct_key)
            if ct_time is None or ct_time > ct[STEPS]:
                heapq.heappush(front, ct)

def test_example_part2():
    sol = solve_recursive(*parse_map(example_part_2, add_portal_edges=False))
    print(sol)

def main():
    with open(Path(__file__).parent / 'input.txt', 'r') as f:
        main_map= f.read()
    g, portal_names, _, _ = parse_map(main_map)
    p = nx.shortest_path(g, portal_names['AA'][0], portal_names['ZZ'][0] )[1:]
    len_path = len(p)
    print('Part 1:', len_path)
    assert(464 == len_path)

    sol = solve_recursive(*parse_map(main_map, add_portal_edges=False))
    print('Part 2:', sol)
    assert(5802 == sol)

if __name__ == "__main__":
    main()


