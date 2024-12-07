#!/usr/bin/env python

"""
but some young elephants were playing nearby and stole all the operators from their
calibration equations! They could finish the calibrations if only someone could
determine which test values could possibly be produced by placing any combination of
operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20

Each line represents a single equation. The test value appears before the colon on each
line; it is your job to determine whether the remaining numbers can be combined with
operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules.
Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle,
you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

    190: 10 19 has only one position that accepts an operator: between 10 and 19.
    Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
    3267: 81 40 27 has two positions for operators. Of the four possible configurations
    of the operators, two cause the right side to match the test value: 81 + 40 * 27
    and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
    292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

The engineers just need the total calibration result, which is the sum of the test values
from just the equations that could possibly be true. In the above example, the sum of
the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?
"""

def evaluate_expression(nums, operators):
    result = nums[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += nums[i + 1]
        else:  # op == '*'
            result *= nums[i + 1]
    return result

def can_solve_equation(test_value, numbers):
    if len(numbers) == 1:
        return test_value == numbers[0]

    operators = ['+', '*']
    num_spaces = len(numbers) - 1

    # Try all possible combinations of operators
    for combo in range(len(operators) ** num_spaces):
        current_ops = []
        temp_combo = combo

        # Convert number to sequence of operators
        for _ in range(num_spaces):
            current_ops.append(operators[temp_combo % len(operators)])
            temp_combo //= len(operators)

        result = evaluate_expression(numbers, current_ops)
        if result == test_value:
            return True

    return False

def solve_puzzle(input_text):
    total = 0

    for line in input_text.strip().split('\n'):
        if not line:
            continue

        test_value, nums = line.split(': ')
        test_value = int(test_value)
        numbers = [int(x) for x in nums.split()]

        if can_solve_equation(test_value, numbers):
            total += test_value

    return total

with open('input.txt') as f:
    print(f'Solution: {solve_puzzle(f.read())}') # should be 1611660863222
