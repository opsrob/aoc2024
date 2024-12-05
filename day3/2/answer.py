#!/usr/bin/env python

"""
There are two new instructions you'll need to handle:

    The do() instruction enables future mul instructions.
    The don't() instruction disables future mul instructions.

Only the most recent do() or don't() instruction applies. At 
the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

This corrupted memory is similar to the example from before, but
this time the mul(5,5) and mul(11,8) instructions are disabled because
there is a don't() instruction before them. The other mul instructions
function normally, including the one at the end that gets re-enabled by
a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the
results of just the enabled multiplications?
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
    pattern_mul = r'mul\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)'
    pattern_do = r'do\(\)'
    pattern_dont = r'don\'t\(\)'

    total = 0
    mul_enabled = True

    try:
        with open(filename, 'r', encoding='us-ascii') as file:
            content = file.read()

            # Process instructions in order
            for match in re.finditer(f"{pattern_mul}|{pattern_do}|{pattern_dont}", content):
                if match.group().startswith('do()'):
                    mul_enabled = True
                elif match.group().startswith('don\'t()'):
                    mul_enabled = False
                elif match.group().startswith('mul(') and mul_enabled:
                    x, y = match.groups()
                    result = int(x) * int(y)
                    total += result
                    print(f"Found: mul({x},{y}) = {result}")

    except FileNotFoundError:
        print(f'Error: File {filename} not found.')
    except Exception as e:
        print(f'An error occurred: {e}')

    return total

def main():
    result = parse_and_calculate_mul('input.txt')
    print(f'\nTotal sum of multiplications: {result}') # result should be 90669332

if __name__ == '__main__':
    main()
