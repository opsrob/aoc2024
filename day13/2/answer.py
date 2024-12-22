#!/usr/bin/env python

"""This solution uses direct algebraic calculation of button presses with
no memory allocation or iteration to handle the large numbers efficiently.

As you go to win the first prize, you discover that the claw is nowhere near
where you expected it would be. Due to a unit conversion error in your
measurements, the position of every prize is actually 10000000000000 higher
on both the X and Y axis!
Add 10000000000000 to the X and Y position of every prize. After making this
change, the example above would now look like this:
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279

Now, it is only possible to win a prize on the second and fourth claw machines.
Unfortunately, it will take *many more than *100 presses to do so.
Using the corrected prize coordinates, figure out how to win as many prizes as
possible. What is the fewest tokens you would have to spend to win all possible
prizes?
"""

import re
from dataclasses import dataclass

@dataclass
class ClawMachine:
    """Represents a claw machine with button movements and prize location."""
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    prize_x: int
    prize_y: int

def parse_input(filename: str, offset: int = 10000000000000) -> list[ClawMachine]:
    """Parse input file and return list of claw machines."""
    machines = []
    current_machine = {}
    
    with open(filename, 'r') as f:
        for line in f:
            if match := re.match(r'Button A: X\+(\d+), Y\+(\d+)', line):
                current_machine['a_x'] = int(match.group(1))
                current_machine['a_y'] = int(match.group(2))
            elif match := re.match(r'Button B: X\+(\d+), Y\+(\d+)', line):
                current_machine['b_x'] = int(match.group(1))
                current_machine['b_y'] = int(match.group(2))
            elif match := re.match(r'Prize: X=(\d+), Y=(\d+)', line):
                current_machine['prize_x'] = int(match.group(1)) + offset
                current_machine['prize_y'] = int(match.group(2)) + offset
                machines.append(ClawMachine(**current_machine))
                current_machine = {}
    
    return machines

def find_button_presses(machine: ClawMachine):
    """Find button press combination using direct algebraic solution."""
    denominator = (machine.b_y * machine.a_x - machine.b_x * machine.a_y)
    if denominator == 0:
        return None
        
    times_b = (machine.prize_y * machine.a_x - machine.prize_x * machine.a_y) / denominator
    times_a = (machine.prize_x - machine.b_x * times_b) / machine.a_x
    
    if times_a.is_integer() and times_b.is_integer() and times_a >= 0 and times_b >= 0:
        return int(times_a), int(times_b)
    return None

def solve_puzzle(filename: str) -> int:
    """Solve the claw machine puzzle and return minimum total tokens needed."""
    machines = parse_input(filename)
    total_tokens = 0
    
    for i, machine in enumerate(machines):
        if result := find_button_presses(machine):
            total_tokens += result[0] * 3 + result[1]
            
    return total_tokens

if __name__ == '__main__':
    result = solve_puzzle('input.txt')
    print(f'Minimum tokens needed: {result}') # should be 87550094242995
