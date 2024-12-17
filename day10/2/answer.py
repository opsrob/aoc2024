#!/usr/bin/env python
"""
--- Part Two ---

The reindeer spends a few minutes reviewing your hiking trail map before realizing
something, disappearing for a few minutes, and finally returning with yet another
slightly-charred piece of paper.

The paper describes a second way to measure a trailhead called its rating. A
trailhead's rating is the number of distinct hiking trails which begin at that
trailhead. For example:

.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....

The above map has a single trailhead; its rating is 3 because there are exactly
three distinct hiking trails which begin at that position:

.....0.   .....0.   .....0.
..4321.   .....1.   .....1.
..5....   .....2.   .....2.
..6....   ..6543.   .....3.
..7....   ..7....   .....4.
..8....   ..8....   ..8765.
..9....   ..9....   ..9....

Here is a map containing a single trailhead with rating 13:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....

This map contains a single trailhead with rating 227 (because there are 121 distinct
hiking trails that lead to the 9 on the right edge and 106 that lead to the 9 on
the bottom edge):

012345
123456
234567
345678
4.6789
56789.

Here's the larger example from before:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732

Considering its trailheads in reading order, they have ratings of 20, 24, 10, 4, 1,
4, 5, 8, and 5. The sum of all trailhead ratings in this larger example topographic
map is 81.

You're not sure how, but the reindeer seems to have crafted some tiny flags out of
toothpicks and bits of paper and is using them to mark trailheads on your topographic
map. What is the sum of the ratings of all trailheads?
"""

def read_input(filename='input.txt'):
    '''Read and parse input file into a 2D grid'''
    with open(filename) as f:
        return [[int(c) for c in line.strip()] for line in f]

def get_neighbors(grid, pos):
    '''Return valid adjacent positions (up, down, left, right) for a given position'''
    rows, cols = len(grid), len(grid[0])
    r, c = pos
    neighbors = []
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < rows and 0 <= new_c < cols:
            neighbors.append((new_r, new_c))
    return neighbors

def find_trailheads(grid):
    '''Find all positions with height 0'''
    trailheads = []
    for r, row in enumerate(grid):
        for c, height in enumerate(row):
            if height == 0:
                trailheads.append((r, c))
    return trailheads

def count_distinct_trails(grid, start):
    '''Count number of distinct hiking trails from start to any height 9'''
    rows, cols = len(grid), len(grid[0])
    visited = set()
    trail_count = 0
    
    def dfs(pos, current_height):
        '''DFS to count distinct trails following hiking rules'''
        nonlocal trail_count
        if current_height == 9:
            trail_count += 1
            return
            
        r, c = pos
        for next_pos in get_neighbors(grid, pos):
            nr, nc = next_pos
            next_height = grid[nr][nc]
            
            if (next_height == current_height + 1 and 
                next_pos not in visited):
                visited.add(next_pos)
                dfs(next_pos, next_height)
                visited.remove(next_pos)
    
    visited.add(start)
    dfs(start, 0)
    return trail_count

def solve(grid):
    '''Find sum of ratings for all trailheads'''
    trailheads = find_trailheads(grid)
    return sum(count_distinct_trails(grid, pos) for pos in trailheads)

def main():
    '''Main solution entry point'''
    grid = read_input()
    result = solve(grid)
    print(f'Sum of trailhead ratings: {result}') # should be 1459

if __name__ == '__main__':
    main()