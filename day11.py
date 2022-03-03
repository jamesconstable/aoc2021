#! /usr/bin/env python

'''
Solvers and example test cases for Day 11 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/11>
'''

from typing import Iterable, List, Tuple
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 11, part 1
    '''
    grid = [[int(char) for char in line.strip()] for line in lines]
    total_flashes = 0
    for _ in range(100):
        grid, flashes = simulate_octopuses(grid)
        total_flashes += flashes
    return total_flashes


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 11, part 2
    '''
    grid = [[int(char) for char in line.strip()] for line in lines]
    step = 1
    while True:
        grid, flashes = simulate_octopuses(grid)
        if flashes == len(grid) * len(grid[0]):
            return step
        step += 1


NEIGHBOUR_OFFSETS = [
    (-1, -1), (-1,  0), (-1,  1),
    ( 0, -1),           ( 0,  1),  # noqa: E201
    ( 1, -1), ( 1,  0), ( 1,  1)   # noqa: E201
]


def simulate_octopuses(grid: List[List[int]]) -> Tuple[List[List[int]], int]:
    '''
    Executes one step of the Dumbo octopus simulation, returning the updated
    grid and the number of octopuses that flashed in that timestep.
    '''
    needs_flash = []
    for y, row in enumerate(grid):
        for x in range(len(row)):
            grid[y][x] += 1
            if grid[y][x] > 9:
                needs_flash.append((x, y))

    flashed = set()
    while len(needs_flash) > 0:
        x, y = needs_flash.pop()
        if (x, y) in flashed:
            continue
        grid[y][x] = 0
        flashed.add((x, y))
        for dx, dy in NEIGHBOUR_OFFSETS:
            if 0 <= x+dx < len(grid[0]) and 0 <= y+dy < len(grid) \
                    and (x+dx, y+dy) not in flashed:
                grid[y+dy][x+dx] += 1
                if grid[y+dy][x+dx] > 9:
                    needs_flash.append((x+dx, y+dy))

    return grid, len(flashed)


class TestDay11(unittest.TestCase):
    '''
    Example test cases for Day 11, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            '5483143223\n',
            '2745854711\n',
            '5264556173\n',
            '6141336146\n',
            '6357385478\n',
            '4167524645\n',
            '2176841721\n',
            '6882881134\n',
            '4846848554\n',
            '5283751526'
        ]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 1656)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 195)
