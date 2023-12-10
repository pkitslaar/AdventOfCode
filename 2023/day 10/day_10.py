"""
Advent of Code 2023 - Day 10
Pieter Kitslaar
"""


import networkx as nx


def parse(data):
    grid = {}
    start_pos = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c != ".":
                grid[(x, y)] = c
                if c == "S":
                    start_pos = (x, y)
    return grid, start_pos


def to_graph(grid, start_pos):
    G = nx.Graph()
    for pos, c in grid.items():
        match c:
            case "S":
                G.add_node(pos, label="S")
            case "7":
                G.add_node(pos, label="7")
                # left neighbour
                n1 = (pos[0] - 1, pos[1])
                if grid.get(n1, ".") not in ".J7|":
                    G.add_edge(n1, pos)
                # bottom neighbour
                n2 = (pos[0], pos[1] + 1)
                if grid.get(n2, ".") not in ".F7-":
                    G.add_edge(n2, pos)
            case "F":
                G.add_node(pos, label="F")
                # right neighbour
                n1 = (pos[0] + 1, pos[1])
                if grid.get(n1, ".") not in ".FL|":
                    G.add_edge(n1, pos)
                # bottom neighbour
                n2 = (pos[0], pos[1] + 1)
                if grid.get(n2, ".") not in ".F7-":
                    G.add_edge(n2, pos)
            case "L":
                G.add_node(pos, label="L")
                # top neighbour
                n1 = (pos[0], pos[1] - 1)
                if grid.get(n1, ".") not in ".LJ-":
                    G.add_edge(n1, pos)
                # right neighbour
                n2 = (pos[0] + 1, pos[1])
                if grid.get(n2, ".") not in ".FL|":
                    G.add_edge(n2, pos)
            case "J":
                G.add_node(pos, label="J")
                # top neighbour
                n1 = (pos[0], pos[1] - 1)
                if grid.get(n1, ".") not in ".LJ-":
                    G.add_edge(n1, pos)
                # left neighbour
                n2 = (pos[0] - 1, pos[1])
                if grid.get(n2, ".") not in ".J7|":
                    G.add_edge(n2, pos)
            case "-":
                G.add_node(pos, label="-")
                # left neighbour
                n1 = (pos[0] - 1, pos[1])
                if grid.get(n1, ".") not in ".J7|":
                    G.add_edge(n1, pos)
                # right neighbour
                n2 = (pos[0] + 1, pos[1])
                if grid.get(n2, ".") not in ".FL|":
                    G.add_edge(n2, pos)
            case "|":
                G.add_node(pos, label="|")
                # top neighbour
                n1 = (pos[0], pos[1] - 1)
                if grid.get(n1, ".") not in ".LJ-":
                    G.add_edge(n1, pos)
                # bottom neighbour
                n2 = (pos[0], pos[1] + 1)
                if grid.get(n2, ".") not in ".F7-":
                    G.add_edge(n2, pos)
            case _:
                raise Exception(f"Unknown character {c}")
    return G.to_undirected(), start_pos


from heapq import heappush, heappop, heapify


def find_cycle(G, start_pos):
    visited = {start_pos: 0}
    loop_edges = []
    # pick one neighbour from the start position
    neighbours = list(G.neighbors(start_pos))
    fist_neighbour = neighbours[0]
    other_neighbours = neighbours[1:]
    to_visit = [(1, neighbours[0], (start_pos, fist_neighbour))]

    while to_visit:
        distance, current, edge = heappop(to_visit)
        if current in visited:
            continue
        visited[current] = distance
        loop_edges.append(edge)
        if current in other_neighbours:
            # found loop
            loop_edges.append((current, start_pos))
            break

        neighbours = list(G.neighbors(current))
        for neighbour in neighbours:
            if neighbour not in visited:
                heappush(to_visit, (distance + 1, neighbour, (current, neighbour)))
    # find signed area to see if loop is clockwise
    area = 0
    for (u, v) in loop_edges:
        area += (v[0] - u[0]) * (v[1] + u[1])
    if area > 0:
        # reverse loop
        loop_edges = [(v, u) for (u, v) in reversed(loop_edges)]
    return loop_edges


def solve(data, part2=False):
    grid, start_pos = parse(data)
    graph, start_pos = to_graph(grid, start_pos)
    loop_edges = find_cycle(graph, start_pos)
    # loop_edges_nx = nx.find_cycle(graph, start_pos)
    # assert loop_edges == loop_edges_nx
    loop_nodes = []
    for edge in loop_edges:
        loop_nodes.extend(edge)
    min_x = min([pos[0] for pos in loop_nodes])
    max_x = max([pos[0] for pos in loop_nodes])
    min_y = min([pos[1] for pos in loop_nodes])
    max_y = max([pos[1] for pos in loop_nodes])
    loop_grid = [["."] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for edge in loop_edges:
        u, _ = edge
        loop_grid[u[1] - min_y][u[0] - min_x] = graph.nodes[u]["label"]
    print("\n".join("".join(row) for row in loop_grid))

    distances = {}
    distances[start_pos] = 0
    for (u, v) in loop_edges[:-1]:
        distances[v] = distances[u] + 1
    for (v, u) in reversed(loop_edges[1:]):
        distances[v] = min([distances[v], distances[u] + 1])
    return max(distances.values())


EXAMPLE_DATA_1A = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""


def test_example_1a():
    result = solve(EXAMPLE_DATA_1A)
    print(f"example: {result}")
    assert result == 4


EXAMPLE_DATA_1B = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""


def test_example_1b():
    result = solve(EXAMPLE_DATA_1B)
    print(f"example: {result}")
    assert result == 8


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 6690


EXAMPLE_DATA_2A = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""


def solve2(data):
    grid, start_pos = parse(data)
    graph, start_pos = to_graph(grid, start_pos)
    loop_edges = find_cycle(graph, start_pos)

    inside_candidates = set()
    loop_positions = set()
    for (u, v) in loop_edges:
        loop_positions.add(u)
        loop_positions.add(v)
        direction = (v[0] - u[0], v[1] - u[1])
        if direction == (0, 1):
            # downqards add candidate to left
            inside_candidates.add((u[0] - 1, u[1]))
            inside_candidates.add((v[0] - 1, v[1]))
        elif direction == (0, -1):
            # upwards add candidate to right
            inside_candidates.add((u[0] + 1, u[1]))
            inside_candidates.add((v[0] + 1, v[1]))
        elif direction == (1, 0):
            # right add candidate to bottom
            inside_candidates.add((u[0], u[1] + 1))
            inside_candidates.add((v[0], v[1] + 1))
        elif direction == (-1, 0):
            # left add candidate to top
            inside_candidates.add((u[0], u[1] - 1))
            inside_candidates.add((v[0], v[1] - 1))
        else:
            raise Exception(f"Unknown direction {direction}")
    inside_candidates = inside_candidates - loop_positions

    OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = set()
    to_visit = [(0, p) for p in inside_candidates]
    heapify(to_visit)
    while to_visit:
        distance, current = heappop(to_visit)
        if current in visited:
            continue
        if current in loop_positions:
            continue
        visited.add(current)
        for offset in OFFSETS:
            neighbour = (current[0] + offset[0], current[1] + offset[1])
            # if neighbour not in visited and neighbour not in loop_positions:
            heappush(to_visit, (distance + 1, neighbour))
    return len(visited)


def test_example2a():
    result = solve2(EXAMPLE_DATA_2A)
    print(f"example 2: {result}")
    assert result == 4


EXAMPLE_DATA_2B = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""


def test_example2b():
    result = solve2(EXAMPLE_DATA_2B)
    print(f"example 2: {result}")
    assert result == 8


EXAMPLE_DATA_2C = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


def test_example2c():
    result = solve2(EXAMPLE_DATA_2C)
    print(f"example 2: {result}")
    assert result == 10


def test_part2():
    result = solve2(data())
    print("Part 2:", result)
    assert result == 525


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
