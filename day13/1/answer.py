#!/usr/bin/env python
"""
The claw machines here are a little unusual. Instead of a joystick
or directional buttons to control the claw, these machines have two
buttons labeled `A` and `B`. Worse, you can't just put in a token
and play; it costs _3 tokens_ to push the `A` button and _1 token_
to push the `B` button.

With a little experimentation, you figure out that each machine's 
buttons are configured to move the claw a specific amount to the _right_
(along the `X` axis) and a specific amount _forward_ (along the `Y`
axis) each time that button is pressed.

Each machine contains one _prize_; to win the prize, the claw must be
positioned _exactly_ above the prize on both the `X` and `Y` axes.

You wonder: what is the smallest number of tokens you would have to
spend to win as many prizes as possible? You assemble a list of every
machine's button behavior and prize location (your puzzle input). For
example:

```
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
```

This list describes the button configuration and prize location of
four different claw machines.

For now, consider just the first claw machine in the list:

- Pushing the machine's `A` button would move the claw `94` units along
the `X` axis and `34` units along the `Y` axis.
- Pushing the `B` button would move the claw `22` units along the `X`
axis and `67` units along the `Y` axis.
- The prize is located at `X=8400`, `Y=5400`; this means that from the claw's
initial position, it would need to move exactly `8400` units along the `X`
axis and exactly `5400` units along the `Y` axis to be perfectly aligned with
the prize in this machine.

The cheapest way to win the prize is by pushing the `A` button `80` times and
the `B` button `40` times. This would line up the claw along the `X` axis
(because `80*94 + 40*22 = 8400`) and along the `Y` axis 
(because `80*34 +40*67 = 5400`). Doing this would cost `80*3` tokens for the 
`A` presses and `40*1` for the `B` presses, a total of `_280_` tokens.

For the second and fourth claw machines, there is no combination of A and B
presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing
the `A` button `38` times and the `B` button `86` times. Doing this would cost
a total of `_200_` tokens.

So, the most prizes you could possibly win is two; the minimum tokens you
would have to spend to win all (two) prizes is `_480_`.

You estimate that each button would need to be pressed _no more than `100`
times_ to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. _What is the fewest tokens
you would have to spend to win all possible prizes?_
"""

import re
from dataclasses import dataclass
from typing import Optional, Tuple
from itertools import product

@dataclass
class ClawMachine:
    """Represents a claw machine with button movements and prize location."""
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    prize_x: int
    prize_y: int

def parse_input(filename: str) -> list[ClawMachine]:
    """Parse input file and return list of claw machines."""
    machines = []
    current_machine = {}

    with open(filename, 'r', encoding='us-ascii') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if match := re.match(r'Button A: X\+(\d+), Y\+(\d+)', line):
                current_machine['a_x'] = int(match.group(1))
                current_machine['a_y'] = int(match.group(2))
            elif match := re.match(r'Button B: X\+(\d+), Y\+(\d+)', line):
                current_machine['b_x'] = int(match.group(1))
                current_machine['b_y'] = int(match.group(2))
            elif match := re.match(r'Prize: X=(\d+), Y=(\d+)', line):
                current_machine['prize_x'] = int(match.group(1))
                current_machine['prize_y'] = int(match.group(2))
                machines.append(ClawMachine(**current_machine))
                current_machine = {}

    return machines

def find_button_presses(machine: ClawMachine, max_presses: int = 100) -> Optional[Tuple[int, int]]:
    """
    Find minimum button press combination to win prize.
    Returns (a_presses, b_presses) if solution exists, None otherwise.
    """
    # Generate all possible combinations of button presses
    combinations = product(range(max_presses + 1), repeat=2)

    # Find valid combinations that reach the prize
    valid_combinations = [
        (a, b) for a, b in combinations
        if (a * machine.a_x + b * machine.b_x == machine.prize_x and
            a * machine.a_y + b * machine.b_y == machine.prize_y)
    ]

    if not valid_combinations:
        return None

    # Find combination with minimum token cost
    return min(valid_combinations, key=lambda x: 3 * x[0] + x[1])

def calculate_tokens(a_presses: int, b_presses: int) -> int:
    """Calculate total tokens needed for given button presses."""
    return a_presses * 3 + b_presses

def solve_puzzle(filename: str) -> int:
    """
    Solve the claw machine puzzle and return minimum total tokens needed.
    """
    machines = parse_input(filename)
    total_tokens = 0

    for i, machine in enumerate(machines):
        result = find_button_presses(machine)
        if result:
            a_presses, b_presses = result
            tokens = calculate_tokens(a_presses, b_presses)
            total_tokens += tokens

    return total_tokens

if __name__ == '__main__':
    result = solve_puzzle('input.txt')
    print(f'Minimum tokens needed: {result}') # should be 37680
