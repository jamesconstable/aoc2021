#! /usr/bin/env python

import collections
import sys

def part1():
    count = 0
    last = float('inf')
    for line in sys.stdin:
        if int(line) > last:
            count += 1
        last = int(line)
    return count

def part2():
    count = 0
    last = float('inf')
    window = collections.deque([], maxlen=3)
    for line in sys.stdin:
        window.append(int(line))
        if len(window) == 3:
            s = sum(window)
            if s > last:
                count += 1
            last = s
    return count

if __name__ == '__main__':
    match sys.argv[1:]:
        case ['1']:
            print(part1())
        case ['2']:
            print(part2())
        case _:
            print("Usage: ./day01.py <part_number> < input.txt",
                    file=sys.stderr)
