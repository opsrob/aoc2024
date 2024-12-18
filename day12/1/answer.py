#!/usr/bin/env python
"""
You're about to settle near a complex arrangement of garden plots
when some Elves ask if you can lend a hand. They'd like to set up
fences around each region of garden plots, but they can't figure
out how much fence they need to order or how much it will cost.
They hand you a map (your puzzle input) of the garden plots.

Each garden plot grows only a single type of plant and is indicated
by a single letter on your map. When multiple garden plots are
growing the same type of plant and are touching (horizontally or
vertically), they form a region. For example:

AAAA
BBCD
BBCC
EEEC

This 4x4 arrangement includes garden plots growing five different
types of plants (labeled A, B, C, D, and E), each grouped into
their own region.

In order to accurately calculate the cost of the fence around a
single region, you need to know that region's area and perimeter.

The area of a region is simply the number of garden plots the region
contains. The above map's type A, B, and C plants are each in a region
of area 4. The type E plants are in a region of area 3; the type D
plants are in a region of area 1.

Each garden plot is a square and so has four sides. The perimeter of a
region is the number of sides of garden plots in the region that do not
touch another garden plot in the same region. The type A and C plants
are each in a region with perimeter 10. The type B and E plants are
each in a region with perimeter 8. The lone D plot forms its own region
with perimeter 4.

Visually indicating the sides of plots in each region that contribute
to the perimeter using - and |, the above map's regions' perimeters are
measured as follows:

+-+-+-+-+
|A A A A|
+-+-+-+-+     +-+
              |D|
+-+-+   +-+   +-+
|B B|   |C|
+   +   + +-+
|B B|   |C C|
+-+-+   +-+ +
          |C|
+-+-+-+   +-+
|E E E|
+-+-+-+

Plants of the same type can appear in multiple separate regions, and
regions can even appear within other regions. For example:

OOOOO
OXOXO
OOOOO
OXOXO
OOOOO

The above map contains five regions, one containing all of the O garden
plots, and the other four each containing a single X plot.

The four X regions each have area 1 and perimeter 4. The region containing
21 type O plants is more complicated; in addition to its outer edge
contributing a perimeter of 20, its boundary with each X region contributes
an additional 4 to its perimeter, for a total perimeter of 36.

Due to "modern" business practices, the price of fence required for a
region is found by multiplying that region's area by its perimeter. The total
price of fencing all regions on a map is found by adding together the price
of fence for every region on the map.

In the first example, region A has price 4 * 10 = 40, region B has price
4 * 8 = 32, region C has price 4 * 10 = 40, region D has price 1 * 4 = 4,
and region E has price 3 * 8 = 24. So, the total price for the first
example is 140.

In the second example, the region with all of the O plants has price
21 * 36 = 756, and each of the four smaller X regions has price 1 * 4 = 4,
for a total price of 772 (756 + 4 + 4 + 4 + 4).

Here's a larger example:

RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE

It contains:

    A region of R plants with price 12 * 18 = 216.
    A region of I plants with price 4 * 8 = 32.
    A region of C plants with price 14 * 28 = 392.
    A region of F plants with price 10 * 18 = 180.
    A region of V plants with price 13 * 20 = 260.
    A region of J plants with price 11 * 20 = 220.
    A region of C plants with price 1 * 4 = 4.
    A region of E plants with price 13 * 18 = 234.
    A region of I plants with price 14 * 22 = 308.
    A region of M plants with price 5 * 12 = 60.
    A region of S plants with price 3 * 8 = 24.

So, it has a total price of 1930.

What is the total price of fencing all regions on your map?
"""
from collections import defaultdict

def read_input(filename):
    '''Read and return the garden plot map from the input file'''
    with open(filename, encoding='us-ascii') as f:
        return f.read().strip()

def parse_map(input_text):
    '''Convert input text into a 2D list of characters'''
    return [list(line) for line in input_text.split('\n')]

def find_regions(garden_map):
    '''
    Find all regions in the garden map using flood fill.
    Returns a dict mapping coordinates to region IDs.
    '''
    height = len(garden_map)
    width = len(garden_map[0])
    regions = {}
    region_id = 0
    
    def flood_fill(x, y, plant_type, region_id):
        '''Helper function to perform flood fill on a region'''
        if (x < 0 or x >= width or y < 0 or y >= height or 
            (y, x) in regions or garden_map[y][x] != plant_type):
            return
        
        regions[(y, x)] = region_id
        # Check adjacent cells (up, down, left, right)
        flood_fill(x, y-1, plant_type, region_id)
        flood_fill(x, y+1, plant_type, region_id)
        flood_fill(x-1, y, plant_type, region_id)
        flood_fill(x+1, y, plant_type, region_id)
    
    # Find all regions using flood fill
    for y, row in enumerate(garden_map):
        for x, cell in enumerate(row):
            if (y, x) not in regions:
                flood_fill(x, y, garden_map[y][x], region_id)
                region_id += 1
    
    return regions

def calculate_region_stats(garden_map, regions):
    '''
    Calculate area and perimeter for each region.
    Returns a dict mapping region IDs to (area, perimeter) tuples.
    '''
    height = len(garden_map)
    width = len(garden_map[0])
    stats = defaultdict(lambda: [0, 0])  # [area, perimeter]
    
    for y, row in enumerate(garden_map):
        for x, _ in enumerate(row):
            region_id = regions.get((y, x))
            if region_id is None:
                continue
                
            stats[region_id][0] += 1  # Increment area
            
            # Check each side for perimeter contribution
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx < 0 or nx >= width or ny < 0 or ny >= height or
                    regions.get((ny, nx)) != region_id):
                    stats[region_id][1] += 1  # Increment perimeter
    
    return stats

def calculate_total_price(stats):
    '''Calculate the total price based on area and perimeter of all regions'''
    return sum(area * perimeter for area, perimeter in stats.values())

def solve_puzzle(filename='input.txt'):
    '''Main function to solve the garden fence puzzle'''
    # Read and parse input
    input_text = read_input(filename)
    garden_map = parse_map(input_text)
    
    # Find regions using flood fill
    regions = find_regions(garden_map)
    
    # Calculate statistics for each region
    stats = calculate_region_stats(garden_map, regions)
    
    # Calculate and return total price
    return calculate_total_price(stats)

if __name__ == '__main__':
    result = solve_puzzle()
    print(f'The total price of fencing all regions is: {result}') # should print 1461806
