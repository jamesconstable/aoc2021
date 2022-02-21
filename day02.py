#! /usr/bin/env python

'''
Solvers and example test cases for Day 2 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/2>
'''

import sys
from typing import Iterable
import unittest


def part1(lines: Iterable[str]) -> int:
    '''Solver for Day 2, part 1'''
    horizontal = 0
    depth = 0
    for line in lines:
        command, amount_str = line.split()
        amount = int(amount_str)
        match command:
            case 'forward':
                horizontal += amount
            case 'down':
                depth += amount
            case 'up':
                depth -= amount
    return horizontal * depth


def part2(lines: Iterable[str]) -> int:
    '''Solver for Day 2, part 2'''
    horizontal = 0
    depth = 0
    aim = 0
    for line in lines:
        command, amount_str = line.split()
        amount = int(amount_str)
        match command:
            case 'forward':
                horizontal += amount
                depth += aim * amount
            case 'down':
                aim += amount
            case 'up':
                aim -= amount
    return horizontal * depth


class TestDay01(unittest.TestCase):
    '''Example test cases for Day 2, as specified in the problem description'''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            'forward 5',
            'down 5',
            'forward 8',
            'up 3',
            'down 8',
            'forward 2'
        ]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 150)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 900)


if __name__ == '__main__':
    match sys.argv[1:]:
        case ['1']:
            print(part1(sys.stdin))
        case ['2']:
            print(part2(sys.stdin))
        case _:
            print("Usage: ./day02.py <part_number> < input.txt",
                  file=sys.stderr)
