#!/usr/bin/env python
"""
Despite the narrative, the order doesn't matter, only the count
matters. This is handy because tracking the order cause oom errors.

_How many stones will you have after blinking 75 times?_
"""

from collections import Counter

def transform_counts(counts: Counter) -> Counter:
    '''Transform stone counts according to rules'''
    new_counts = Counter()
    for num, count in counts.items():
        if num == 0:
            new_counts[1] += count
        elif len(str(num)) % 2 == 0:
            s = str(num)
            mid = len(s) // 2
            left, right = int(s[:mid]), int(s[mid:])
            new_counts[left] += count
            new_counts[right] += count
        else:
            new_counts[num * 2024] += count
    return new_counts

def solve(input_file: str = 'input.txt') -> int:
    with open(input_file) as f:
        stones = [int(x) for x in f.read().strip().split()]
    
    counts = Counter(stones)
    for _ in range(75):
        counts = transform_counts(counts)
    return sum(counts.values())

if __name__ == '__main__':
    print(solve()) # should be 240884656550923