#!/usr/bin/env python

"""
The computer appears to be trying to run a program, but 
its memory (your puzzle input) is corrupted. All of the
instructions have been jumbled up!

It seems like the goal of the program is just to multiply
some numbers. It does that with instructions like mul(X,Y),
where X and Y are each 1-3 digit numbers. For instance,
mul(44,46) multiplies 44 by 46 to get a result of 2024.
Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted,
there are also many invalid characters that should be ignored,
even if they look like part of a mul instruction. Sequences
like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

Only the four highlighted sections are real mul instructions.
Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions.
What do you get if you add up all of the results of the multiplications?
"""

import re

def parse_and_calculate_mul(filename):
    """
    Parse a text file for valid mul(X,Y) expressions and calculate their total.
    
    Args:
        filename (str): Path to the input text file
    
    Returns:
        int: Sum of all valid multiplication results
    """
    # Regex pattern explanation:
    # - Look for 'mul' followed by exactly '('
    # - Capture first number (1-3 digits): (\d{1,3})
    # - Match a comma
    # - Capture second number (1-3 digits): (\d{1,3})
    # - Match exactly ')'
    # - Surrounded by regex word boundaries to prevent partial matches
    # - Ignore invalid surrounding characters
    # pattern = r'\bmul\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)\b'

    # more inclusive:
    pattern = r'mul\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)'

    total = 0

    try:
        with open(filename, 'r') as file:
            content = file.read()

            # Find all valid mul() expressions
            matches = re.findall(pattern, content)

            # Calculate and sum the multiplications
            for x, y in matches:
                result = int(x) * int(y)
                total += result
                print(f'Found: mul({x},{y}) = {result}')
                print(f'Total: {total}')

    except FileNotFoundError:
        print(f'Error: File {filename} not found.')
    except Exception as e:
        print(f'An error occurred: {e}')

    return total

def main():
    result = parse_and_calculate_mul('input.txt')
    print(f'\nTotal sum of multiplications: {result}') # should be 173419328

if __name__ == '__main__':
    main()
