#!/usr/bin/env python
from collections import Counter

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

# Count matches
def count_matches(match1, match2):
    match2_counter = Counter(match2)
    return [match2_counter[num] for num in match1]

# Solve the puzzle
col1, col2 = read_two_columns('input.txt')

similarity = 0

for i in range(len(col1)):
    matches = count_matches(col1, col2)
    similarity += abs((col1[i]) * (matches[i]))

print(similarity)