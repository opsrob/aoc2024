#!/usr/bin/env python

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

def count_reachable_peaks(grid, start):
    '''Count number of height 9 positions reachable via valid hiking trails from start'''
    rows, cols = len(grid), len(grid[0])
    visited = set()
    peaks = set()
    
    def dfs(pos, current_height):
        '''DFS to find all reachable peaks following trail rules'''
        if current_height == 9:
            peaks.add(pos)
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
    return len(peaks)

def solve(grid):
    '''Find sum of scores for all trailheads'''
    trailheads = find_trailheads(grid)
    return sum(count_reachable_peaks(grid, pos) for pos in trailheads)

def main():
    '''Main solution entry point'''
    grid = read_input()
    result = solve(grid)
    print(f'Sum of trailhead scores: {result}')

if __name__ == '__main__':
    main()