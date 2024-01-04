"""
Advent of Code 2023 - Day 23
Pieter Kitslaar
"""

EXAMPLE_DATA = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

import networkx as nx

NEIGHBORS = {
    ".": [(0, 1), (0, -1), (1, 0), (-1, 0)],
    "^": [(0, -1)],
    "v": [(0, 1)],
    ">": [(1, 0)],
    "<": [(-1, 0)],
}


def solve(data, part2=False):
    grid = {}
    start_pos = None
    end_pos = None
    slopes = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if c == ".":
                if not start_pos:
                    start_pos = (x, y)
                else:
                    end_pos = (x, y)

            if c in "^v<>":
                slopes[x, y] = c

            grid[x, y] = c

    graph = nx.DiGraph()
    for pos in grid:
        x, y = pos
        c = grid[pos]
        if c == "#":
            continue
        for dx, dy in NEIGHBORS[c]:
            new_pos = (x + dx, y + dy)
            if new_pos in grid:
                nc = grid[new_pos]
                if nc == "#":
                    continue
                elif nc == "v" and dy == -1:
                    continue
                elif nc == "^" and dy == 1:
                    continue
                elif nc == ">" and dx == -1:
                    continue
                elif nc == "<" and dx == 1:
                    continue

                graph.add_edge(pos, new_pos)

    if not part2:
        all_path_lenghts = [
            len(p) - 1 for p in nx.all_simple_paths(graph, start_pos, end_pos)
        ]
        result = max(all_path_lenghts)
    else:
        graph = graph.to_undirected()
        for edge in graph.edges():
            graph.get_edge_data(*edge)["weight"] = 1

        found_node_to_remove = True
        while found_node_to_remove:
            found_node_to_remove = False
            for n in graph.nodes():
                n_edges = [*graph.edges(n)]
                if len(n_edges) == 2:
                    neighbors = [e[1] for e in n_edges]
                    weight_sum = sum(
                        [graph.get_edge_data(*e)["weight"] for e in n_edges]
                    )
                    graph.remove_node(n)
                    graph.add_edge(*neighbors, weight=weight_sum)
                    found_node_to_remove = True
                    break

        result = 0
        for p in nx.all_simple_paths(graph, start_pos, end_pos):
            this_len = sum(
                [graph.get_edge_data(*e)["weight"] for e in zip(p[:-1], p[1:])]
            )
            if this_len > result:
                result = this_len
    return result


def test_example():
    result = solve(EXAMPLE_DATA)
    print(f"example: {result}")
    assert result == 94


def test_part1():
    result = solve(data())
    print("Part 1:", result)
    assert result == 2218


def test_example2():
    result = solve(EXAMPLE_DATA, part2=True)
    print(f"example 2: {result}")
    assert result == 154


def test_part2():
    result = solve(data(), part2=True)
    print("Part 2:", result)
    assert result > 5634
    assert result == 6674


from pathlib import Path

THIS_DIR = Path(__file__).parent


def data():
    with open(THIS_DIR / "input.txt") as f:
        return f.read()
