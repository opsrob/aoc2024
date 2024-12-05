#!/usr/bin/env python

"""
Help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards,
or even overlapping other words. It's a little unusual, though, as you don't merely need
to find one instance of XMAS - you need to find all of them.
"""

# Based off of https://www.geeksforgeeks.org/search-a-word-in-a-2d-grid-of-characters/
# with modifications for counting and reading from file

COUNT = []

def read_grid(filename):
    """open file and print info to validate"""
    with open(filename, 'r', encoding='us-ascii') as file:
        grid = [list(line.strip()) for line in file]
    print(f'Number of rows: {len(grid)}')
    print(f'Number of columns: {len(grid[0])}')
    return grid

def search_2d(grid, row, col, word):
    """search the grid"""
    m = len(grid)
    n = len(grid[0])

    # return false if the given coordinate
    # does not match with first index char.
    if grid[row][col] != word[0]:
        return False

    len_word = len(word)

    # x and y are used to set the direction in which
    # word needs to be searched.
    x = [-1, -1, -1, 0, 0, 1, 1, 1]
    y = [-1, 0, 1, -1, 1, -1, 0, 1]

    # This loop will search in all the 8 directions
    # one by one. It will return true if one of the
    # directions contain the word.
    for dir in range(8):

        # Initialize starting point for current direction
        current_x, current_y = row + x[dir], col + y[dir]
        k = 1

        while k < len_word:

            # break if out of bounds
            if current_x >= m or current_x < 0 or current_y >= n or current_y < 0:
                break

            # break if characters dont match
            if grid[current_x][current_y] != word[k]:
                break

            # Moving in particular direction
            current_x += x[dir]
            current_y += y[dir]
            k += 1

        # If all character matched, then value of must
        # be equal to length of word
        if k == len_word:
            COUNT.append((row, col))

def main():
    grid = read_grid('input.txt')
    word = 'XMAS'
    m = len(grid)
    n = len(grid[0])
    for i in range(m):
        for j in range(n):
            search_2d(grid, i, j, word)
    print('Total Occurrences: ', len(COUNT)) # answer should be 2397

if __name__ == '__main__':
    main()
