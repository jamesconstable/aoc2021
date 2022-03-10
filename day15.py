#! /usr/bin/env python

'''
Solvers and example test cases for Day 15 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/15>
'''

from dataclasses import dataclass
import heapq
from typing import Iterable, List
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 15, part 1
    '''
    risk_map = [[int(c) for c in line.strip()] for line in lines]
    destination = Coord(len(risk_map) - 1, len(risk_map) - 1)
    return lowest_risk_path(Coord(0, 0), destination, risk_map)


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 15, part 2
    '''
    risk_map = expand_map([[int(c) for c in line.strip()] for line in lines])
    destination = Coord(len(risk_map) - 1, len(risk_map) - 1)
    return lowest_risk_path(Coord(0, 0), destination, risk_map)


@dataclass(frozen=True, order=True)
class Coord:
    '''
    Represents an (x, y) coordinate within the risk map.
    '''
    x: int
    y: int


def lowest_risk_path(
        start: Coord, end: Coord, risk_map: List[List[int]]) -> int:
    '''
    Returns the risk value of the least risky path from `start` to `end` within
    the given `risk_map`.
    '''
    fringe = [(0, start)]
    seen = set()
    while len(fringe) > 0:
        risk, current = heapq.heappop(fringe)
        if current == end:
            return risk

        if current in seen:
            continue
        seen.add(current)

        for neighbour in neighbours(current, risk_map):
            if neighbour in seen:
                continue
            heapq.heappush(
                fringe,
                (risk + risk_map[neighbour.y][neighbour.x], neighbour))

    raise RuntimeError(f"Couldn't find path from {start} to {end}")


def neighbours(coord: Coord, risk_map: List[List[int]]) -> Iterable[Coord]:
    '''
    Returns an iterator over the coordinates neighbouring `coord` within
    `risk_map`.
    '''
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= coord.x + dx < len(risk_map[0]) \
                and 0 <= coord.y + dy < len(risk_map):
            yield Coord(coord.x + dx, coord.y + dy)


def expand_map(risk_map: List[List[int]]) -> List[List[int]]:
    '''
    Given an n×n risk map, returns its 5n×5n expanded version as described in
    Part 2.
    '''
    full_map = []
    for row_tile in range(5):
        for row in risk_map:
            current_row = []
            for col_tile in range(5):
                for value in row:
                    new_risk = value + row_tile + col_tile
                    if new_risk > 9:
                        new_risk -= 9
                    current_row.append(new_risk)
            full_map.append(current_row)
    return full_map


class TestDay15(unittest.TestCase):
    '''
    Example test cases for Day 15, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            '1163751742\n',
            '1381373672\n',
            '2136511328\n',
            '3694931569\n',
            '7463417111\n',
            '1319128137\n',
            '1359912421\n',
            '3125421639\n',
            '1293138521\n',
            '2311944581'
        ]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 40)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 315)
