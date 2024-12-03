#!/usr/bin/env python

"""
Day 2, Problem 2
The engineers are surprised by the low number of safe reports until they 
realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor
safety systems tolerate a single bad level in what would otherwise be a
safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level
from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

    7 6 4 2 1: Safe without removing any level.
    1 2 7 8 9: Unsafe regardless of which level is removed.
    9 7 6 2 1: Unsafe regardless of which level is removed.
    1 3 2 4 5: Safe by removing the second level, 3.
    8 6 4 4 1: Safe by removing the third level, 4.
    1 3 6 7 9: Safe without removing any level.

Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can
remove a single level from unsafe reports. How many reports are now safe?
"""

def is_valid_row(row):
    """
    Check if a row of numbers is valid based on three conditions:

    via first_2_valid function:
    1. The numbers are either all increasing or all decreasing
    2. Adjacent numbers differ by at least 1 and at most 3

    via this function:
    3. If removing a single level from an unsafe report would make it safe, 
    the report instead counts as safe
    """
    # Check if the row is empty or has only one or two numbers
    if len(row) <= 2:
        return True

    # Check if first two conditions are valid
    if first_2_valid(row):
        return True

    # See if Problem Dampener makes row valid by removing each number
    for i in range(len(row)):
        test_row = row[:i] + row[i + 1:]

        if first_2_valid(test_row):
            return True


def first_2_valid(row):
    """
    Check if a row of numbers is valid based on first 2 conditions:
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
process_input_file('input.txt') # Should print 285
