#!/usr/bin/env python

"""
Maybe you can work out where the guard will go ahead of time so that The
Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^ (to indicate the guard is
currently facing up from the perspective of the map). Any obstructions - crates,
desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly
following these steps:

    If there is something directly in front of you, turn right 90 degrees.
    Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until she reaches
an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard, she turns right before
continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers), she turns right
again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the mapped area
(after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

By predicting the guard's route, you can determine which specific positions in the
lab will be in the patrol path. Including the guard's starting position, the positions
visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before
leaving the mapped area?
"""

def read_map(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f]

def find_guard(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in '^>v<':
                return (x, y, grid[y][x])
    return None

def get_direction(facing):
    return {
        '^': (0, -1),
        '>': (1, 0),
        'v': (0, 1),
        '<': (-1, 0)Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

    If there is something directly in front of you, turn right 90 degrees.
    Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?


    }[facing]

def turn_right(facing):
    return {'^': '>', '>': 'v', 'v': '<', '<': '^'}[facing]

def is_valid(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def solve(filename):
    grid = read_map(filename)
    height, width = len(grid), len(grid[0])
    visited = set()

    # Find guard's starting position
    guard = find_guard(grid)
    if not guard:
        return 0

    x, y, facing = guard
    visited.add((x, y))

    while True:
        dx, dy = get_direction(facing)
        next_x, next_y = x + dx, y + dy

        # Check if guard would leave the area
        if not is_valid(next_x, next_y, grid):
            break

        # If obstacle ahead, turn right
        if grid[next_y][next_x] == '#':
            facing = turn_right(facing)
        else:
            # Move forward
            x, y = next_x, next_y
            visited.add((x, y))

    return len(visited)

if __name__ == "__main__":
    result = solve("input.txt")
    print(f"The guard will visit {result} distinct positions.") # should be 1424
