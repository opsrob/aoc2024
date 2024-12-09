#!/usr/bin/env python

"""
After updating your model, it turns out that an antinode occurs at any grid
position exactly in line with at least two antennas of the same frequency,
regardless of distance. This means that some of the new antinodes will occur
at the position of each antenna (unless that antenna is the only one of its
frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........

In fact, the three T-frequency antennas are all exactly in line with two antennas,
so they are all also antinodes! This brings the total number of antinodes in the
above example to 9.

The original example now has 34 antinodes, including the antinodes that appear
on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##

Calculate the impact of the signal using this updated model. How many unique locations
within the bounds of the map contain an antinode?
"""

def read_map(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f.readlines()]

def find_antennas(grid):
    frequencies = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != '.':
                if cell not in frequencies:
                    frequencies[cell] = []
                frequencies[cell].append((x, y))
    return frequencies

def is_aligned(p1, p2, p3):
    return (p2[1] - p1[1]) * (p3[0] - p1[0]) == (p3[1] - p1[1]) * (p2[0] - p1[0])

def find_antinodes(grid, antennas):
    antinodes = set()
    height = len(grid)
    width = len(grid[0])

    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue

        for pos in positions:
            antinodes.add(pos)

        for y in range(height):
            for x in range(width):
                point = (x, y)
                for i, pos1 in enumerate(positions[:-1]):
                    for pos2 in positions[i+1:]:
                        if is_aligned(pos1, pos2, point):
                            antinodes.add(point)
                            break
                    if point in antinodes:
                        break

    return antinodes

def solve(filename):
    grid = read_map(filename)
    antennas = find_antennas(grid)
    antinodes = find_antinodes(grid, antennas)
    return len(antinodes)

print(solve('input.txt')) # should be 1231