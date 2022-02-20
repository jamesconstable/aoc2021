#! /usr/bin/env python

"""
Solvers and example test cases for Day 1 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/1>
"""

from collections import deque
import sys
from typing import Iterable
import unittest


def part1(lines: Iterable[str]) -> int:
    """Solver for Day 1, part 1"""
    count = 0
    last = None
    for line in lines:
        current = int(line)
        if last is not None and current > last:
            count += 1
        last = current
    return count


def part2(lines: Iterable[str]) -> int:
    """Solver for Day 1, part 2"""
    count = 0
    window: deque = deque([], maxlen=3)
    last = None
    for line in lines:
        window.append(int(line))
        if len(window) == 3:
            current = sum(window)
            if last is not None and current > last:
                count += 1
            last = current
    return count


class TestDay01(unittest.TestCase):
    """Example test cases for Day 1, as specified in the problem description"""
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = "199 200 208 210 200 207 240 269 260 263".split()

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 7)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 5)


if __name__ == '__main__':
    match sys.argv[1:]:
        case ['1']:
            print(part1(sys.stdin))
        case ['2']:
            print(part2(sys.stdin))
        case _:
            print("Usage: ./day01.py <part_number> < input.txt",
                  file=sys.stderr)
