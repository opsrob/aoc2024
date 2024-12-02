#!/usr/bin/env python

# Read columns from text file
def read_two_columns(filename):
    column1 = []
    column2 = []

    with open (filename, 'r') as file:
        for line in file:
            numbers = line.strip().split('   ')
            column1.append(int(numbers[0]))
            column2.append(int(numbers[1]))
    return column1, column2

# Sort
def sort_list(values):
    return sorted(values)

# Solve the puzzle
col1, col2 = read_two_columns('input.txt')
col1_sorted = sort_list(col1)
col2_sorted = sort_list(col2)

distance = 0

for num in range(len(col1_sorted)):
    distance += abs(col1_sorted[num] - col2_sorted[num])

print(distance)