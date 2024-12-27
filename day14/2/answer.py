#!/usr/bin/env python
"""
These robots should have a hard-coded Easter egg: very rarely, most 
of the robots should arrange themselves into _a picture of a Christmas 
tree_.

_What is the fewest number of seconds that must elapse for the robots
to display the Easter egg?_
"""
import re
from typing import List
from dataclasses import dataclass
from collections import defaultdict, namedtuple

@dataclass(frozen=True)
class Point:
    """Represents a point in 2D space."""
    x: int
    y: int

# Simple namedtuple for robot data
Robot = namedtuple('Robot', ['px', 'py', 'vx', 'vy'])

def parse_input(robot_map: str) -> List[Robot]:
    """Parse the input text into a list of Robot objects."""
    bots = []
    pattern = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'

    for line in robot_map.strip().split('\n'):
        match = re.match(pattern, line)
        if match:
            px, py, vx, vy = map(int, match.groups())
            bots.append(Robot(px, py, vx, vy))

    return bots

def get_position(robot: Robot, time: int, width: int, height: int) -> Point:
    """Calculate the position of a robot after given time considering wrapping."""
    x = ((robot.px + robot.vx * time) % width + width) % width
    y = ((robot.py + robot.vy * time) % height + height) % height
    return Point(x, y)

def has_consecutive_robots(points: List[Point], required_length: int = 10) -> bool:
    """Check if there are required_length consecutive robots in any row."""
    rows = defaultdict(list)
    for p in points:
        rows[p.y].append(p.x)

    for y, x_coords in rows.items():
        x_coords.sort()
        longest = 1
        current = 1

        for i in range(1, len(x_coords)):
            if x_coords[i] == x_coords[i-1] + 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1

            if longest >= required_length:
                print(f'Found {longest} consecutive robots in row {y}')
                return True

    return False

def find_pattern(
    robot_pattern: str,
    max_time: int = 10000,
    width: int = 101,
    height: int = 103
) -> int:
    """Find the earliest time when 10 robots form a consecutive line."""
    bots = parse_input(robot_pattern)

    for t in range(max_time):
        if t % 1000 == 0:
            print(f'Checking time {t}...')

        bot_positions = [get_position(robot, t, width, height) for robot in bots]
        if has_consecutive_robots(bot_positions):
            return t

    return -1

def visualize_positions(positions_vis: List[Point], width: int, height: int) -> str:
    """Create a string visualization of robot positions."""
    grid = [['.'] * width for _ in range(height)]
    for p in positions_vis:
        if 0 <= p.x < width and 0 <= p.y < height:
            grid[p.y][p.x] = '*'
    return '\n'.join(''.join(row) for row in grid)

def run_test():
    """Run test with example input."""
    example_data = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2'''

    answer = find_pattern(example_data, max_time=100, width=11, height=7)
    print(f'Test result: Pattern found at time {answer if answer >= 0 else "not found"}')

if __name__ == '__main__':
    # Run tests first
    run_test()

    # Process actual input file
    try:
        with open('input.txt', 'r', encoding='us-ascii') as f:
            robot_data = f.read()
        result = find_pattern(robot_data)
        if result >= 0:
            print(f'\nPattern found at time: {result}')
            robots = parse_input(robot_data)
            positions = [get_position(robot, result, 101, 103) for robot in robots]
            print('\nPattern:')
            print(visualize_positions(positions, 101, 103))
        else:
            print('\nNo pattern found within time limit')
    except FileNotFoundError:
        print('input.txt not found. Please ensure the file exists.')
