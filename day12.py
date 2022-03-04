#! /usr/bin/env python

'''
Solvers and example test cases for Day 12 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/12>
'''

from collections import defaultdict
from typing import Dict, Iterable, List
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 12, part 1
    '''
    graph = read_graph(lines)
    paths = 0
    fringe = [('start', set())]
    while len(fringe) > 0:
        current, seen = fringe.pop()
        if current[0].islower():
            seen.add(current)

        if current == 'end':
            paths += 1
            continue

        for neighbour in graph[current]:
            if neighbour not in seen:
                fringe.append((neighbour, seen.copy()))

    return paths


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 12, part 2
    '''
    graph = read_graph(lines)
    paths = 0
    fringe = [('start', set(), False)]
    while len(fringe) > 0:
        current, seen, used_double = fringe.pop()
        if current[0].islower():
            seen.add(current)

        if current == 'end':
            paths += 1
            continue

        for neighbour in graph[current]:
            if neighbour not in seen:
                fringe.append((neighbour, seen.copy(), used_double))
            elif not used_double and neighbour != 'start':
                fringe.append((neighbour, seen.copy(), True))

    return paths


def read_graph(lines: Iterable[str]) -> Dict[str, List[str]]:
    '''
    Read the problem input into an adjacency list representation of the cave
    graph.
    '''
    graph = defaultdict(list)
    for line in lines:
        node1, node2 = line.strip().split('-')
        graph[node1].append(node2)
        graph[node2].append(node1)
    return graph


class TestDay12(unittest.TestCase):
    '''
    Example test cases for Day 12, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.example1 = [
            'start-A\n',
            'start-b\n',
            'A-c\n',
            'A-b\n',
            'b-d\n',
            'A-end\n',
            'b-end'
        ]

        self.example2 = [
            'dc-end\n',
            'HN-start\n',
            'start-kj\n',
            'dc-start\n',
            'dc-HN\n',
            'LN-dc\n',
            'HN-end\n',
            'kj-sa\n',
            'kj-HN\n',
            'kj-dc'
        ]

        self.example3 = [
            'fs-end\n',
            'he-DX\n',
            'fs-he\n',
            'start-DX\n',
            'pj-DX\n',
            'end-zg\n',
            'zg-sl\n',
            'zg-pj\n',
            'pj-he\n',
            'RW-he\n',
            'fs-DX\n',
            'pj-RW\n',
            'zg-RW\n',
            'start-pj\n',
            'he-WI\n',
            'zg-he\n',
            'pj-fs\n',
            'start-RW'
        ]

    def test_part1_example1(self):
        self.assertEqual(part1(self.example1), 10)

    def test_part1_example2(self):
        self.assertEqual(part1(self.example2), 19)

    def test_part1_example3(self):
        self.assertEqual(part1(self.example3), 226)

    def test_part2_example1(self):
        self.assertEqual(part2(self.example1), 36)

    def test_part2_example2(self):
        self.assertEqual(part2(self.example2), 103)

    def test_part2_example3(self):
        self.assertEqual(part2(self.example3), 3509)
