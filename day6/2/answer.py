#!/usr/bin/env python

"""
Returning after what seems like only a few seconds to The Historians, they explain
that the guard's patrol area is simply too large for them to safely search the lab
without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause
a time paradox. They'd like to place the new obstruction in such a way that the guard
will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to
know all of the possible positions for such an obstruction. The new obstruction can't
be placed at the guard's starting position - the guard is there right now and would
notice.

In the above example, there are only 6 different positions where a new obstruction
would cause the guard to get stuck in a loop. The diagrams of these six situations
use O to mark the new obstruction, | to show a position where the guard moves up/down,
- to show a position where the guard moves left/right, and + to show a position where
the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...

Option two, put a stack of failed suit prototypes in the bottom right quadrant of the
mapped area:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...

Option three, put a crate of chimney-squeeze prototype fabric next to the standing
desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...

Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...

Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...

Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..

It doesn't really matter what you choose to use as an obstacle so long as you and
The Historians can put it into position without the guard noticing. The important
thing is having enough options that you can find one that minimizes time paradoxes,
and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How
many different positions could you choose for this obstruction?
"""

def read_map(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f]

def find_guard(grid):
    """establish starting point on map"""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in '^>v<':
                return (x, y, grid[y][x])
    return None

def get_direction(facing):
    return {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}[facing]

def turn_right(facing):
    return {'^': '>', '>': 'v', 'v': '<', '<': '^'}[facing]

def is_valid(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])

def simulate_path(grid, obstruction_pos=None):
    guard = find_guard(grid)
    if not guard:
        return None
    
    x, y, facing = guard
    path = [(x, y, facing)]
    visited_states = {(x, y, facing)}
    
    while True:
        dx, dy = get_direction(facing)
        next_x, next_y = x + dx, y + dy
        
        # Check if guard would leave the area
        if not is_valid(next_x, next_y, grid):
            return None
            
        # Check if there's an obstacle ahead (including our new obstruction)
        hit_obstacle = grid[next_y][next_x] == '#' or (next_x, next_y) == obstruction_pos
        
        if hit_obstacle:
            facing = turn_right(facing)
        else:
            x, y = next_x, next_y
            
        state = (x, y, facing)
        if state in visited_states:
            return path[path.index(state):]  # Return the loop
        
        visited_states.add(state)
        path.append(state)

def find_loop_positions(filename):
    grid = read_map(filename)
    height, width = len(grid), len(grid[0])
    guard_pos = find_guard(grid)
    valid_positions = set()
    
    # Try each possible position for the new obstruction
    for y in range(height):
        for x in range(width):
            # Skip if position is invalid
            if grid[y][x] != '.' or (x, y) == (guard_pos[0], guard_pos[1]):
                continue
                
            # Check if adding obstruction here creates a loop
            if simulate_path(grid, (x, y)):
                valid_positions.add((x, y))
    
    return len(valid_positions)

if __name__ == "__main__":
    result = find_loop_positions("input.txt")
    print(f"There are {result} possible positions for the obstruction.")