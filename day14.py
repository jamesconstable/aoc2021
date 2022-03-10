#! /usr/bin/env python

'''
Solvers and example test cases for Day 14 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/14>
'''

from collections import defaultdict
from itertools import pairwise
from typing import Dict, Iterable, List, Tuple
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 14, part 1
    '''
    template_str, insertion_rules = read_input(lines)
    counts = element_count_after(10, list(template_str), insertion_rules)
    return counts[0][1] - counts[-1][1]


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 14, part 2
    '''
    template_str, insertion_rules = read_input(lines)
    counts = element_count_after(40, list(template_str), insertion_rules)
    return counts[0][1] - counts[-1][1]


def element_count_after(
        iterations: int,
        template: List[str],
        rules: Dict[Tuple[str, str], str]) \
        -> List[Tuple[str, int]]:
    '''
    Computes the number of units of each element required to apply `rules` to
    `template` `iterations` times. The returned element-count list is sorted
    from most to least common.
    '''
    # The exact order of elements in the polymer doesn't matter, so rather than
    # generate the full sequence on each iteration (which would grow
    # exponentially), we'll just track how many of each pair it contains.
    pair_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    for pair in pairwise(template):
        pair_counts[pair] += 1

    for _ in range(iterations):
        new_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        for pair, count in pair_counts.items():
            new_counts[(pair[0], rules[pair])] += count
            new_counts[(rules[pair], pair[1])] += count
        pair_counts = new_counts

    # Count the number of each unit type appearing in the resulting polymer.
    # Because we're tracking pairs and not individual units, every unit is
    # double-counted, except for the first and last which only appear in one
    # pair each. Initialise both of these to one to compensate.
    unit_counts: Dict[str, int] = defaultdict(int)
    unit_counts[template[0]] += 1
    unit_counts[template[-1]] += 1
    for pair, count in pair_counts.items():
        unit_counts[pair[0]] += count
        unit_counts[pair[1]] += count
    counts_list = [(unit, count // 2) for unit, count in unit_counts.items()]
    counts_list.sort(key=lambda x: -x[1])
    return counts_list


def read_input(lines: Iterable[str]) -> Tuple[str, Dict[Tuple[str, str], str]]:
    '''
    Parses the problem input and returns a tuple containing the initial
    template and a dictionary of the insertion rules.
    '''
    lines_iter = iter(lines)
    template = next(lines_iter).strip()
    next(lines_iter)  # Skip blank line between template and insertion rules

    insertion_rules = {}
    for line in lines_iter:
        pair, insertion = line.strip().split(' -> ')
        insertion_rules[(pair[0], pair[1])] = insertion

    return template, insertion_rules


class TestDay14(unittest.TestCase):
    '''
    Example test cases for Day 14, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            'NNCB\n',
            '\n',
            'CH -> B\n',
            'HH -> N\n',
            'CB -> H\n',
            'NH -> C\n',
            'HB -> C\n',
            'HC -> B\n',
            'HN -> C\n',
            'NN -> C\n',
            'BH -> H\n',
            'NC -> B\n',
            'NB -> B\n',
            'BN -> B\n',
            'BB -> N\n',
            'BC -> B\n',
            'CC -> N\n',
            'CN -> C'
        ]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 1588)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 2188189693529)
