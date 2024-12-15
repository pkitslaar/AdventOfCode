"""
Advent of Code 2024 - Day 15
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

EXAMPLE_DATA_SMALL = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

def parse(data):
    lines = data.strip().splitlines()
    grid_lines = []
    move_lines = []
    in_grid = True
    for line in lines:
        if not line.strip():
            in_grid = False
            continue
        if in_grid:
            grid_lines.append(line)
        else:
            move_lines.append(line)
    
    grid = {}
    robot = None
    for y, line in enumerate(grid_lines):
        for x, c in enumerate(line):
            if c == "@":
                robot = (x,y)
                c = '.' # mark as free space
            grid[x,y] = c
    moves = []
    for line in move_lines:
        moves.extend([*line])
    return grid, robot, moves

def print_grid(grid, robot):
    g = grid.copy()
    g[robot] = "@"
    max_x = max(x for x,y in g)
    max_y = max(y for x,y in g)
    print()
    for y in range(max_y+1):
        for x in range(max_x+1):
            print(g[(x,y)], end="")
        print()

dXY = {'>': (1,0), '<': (-1,0), 'v': (0,1), '^': (0,-1)}

BBOX_OTHER = {'[': ']', ']': '['}

def push_big_box_vertical(grid, c_pos, dxy, may_push=False):
    """
    Function to push a box that spans two columns vertically
    
    This function gets invoked when the robot is trying to push a box vertical.
    c_pos initially is the position of the robot, dxy is the direction of the push.
    The functionally will recursively push boxes until it hits a wall or a free space.

    The function can first be used to test if the push would be successful by setting may_push=False
    Later the function can be run again with may_push=True to actually push the boxes.
    """
    n_pos = (c_pos[0], c_pos[1] + dxy[1])
    n_grid = grid[n_pos]
    assert n_grid in "[]" # assert that we are pushing a box to begin with
    
    # vertical box movement
    # see which columns the box is spanning
    box_columns = [n_pos[0], n_pos[0]+1 if n_grid == '[' else n_pos[0]-1]
    assert grid[box_columns[0], n_pos[1]] == n_grid
    assert grid[box_columns[1], n_pos[1]] == BBOX_OTHER[n_grid]

    column_status = {}
    for c in box_columns:
        c_n_pos = (c, n_pos[1] + dxy[1])
        c_n_grid = grid[c_n_pos]
        if c_n_grid == ".":
            column_status[c] = "."
        elif c_n_grid == "#":
            column_status[c] = "#"
        elif c_n_grid in "[]":
            # initiate a recursive push to the box in this column
            column_status[c] = push_big_box_vertical(grid, (c, n_pos[1]), dxy, may_push=may_push)
        else:
            raise RuntimeError(f"Unexpected grid value {c_n_grid}")
    if '#' in column_status.values():
        # we hit a wall
        return "#"
    
    if may_push:
        # we can push the box so update the grid
        for c in box_columns:
            grid[c, n_pos[1] + dxy[1]] = grid[c, n_pos[1]]
            grid[c, n_pos[1]] = '.' # free space
    return '.'   

DEBUG = False 

def solve(data, part2=False):
    if part2:
        # double the size of the grid and boxes
        data = ''.join({'O': '[]', '.': '..', '@': "@.", '#': '##'}.get(c,c) for c in data)
    
    grid, robot, moves = parse(data)
    if DEBUG:
        print_grid(grid, robot)

    for m in moves:
        if DEBUG:
            print(m)
        dxy = dXY[m]
        nRobot = (robot[0] + dxy[0], robot[1] + dxy[1])
        nGrid = grid[nRobot]
        if nGrid == ".":
            robot = nRobot # free space
        elif nGrid == "#":
            continue # wall
        elif nGrid == "O":
            # we hit a box find the end of any sequence of boxes in this direction
            endBox = nRobot
            while grid[endBox] == "O":
                endBox = (endBox[0] + dxy[0], endBox[1] + dxy[1])
            endBoxGrid = grid[endBox]
            # check if we can push the box
            if endBoxGrid == ".":
                robot = nRobot
                grid[endBox] = "O"
                grid[nRobot] = "."
            elif endBoxGrid == "#":
                continue
            else:
                raise RuntimeError(f"Unexpected grid value {nGrid}")
        
        elif nGrid in "[]" and dxy[1] == 0:
            # horizontal double box movement
            endBox = nRobot
            while grid[endBox] in "[]":
                endBox = (endBox[0] + dxy[0], endBox[1])
            endBoxGrid = grid[endBox]
            # check if we can push the box
            if endBoxGrid == ".":
                robot = nRobot
                grid[nRobot] = "." # free space
                box_c = ']' if dxy[0] > 0 else '['
                while endBox != nRobot:
                    grid[endBox] = box_c
                    endBox = (endBox[0] - dxy[0], endBox[1])
                    box_c = ']' if box_c == '[' else '['
            elif endBoxGrid == "#":
                pass
            else:
                raise RuntimeError(f"Unexpected grid value {endBoxGrid}")
            
        elif nGrid in "[]" and dxy[0] == 0:
            # test if we can push the box
            v_result = push_big_box_vertical(grid, robot, dxy, may_push=False)
            if v_result == ".":
                push_big_box_vertical(grid, robot, dxy, may_push=True)
                robot = nRobot
        else:
            raise RuntimeError(f"Unexpected grid value {nGrid}")
    
        if DEBUG:
            print_grid(grid, robot)

    C = 'O' if not part2 else '['
    result = sum(100*y + x for x,y in grid if grid[x,y] == C)
    return result


def test_example_small():
    result = solve(EXAMPLE_DATA_SMALL)
    print(f"example: {result}")
    assert result == 2028

def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 10092

def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 1526018

EXAMPLE_DATA_2 = """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""

def test_example2_small():
    result = solve(EXAMPLE_DATA_2, part2=True)
    print(f"example 2: {result}")
    assert result == 618

def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 9021

def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result == 1550677


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()