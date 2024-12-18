#!/usr/bin/env python
"""
Fortunately, the Elves are trying to order so much fence that they qualify for
a bulk discount!

Under the bulk discount, instead of using the perimeter to calculate the price,
you need to use the number of sides each region has. Each straight section of
fence counts as a side, regardless of how long it is.

Consider this example again:

AAAA
BBCD
BBCC
EEEC

The region containing type A plants has 4 sides, as does each of the regions
containing plants of type B, D, and E. However, the more complex region containing
the plants of type C has 8 sides!

Using the new method of calculating the per-region price by multiplying the region's
area by its number of sides, regions A through E have prices 16, 16, 32, 4, and 12,
respectively, for a total price of 80.

The second example above (full of type X and O plants) would have a total price of
436.

Here's a map that includes an E-shaped region full of type E plants:

EEEEE
EXXXX
EEEEE
EXXXX
EEEEE

The E-shaped region has an area of 17 and 12 sides for a price of 204. Including
the two regions full of type X plants, this map has a total price of 236.

This map has a total price of 368:

AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA

It includes two regions full of type B plants (each with 4 sides) and a single
region full of type A plants (with 4 sides on the outside and 8 more sides on
the inside, a total of 12 sides). Be especially careful when counting the fence
around regions like the one full of type A plants; in particular, each section
of fence has an in-side and an out-side, so the fence does not connect across
the middle of the region (where the two B regions touch diagonally). (The Elves
would have used the Möbius Fencing Company instead, but their contract terms
were too one-sided.)

The larger example from before now has the following updated prices:

    A region of R plants with price 12 * 10 = 120.
    A region of I plants with price 4 * 4 = 16.
    A region of C plants with price 14 * 22 = 308.
    A region of F plants with price 10 * 12 = 120.
    A region of V plants with price 13 * 10 = 130.
    A region of J plants with price 11 * 12 = 132.
    A region of C plants with price 1 * 4 = 4.
    A region of E plants with price 13 * 8 = 104.
    A region of I plants with price 14 * 16 = 224.
    A region of M plants with price 5 * 6 = 30.
    A region of S plants with price 3 * 6 = 18.

Adding these together produces its new total price of 1206.

What is the new total price of fencing all regions on your map?
"""

from collections import deque
from typing import List, Set, Tuple

def read_input(filename: str) -> List[str]:
    """Read and return the garden map from the input file"""
    with open(filename, 'r', encoding='us-ascii') as f:
        return [line.strip() for line in f]

def get_connected_region(
    start: Tuple[int, int],
    plant_type: str,
    grid: List[str]
) -> Set[Tuple[int, int]]:

    """Find all cells in a connected region starting from given coordinate"""
    rows, cols = len(grid), len(grid[0])
    region = set()
    queue = deque([start])

    while queue:
        i, j = queue.popleft()
        if (i, j) in region:
            continue

        region.add((i, j))
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if (0 <= ni < rows and 0 <= nj < cols and 
                grid[ni][nj] == plant_type and 
                (ni, nj) not in region):
                queue.append((ni, nj))

    return region

def count_region_sides(region: Set[Tuple[int, int]]) -> int:
    """
    Count sides by examining corners of cells.
    Each corner contributes to the side count based on its configuration.
    """
    # Generate all corner points
    corner_candidates = set()
    for r, c in region:
        for cr, cc in [(r - 0.5, c - 0.5), (r + 0.5, c - 0.5), 
                       (r + 0.5, c + 0.5), (r - 0.5, c + 0.5)]:
            corner_candidates.add((cr, cc))

    corners = 0
    for cr, cc in corner_candidates:
        # Check configuration of cells around this corner
        config = [
            (int(cr - 0.5), int(cc - 0.5)) in region,
            (int(cr + 0.5), int(cc - 0.5)) in region,
            (int(cr + 0.5), int(cc + 0.5)) in region,
            (int(cr - 0.5), int(cc + 0.5)) in region
        ]
        cell_count = sum(config)

        if cell_count == 1:  # Single cell corner
            corners += 1
        elif cell_count == 2:  # Two cells
            # Check if they're diagonal
            if config in ([True, False, True, False], [False, True, False, True]):
                corners += 2
            # Adjacent cells don't add a corner
        elif cell_count == 3:  # Three cells
            corners += 1
        # Four cells don't add a corner

    return corners

def find_all_regions(grid: List[str]) -> List[Set[Tuple[int, int]]]:
    """Find all distinct regions in the grid"""
    rows, cols = len(grid), len(grid[0])
    seen = set()
    regions = []

    for r in range(rows):
        for c in range(cols):
            if (r, c) in seen:
                continue

            seen.add((r, c))
            region = get_connected_region((r, c), grid[r][c], grid)
            regions.append(region)
            seen.update(region)

    return regions

def calculate_total_price(grid: List[str]) -> int:
    """Calculate the total price of all regions in the garden"""
    total_price = 0
    regions = find_all_regions(grid)

    for region in regions:
        area = len(region)
        sides = count_region_sides(region)
        price = area * sides
        plant_type = grid[next(iter(region))[0]][next(iter(region))[1]]
        print(f'Region {plant_type}: Area={area}, Sides={sides}, Price={price}')
        total_price += price

    return total_price

def solve(filename: str) -> int:
    """Solve the puzzle by reading input and calculating total price"""
    grid = read_input(filename)
    return calculate_total_price(grid)

if __name__ == '__main__':
    result = solve('input.txt')
    print(f'Total price: {result}') # should be 887932
