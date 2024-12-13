#!/usr/bin/env python

"""
Upon completion, two things immediately become clear. First, the disk
definitely has a lot more contiguous free space, just like the amphipod
hoped. Second, the computer is running much more slowly! Maybe introducing
all of that file system fragmentation was a bad idea?

The eager amphipod already has a new plan: rather than move individual blocks,
he'd like to try compacting the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space
blocks that could fit the file. Attempt to move each file exactly once in order
of decreasing file ID number starting with the file with the highest file ID
number. If there is no span of free space to the left of a file that is large 
nough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..

The process of updating the filesystem checksum is the same; now, this example's
checksum would be 2858.

Start over, now compacting the amphipod's hard drive using this new method instead.
What is the resulting filesystem checksum?
"""

### Claude and I struggled with day9. Part two was a rewrite.

from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Segment:
    '''Represents a contiguous disk segment'''
    pos: int
    size: int

class Diskmap:
    '''Represents disk block allocation'''
    def __init__(self, text: str):
        self.file = defaultdict(list)
        self.empty = []
        pos = 0
        
        for i in range(len(text) // 2):
            blocks = int(text[2*i])
            empty = int(text[2*i+1])
            self.file[i].append(Segment(pos, blocks))
            pos += blocks
            if empty:
                self.empty.append(Segment(pos, empty))
                pos += empty
        blocks = int(text[-1])
        self.file[i+1] = [Segment(pos, blocks)]
        self.empty.reverse()
    
    def allocate_one(self, need: int, block_max: int = 0):
        '''Find single contiguous allocation space'''
        for i in range(len(self.empty) - 1, -1, -1):
            seg = self.empty[i]
            if block_max and seg.pos > block_max:
                return None, need
            if seg.size < need:
                continue
            
            result = Segment(seg.pos, need)
            if seg.size == need:
                self.empty = self.empty[:i] + self.empty[i+1:]
            else:
                self.empty[i] = Segment(seg.pos + need, seg.size - need)
            return result, 0
        return None, need
    
    def checksum(self):
        '''Calculate filesystem checksum'''
        result = 0
        for fileno, segs in self.file.items():
            for seg in segs:
                result += fileno * sum(range(seg.pos, seg.pos + seg.size))
        return result

def solve_part2(text: str):
    '''Solve part 2 - move whole files to earliest possible position'''
    diskmap = Diskmap(text)
    
    for fileno, file_segs in sorted(diskmap.file.items(), reverse=True):
        file_seg = file_segs[0]
        seg, left = diskmap.allocate_one(file_seg.size, block_max=file_seg.pos)
        if left == 0:
            diskmap.file[fileno] = [seg]
            
    return diskmap.checksum()

def test():
    '''Test with example input'''
    example = '2333133121414131402'
    result = solve_part2(example)
    assert result == 2858, f'Expected 2858, got {result}'
    print('Test passed!')

test()

with open('input.txt') as f:
    text = f.read().strip()
    print(f'Solution: {solve_part2(text)}') # should be 6227018762750