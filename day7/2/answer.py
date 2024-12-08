#!/usr/bin/env python

"""
Just then, you spot your mistake: some well-hidden elephants are holding a 
hird type of operator.

The concatenation operator (||) combines the digits from its left and right
inputs into a single number. For example, 12 || 345 would become 12345. All
operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition
and multiplication, the above example has three more equations that can be
made true by inserting operators:

    156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
    7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
    192: 17 8 14 can be made true using 17 || 8 + 14.

Adding up all six test values (the three that could be made before using only +
and * plus the new three that can now be made by also using ||) produces the new
total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations
could possibly be true. What is their total calibration result?
"""

def evaluate_expression(nums, operators):
    result = nums[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += nums[i + 1]
        elif op == '*':
            result *= nums[i + 1]
        else:  # op == '||'
            result = int(str(result) + str(nums[i + 1]))
    return result

def can_solve_equation(test_value, numbers):
    if len(numbers) == 1:
        return test_value == numbers[0]
    
    operators = ['+', '*', '||']
    num_spaces = len(numbers) - 1
    
    for combo in range(len(operators) ** num_spaces):
        current_ops = []
        temp_combo = combo
        
        for _ in range(num_spaces):
            current_ops.append(operators[temp_combo % len(operators)])
            temp_combo //= len(operators)
            
        try:
            result = evaluate_expression(numbers, current_ops)
            if result == test_value:
                return True
        except:
            continue            
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

# Verify example
example = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

print(f"Example solution: {solve_puzzle(example)}")  # Should print 11387

with open('input.txt') as f:
    print(f"Solution: {solve_puzzle(f.read())}") # Should be 945341732469724
