#! /usr/bin/env python

'''
Solvers and example test cases for Day 13 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/13>
'''

from dataclasses import dataclass
from typing import Iterable, List, Tuple
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 13, part 1
    '''
    dots, [fold, *_] = read_input(lines)
    result = perform_fold(dots, fold)
    return len(result)


def part2(lines: Iterable[str]) -> str:
    '''
    Solver for Day 13, part 2
    '''
    dots, folds = read_input(lines)
    for fold in folds:
        dots = perform_fold(dots, fold)

    # Assemble pretty print output.
    lines = []
    for y in range(-1, 6):
        line = []
        for x in range(-1, 5*8):
            line.append('██' if Coord(x, y) in dots else '  ')
        lines.append(''.join(line))

    return '\n'.join(lines)


@dataclass(frozen=True)
class Coord:
    '''
    Represents a single (x, y) coordinate.
    '''
    x: int
    y: int


def perform_fold(dots: List[Coord], fold: Tuple[str, int]) -> List[Coord]:
    '''
    Returns the result of folding dots along the axis specified by fold.
    Duplicate dots and dots along the fold axis are removed.
    '''
    axis, threshold = fold
    dot_set = set()
    for dot in dots:
        if axis == 'y':
            if dot.y > threshold:
                dot_set.add(Coord(dot.x, threshold - (dot.y - threshold)))
            elif dot.y < threshold:
                dot_set.add(dot)
        else:
            if dot.x > threshold:
                dot_set.add(Coord(threshold - (dot.x - threshold), dot.y))
            elif dot.x < threshold:
                dot_set.add(dot)
        dots = list(dot_set)
    return dots


def read_input(lines: Iterable[str]) \
        -> Tuple[List[Coord], List[Tuple[str, int]]]:
    '''
    Parses the problem input into a list of dot coordinates and fold
    instructions.
    '''
    dots = []
    lines_iter = iter(lines)
    for line in lines_iter:
        line = line.strip()
        if len(line) == 0:
            break
        x, y = line.split(',')
        dots.append(Coord(int(x), int(y)))

    folds = []
    for line in lines_iter:
        _, _, fold = line.strip().split()
        axis, value = fold.split('=')
        folds.append((axis, int(value)))

    return dots, folds


class TestDay13(unittest.TestCase):
    '''
    Example test cases for Day 13, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            '6,10\n',
            '0,14\n',
            '9,10\n',
            '0,3\n',
            '10,4\n',
            '4,11\n',
            '6,0\n',
            '6,12\n',
            '4,1\n',
            '0,13\n',
            '10,12\n',
            '3,4\n',
            '3,0\n',
            '8,4\n',
            '1,10\n',
            '2,14\n',
            '8,10\n',
            '9,0\n',
            '\n',
            'fold along y=7\n',
            'fold along x=5'
        ]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 17)

    def test_part2_example(self):
        expected = '\n'.join(line.ljust(82) for line in [
            '              ',
            '  ██████████  ',
            '  ██      ██  ',
            '  ██      ██  ',
            '  ██      ██  ',
            '  ██████████  ',
            '              '])
        self.assertEqual(part2(self.data), expected)
