#!/usr/bin/env python

"""
While the Elves get to work printing the correctly-ordered updates, you have a
little time to fix the rest of them.

For each of the incorrectly-ordered updates, use the page ordering rules to put
the page numbers in the right order. For the above example, here are the three
incorrectly-ordered updates and their correct orderings:

    75,97,47,61,53 becomes 97,75,47,61,53.
    61,13,29 becomes 61,29,13.
    97,13,75,29,47 becomes 97,75,47,29,13.

After taking only the incorrectly-ordered updates and ordering them correctly, their
middle page numbers are 47, 29, and 47. Adding these together produces 123.

Find the updates which are not in the correct order. What do you get if you add up
the middle page numbers after correctly ordering just those updates?
"""

from collections import defaultdict, deque

def parse_input(text):
    """parse the two sections of the input file into rules and updates"""
    rules_section, updates_section = text.strip().split('\n\n')
    rules = set(tuple(map(int, line.split('|'))) for line in rules_section.split('\n'))
    updates = [list(map(int, line.split(','))) for line in updates_section.split('\n') if line]
    return rules, updates

def is_valid_order(pages, rules):
    """determine if order is valid"""
    return all(pages.index(before) < pages.index(after) 
              for before, after in rules 
              if before in pages and after in pages)

def topological_sort(pages, rules):
    """make it real with topological sorting of directed acyclic graph"""
    # Build adjacency list and in-degree count
    graph = defaultdict(set)
    in_degree = defaultdict(int)

    # Only consider rules where both pages are in the update
    for before, after in rules:
        if before in pages and after in pages:
            graph[before].add(after)
            in_degree[after] += 1
            # Ensure all pages are in in_degree dict
            in_degree.setdefault(before, 0)

    # Initialize queue with nodes having no dependencies
    queue = deque([page for page in pages if in_degree[page] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result

def get_middle_page(pages):
    """get the middle page"""
    return pages[len(pages) // 2]

def solve_part2(input_text):
    """solve the puzzle"""
    rules, updates = parse_input(input_text)

    middle_sum = 0
    for update in updates:
        if not is_valid_order(update, rules):
            correct_order = topological_sort(update, rules)
            middle_sum += get_middle_page(correct_order)

    return middle_sum

def main(filename):
    with open(filename) as f:
        result = solve_part2(f.read())
    print(f'Sum of middle pages from reordered incorrect updates: {result}') # should be 5346

if __name__ == '__main__':
    import sys
    main('input.txt')
