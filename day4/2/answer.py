#!/usr/bin/env python

"""
Looking for the instructions, you flip over the word search to find that this isn't
actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two
MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S

Irrelevant characters have again been replaced with . in the above diagram. Within the X,
each MAS can be written forwards or backwards.
"""

def read_grid(filename):
    """open file and print info to validate"""
    with open(filename, 'r', encoding='us-ascii') as file:
        grid = [list(line.strip()) for line in file]
    print(f"Number of rows: {len(grid)}")
    print(f"Number of columns: {len(grid[0])}")
    return grid

def search2D(grid):
    m = len(grid)
    n = len(grid[0])
    candidates = []
    count = 0

    # find all coords that contain letter "A"
    # stay 1 character away from the boundary
    for i in range(m - 1):
        for j in range(n - 1):
            if grid[i][j] == "A":
                candidates.append((i, j))

    for i, j in candidates:
        if ((grid[i - 1][j - 1] == "S" and grid[i + 1][j + 1] == "M") or
            (grid[i - 1][j - 1] == "M" and grid[i + 1][j + 1] == "S")):
            if ((grid[i + 1][j-1] == "S" and grid[i - 1][j + 1] == "M") or
                (grid[i + 1][j-1] == "M" and grid[i - 1][j + 1] == "S")):
                count += 1
    return count

def main():
    grid = read_grid("input.txt")
    count = search2D(grid)
    print("Total Occurrences:", count)

if __name__ == "__main__":
    main()
