#! /usr/bin/env python

'''
Solvers and example test cases for Day 9 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/9>
'''

from dataclasses import astuple, dataclass
from typing import Iterable, Sequence, Set
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 9, part 1
    '''
    heights = [[int(i) for i in line.strip()] for line in lines]
    total_risk = 0
    for y in range(len(heights)):
        for x in range(len(heights[0])):
            if is_low_point(heights, Coord(x, y)):
                total_risk += heights[y][x] + 1
    return total_risk


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 9, part 2
    '''
    heights = [[int(i) for i in line.strip()] for line in lines]
    basins = []
    for y in range(len(heights)):
        for x in range(len(heights[0])):
            if is_low_point(heights, Coord(x, y)):
                basins.append(get_basin(heights, Coord(x, y)))
    basin_sizes = sorted(len(basin) for basin in basins)
    return basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]


@dataclass(frozen=True)
class Coord:
    '''
    Represents a single (x, y) coordinate.
    '''
    x: int
    y: int


def is_low_point(heights: Sequence[Sequence[int]], coord: Coord) -> bool:
    '''
    Returns True if coord is a local minimum in heights, and False otherwise.
    '''
    x, y = astuple(coord)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= x+dx < len(heights[0]) and 0 <= y+dy < len(heights):
            if heights[y][x] >= heights[y+dy][x+dx]:
                return False
    return True


def get_basin(heights: Sequence[Sequence[int]], low_point: Coord) \
        -> Set[Coord]:
    '''
    Returns the coordinates of all cells within the basin specified by the
    given lowest point.
    '''
    basin: Set[Coord] = set()
    fringe = [low_point]
    while len(fringe) > 0:
        coord = fringe.pop()
        if coord in basin:
            continue
        basin.add(coord)
        x, y = astuple(coord)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if 0 <= x+dx < len(heights[0]) and 0 <= y+dy < len(heights):
                if heights[y][x] <= heights[y+dy][x+dx] < 9:
                    fringe.append(Coord(x+dx, y+dy))
    return basin


class TestDay09(unittest.TestCase):
    '''
    Example test cases for Day 9, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            '2199943210\n',
            '3987894921\n',
            '9856789892\n',
            '8767896789\n',
            '9899965678\n'
        ]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 15)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 1134)
