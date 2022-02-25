#! /usr/bin/env python

'''
Solvers and example test cases for Day 7 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/7>
'''

from typing import Callable, Iterable, List
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 7, part 1
    '''
    positions = [int(i) for i in next(iter(lines)).strip().split(',')]
    return min_fuel_needed(positions, lambda x, y: abs(x - y))


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 7, part 2
    '''
    positions = [int(i) for i in next(iter(lines)).strip().split(',')]
    return min_fuel_needed(positions, lambda x, y: triangle(abs(x - y)))


def min_fuel_needed(positions: List[int],
                    fuel_usage: Callable[[int, int], int]) -> int:
    '''
    Given a list of crab positions and a callable that computes the amount of
    fuel needed to travel between two points, returns the minimum amount of
    fuel required to move all the crabs to the same position.
    '''
    best = float('inf')
    for i in range(min(positions), max(positions)+1):
        total = 0
        for j in positions:
            total += fuel_usage(i, j)
        if total < best:
            best = total
    return int(best)


def triangle(n: int) -> int:
    '''
    Calculates the nth triangular number.
    '''
    return (n * (n + 1)) // 2


class TestDay07(unittest.TestCase):
    '''
    Example test cases for Day 7, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = ['16,1,2,0,4,2,7,1,2,14']

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 37)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 168)
