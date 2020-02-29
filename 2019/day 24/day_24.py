from pathlib import Path

def read_map(txt):
    grid = []
    for l_raw in txt.splitlines():
        l = l_raw.strip()
        if l:
            grid.append(list(l))
    return grid

def map_to_txt(grid):
    return '\n'.join([''.join(r) for r in grid])

def get_adjacent_values(grid, g_down=None, g_up=None):
    height = len(grid)
    width = len(grid[0])
    adj_grid = [[0 for _x in range(width)] for _y in range(height)]
    for y in range(height):
        for x in range(width):
            adjacent = 0
            
            if y > 0 and grid[y-1][x] == '#':
                adjacent += 1
            if y + 1 < height and grid[y+1][x] == '#':
                adjacent += 1
            
            if x > 0 and grid[y][x-1] == '#':
                adjacent += 1
            if x + 1 < width and grid[y][x+1] == '#':
                adjacent += 1

            # check level above 
            if y == 0 and g_up and g_up[1][2] == '#':
                adjacent += 1
            if y +1 == height and g_up and g_up[3][2] == '#':
                adjacent += 1
            if x == 0 and g_up and g_up[2][1] == '#':
                adjacent += 1
            if x +1 == width and g_up and g_up[2][3] == '#':
                adjacent += 1
            
            # check level below
            if (1,2) == (y,x) and g_down: # tile 8 in example
                adjacent += sum([1 for _x in range(5) if g_down[0][_x] == '#'])
            if (3,2) == (y,x) and g_down: # tile 18 in example
                adjacent += sum([1 for _x in range(5) if g_down[4][_x] == '#'])
            if (2,1) == (y,x) and g_down: # tile 12 in example
                adjacent += sum([1 for _y in range(5) if g_down[_y][0] == '#'])
            if (2,3) == (y,x) and g_down: # tile 14 in example
                adjacent += sum([1 for _y in range(5) if g_down[_y][4] == '#'])
            adj_grid[y][x] = adjacent
    return adj_grid
            

def update(grid, adj_grid = None):
    height = len(grid)
    width = len(grid[0])
    if adj_grid is None:
        adj_grid = get_adjacent_values(grid)
    new_grid = [['.' for _x in range(width)] for _y in range(height)]
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '?':
                new_grid[y][x] = '?'
            else:
                if grid[y][x] == '#' and adj_grid[y][x] == 1:
                    new_grid[y][x] = '#'
                if grid[y][x] == '.' and adj_grid[y][x] in (1,2):
                    new_grid[y][x] = '#'
    return new_grid

initial_map = """\
....#
#..#.
#..##
..#..
#...."""

def test_simple_read():
    g = read_map(initial_map)
    assert(len(g) == 5)
    assert(g[0] == ['.', '.', '.', '.', '#'])
    assert(g[1] == ['#', '.', '.', '#', '.'])
    assert(g[2] == ['#', '.', '.', '#', '#'])
    assert(g[3] == ['.', '.', '#', '.', '.'])
    assert(g[4] == ['#', '.', '.', '.', '.'])

def test_adj_grid():
    g = read_map(initial_map)
    adj_grid = get_adjacent_values(g)
    assert(len(adj_grid) == len(g))
    assert(len(adj_grid[0]) == len(g[0]))
    assert(adj_grid[0] == [1, 0, 0, 2, 0])
    assert(adj_grid[1] == [1, 1, 1, 1, 3])
    assert(adj_grid[2] == [1, 1, 2, 2, 1])
    assert(adj_grid[3] == [2, 1, 0, 2, 1])
    assert(adj_grid[4] == [0, 1, 1, 0, 0])

def test_map_to_txt():
    g = read_map(initial_map)
    txt = map_to_txt(g)
    assert(initial_map == txt)

after_1_minute = """\
#..#.
####.
###.#
##.##
.##.."""

after_2_minutes = """\
#####
....#
....#
...#.
#.###"""

after_3_minutes = """\
#....
####.
...##
#.##.
.##.#"""

after_4_minutes = """\
####.
....#
##..#
.....
##..."""
def test_update():
    g0 = read_map(initial_map)
    g1 = update(g0)
    assert(after_1_minute == map_to_txt(g1))
    g2 = update(g1)
    assert(after_2_minutes == map_to_txt(g2))
    g3 = update(g2)
    assert(after_3_minutes == map_to_txt(g3))
    g4 = update(g3)
    assert(after_4_minutes == map_to_txt(g4))

def find_duplicate_layout(init_txt):
    prev_grid = read_map(init_txt)
    layouts = set([init_txt.strip()])
    while True:
        new_grid = update(prev_grid)
        new_layout = map_to_txt(new_grid)
        if new_layout in layouts:
            print('Found dupliate')
            return new_grid
        layouts.add(new_layout)
        prev_grid = new_grid

initial_duplicate = """\
.....
.....
.....
#....
.#..."""

def test_duplicate():
    duplicate = find_duplicate_layout(initial_map)
    assert(initial_duplicate == map_to_txt(duplicate))

def compute_rating(grid):
    rating = 0
    cell_index = 0
    for row in grid:
        for cell in row:
            if cell == '#':
                rating += pow(2, cell_index)
            cell_index += 1
    return rating

def test_rating():
    dup_grid = read_map(initial_duplicate)
    dup_rating = compute_rating(dup_grid)
    assert(2129920 == dup_rating)

with open(Path(__file__).parent / 'input.txt', 'r') as f:
    puzzle_input = f.read().strip()

def part1():
    duplicate = find_duplicate_layout(puzzle_input)
    rating = compute_rating(duplicate)
    print('Part 1', rating)
    assert(13500447 == rating)

def filled_grid(fill_value='#'):
    g = [[fill_value for _x in range(5)] for _y in range(5)]
    g[2][2] = '?'
    return g

initial_map_multi = """\
....#
#..#.
#.?##
..#..
#...."""


def test_adj_multi_level():
    level0 = read_map(initial_map_multi)
    level_up = filled_grid('.')
    level_down = filled_grid('.')

    adj_grid_0 = get_adjacent_values(level0, level_down, level_up)
    expected_adj_grid_0 = [
        [1, 0, 0, 2, 0],
        [1, 1, 1, 1, 3],
        [1, 1, 2, 2, 1],
        [2, 1, 0, 2, 1],
        [0, 1, 1, 0, 0],
    ]
    assert(adj_grid_0 == expected_adj_grid_0)

    adj_grid_up = get_adjacent_values(level_up, level0, None)
    expected_adj_grid_up = [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 3, 0, 2, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    assert(adj_grid_up == expected_adj_grid_up)

    adj_grid_down = get_adjacent_values(level_down, None, level0)
    expected_adj_grid_down = [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 1, 1, 1, 2],
    ]
    assert(adj_grid_down == expected_adj_grid_down)


def update_multi_level(initial_grid, num_minutes):
    levels = [{0: initial_grid, -1: filled_grid('.'), 1: filled_grid('.')}]
    for minute in range(num_minutes):
        this_levels = levels[-1]
        print(minute)
        # compute adjacents
        adjacent = {}
        for level in this_levels:
            adj_level = get_adjacent_values(this_levels[level], this_levels.get(level+1), this_levels.get(level-1))
            adjacent[level] = adj_level
        
        # update
        new_levels = {}
        for level in this_levels:
            new_level = update(this_levels[level], adjacent[level])
            new_levels[level] = new_level

        # add new empty levels above and below existing
        min_level = min(new_levels)
        max_level = max(new_levels)
        new_levels[min_level-1] = filled_grid('.')
        new_levels[max_level+1] = filled_grid('.')
        levels.append(new_levels)
    return levels
        

level_0_10 = """\
.#...
.#.##
.#?..
.....
....."""

level_5d_10 = """\
..#..
.#.#.
..?.#
.#.#.
..#.."""

level_5u_10 = """\
####.
#..#.
#.?#.
####.
....."""

def test_update_multi_level():
    g = read_map(initial_map_multi)
    assert(initial_map_multi == map_to_txt(g))
    levels = update_multi_level(g, 10)
 
    expected_level_0_10 = read_map(level_0_10)
    assert(expected_level_0_10 == levels[10][0])

    expected_level_5d_10 = read_map(level_5d_10)
    assert(expected_level_5d_10 == levels[10][-5])
    
    expected_level_5u_10 = read_map(level_5u_10)
    assert(expected_level_5u_10 == levels[10][5])

    dephts = levels[10]
    total_bugs = count_bugs(dephts)
    assert(99 == total_bugs)

def count_bugs(dephts):
    total_bugs = 0
    for depth, grid in dephts.items():
        for row in grid:
            for c in row:
                if c=='#':
                    total_bugs += 1
    return total_bugs
    

def part2():
    g = read_map(puzzle_input)
    g[2][2]='?'
    num_minutes = 200
    levels = update_multi_level(g, num_minutes)
    answer = count_bugs(levels[num_minutes])
    print('Part 2', answer)
    asset(2120 == answer)




if __name__ == "__main__":
    part1()
    part2()
