#! /usr/bin/env python

'''
Solvers and example test cases for Day 5 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/5>
'''

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, List, Tuple
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 5, part 1
    '''
    vents = parse_input(lines)
    vent_points: Counter = Counter()
    for (start, end) in vents:
        if start.x == end.x or start.y == end.y:
            vent_points.update(points_between(start, end))
    return sum(1 for (_, count) in vent_points.most_common() if count >= 2)


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 5, part 2
    '''
    vents = parse_input(lines)
    vent_points: Counter = Counter()
    for (start, end) in vents:
        vent_points.update(points_between(start, end))
    return sum(1 for (_, count) in vent_points.most_common() if count >= 2)


@dataclass(frozen=True)
class Point:
    '''
    Represents a single (x, y) coordinate.
    '''
    x: int
    y: int


def points_between(start: Point, end: Point) -> Iterable[Point]:
    '''
    Iterates over the integral points between start and end (inclusive). Line
    must be either vertical, horizontal, or 45 degrees.
    '''
    x_step = sign(end.x - start.x)
    y_step = sign(end.y - start.y)
    x = start.x
    y = start.y
    while x != end.x or y != end.y:
        yield Point(x, y)
        x += x_step
        y += y_step
    yield Point(x, y)


def sign(value: int) -> int:
    '''
    Returns the sign of value, i.e. 1 if value is positive, -1 if value is
    negative, or 0 if value is zero.
    '''
    if value < 0:
        return -1
    if value == 0:
        return 0
    return 1


def parse_input(lines: Iterable[str]) -> List[Tuple[Point, Point]]:
    '''
    Parses the problem input and returns a list of (Point, Point) tuples
    describing the vents.
    '''
    vents = []
    for line in lines:
        start, _, end = line.split()
        p1_x, p1_y = start.split(',')
        p2_x, p2_y = end.split(',')
        vents.append((Point(int(p1_x), int(p1_y)),
                      Point(int(p2_x), int(p2_y))))
    return vents


class TestDay05(unittest.TestCase):
    '''
    Example test cases for Day 5, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            '0,9 -> 5,9',
            '8,0 -> 0,8',
            '9,4 -> 3,4',
            '2,2 -> 2,1',
            '7,0 -> 7,4',
            '6,4 -> 2,0',
            '0,9 -> 2,9',
            '3,4 -> 1,4',
            '0,0 -> 8,8',
            '5,5 -> 8,2']

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 5)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 12)
