#!/usr/bin/env python

"""
Day 2, Problem 1
The unusual data (your puzzle input) consists of many reports, one report per line. Each 
report is a list of numbers called levels that are separated by spaces. For example:

7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9

This example data contains six reports each containing five levels.

The engineers are trying to figure out which reports are safe. The Red-Nosed reactor safety 
systems can only tolerate levels that are either gradually increasing or gradually decreasing.
So, a report only counts as safe if both of the following are true:

    The levels are either all increasing or all decreasing.
    Any two adjacent levels differ by at least one and at most three.

In the example above, the reports can be found safe or unsafe by checking those rules:

    7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
    1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
    9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
    1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
    8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
    1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.

So, in this example, 2 reports are safe.

Analyze the unusual data from the engineers. How many reports are safe?
"""

def is_valid_row(row):
    """
    Check if a row of numbers is valid based on both conditions:
    1. The numbers are either all increasing or all decreasing
    2. Adjacent numbers differ by at least 1 and at most 3
    """
    # Check if the row is empty or has only one number
    if len(row) <= 1:
        return True

    # Determine if the row should be increasing or decreasing
    is_increasing = row[0] < row[1]

    # Check each pair of adjacent numbers
    for i in range(len(row) - 1):
        # Check if the sequence follows the initial trend (increasing or decreasing)
        if is_increasing and row[i] >= row[i + 1]:
            return False
        if not is_increasing and row[i] <= row[i + 1]:
            return False

        # Check the difference between adjacent numbers
        diff = abs(row[i] - row[i + 1])
        if diff < 1 or diff > 3:
            return False
    return True

def process_input_file(filename):
    """
    Process the file and increment safe counter if True
    """
    safe = 0
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file, 1):
            # Convert lines to lists of integers
            row = list(map(int, line.split()))
            result = is_valid_row(row)
            if result == True:
                safe += 1
    print(f"Total Safe: {safe}")

# solve the puzzle
process_input_file('input.txt') # Should print 213
