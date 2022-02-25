#! /usr/bin/env python

'''
Solvers and example test cases for Day 6 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/6>
'''

from collections import Counter, defaultdict
from typing import Dict, Mapping, Iterable
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 6, part 1
    '''
    state = simulate_lanternfish(
        Counter(int(i) for i in next(iter(lines)).strip().split(',')),
        80)
    return sum(state.values())


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 6, part 2
    '''
    state = simulate_lanternfish(
        Counter(int(i) for i in next(iter(lines)).strip().split(',')),
        256)
    return sum(state.values())


def simulate_lanternfish(init_state: Mapping[int, int], days: int) \
        -> Dict[int, int]:
    '''
    Simulates lanternfish population dynamics over the specified number of
    days. The state is specified as a dictionary mapping internal timer values
    (measured in days until reproduction) to the number of fish with that
    timer value.
    '''
    state = defaultdict(int, init_state.items())
    for _ in range(days):
        new_state = defaultdict(int)

        # Age the lanternfish that have moved into the regular 1 week cycle
        for i in range(7):
            new_state[i] = state[(i+1) % 7]

        # Hatch the new lanternfish and age those that are still immature
        for i in range(6, 9):
            new_state[i] += state[(i+1) % 9]
        state = new_state
    return state


class TestDay06(unittest.TestCase):
    '''
    Example test cases for Day 6, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = ["3,4,3,1,2"]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 5934)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 26984457539)
