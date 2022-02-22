#! /usr/bin/env python

'''
Solvers and example test cases for Day 3 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/3>
'''

from collections import Counter
import sys
from typing import Iterable, List, Sequence, Tuple, TypeVar
import unittest


def part1(lines: Iterable[str]) -> int:
    '''Solver for Day 3, part 1'''
    data = list(line.strip() for line in lines)
    gamma = 0
    mask = 0
    for i in range(len(data[0])):
        count_1s = sum(int(row[i]) for row in data)
        gamma = gamma << 1 | (1 if count_1s > len(data) / 2 else 0)
        mask = mask << 1 | 1

    epsilon = gamma ^ mask    # Invert the bits in gamma to obtain epsilon
    return gamma * epsilon


def part2(lines: Iterable[str]) -> int:
    '''Solver for Day 3, part 2'''
    data: List[str] = [line.strip() for line in lines]

    # Filter for the oxygen generator rating
    filtered: List[str] = data[:]
    for i in range(len(filtered[0])):
        if len(filtered) == 1:
            break
        match ranked_frequency_at(i, filtered):
            case [(_, freq1), (_, freq2)] if freq1 == freq2:
                filtered = [row for row in filtered if row[i] == '1']
            case [(most_common, _), *_]:
                filtered = [row for row in filtered if row[i] == most_common]
    oxygen_generator_rating = int(filtered[0], base=2)

    # Filter for the CO2 scrubber rating
    filtered = data[:]
    for i in range(len(filtered[0])):
        if len(filtered) == 1:
            break
        match ranked_frequency_at(i, filtered):
            case [(_, freq1), (_, freq2)] if freq1 == freq2:
                filtered = [row for row in filtered if row[i] == '0']
            case [*_, (least_common, _)]:
                filtered = [row for row in filtered if row[i] == least_common]
    co2_scrubber_rating = int(filtered[0], base=2)

    return oxygen_generator_rating * co2_scrubber_rating


Item = TypeVar('Item')


def ranked_frequency_at(i: int, data: Sequence[Sequence[Item]]) \
        -> List[Tuple[Item, int]]:
    '''
    Given a column index and a 2D grid of items, returns a list of tuples
    containing just the unique items in that column and the number of times
    they appear, sorted from most to least frequent.
    '''
    return Counter(row[i] for row in data).most_common()


class TestDay03(unittest.TestCase):
    '''Example test cases for Day 3, as specified in the problem description'''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = (("00100 11110 10110 10111 10101 01111 "
                      "00111 11100 10000 11001 00010 01010")
                     .replace(' ', '\n ')
                     .split(' '))

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 198)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 230)


if __name__ == '__main__':
    match sys.argv[1:]:
        case ['1']:
            print(part1(sys.stdin))
        case ['2']:
            print(part2(sys.stdin))
        case _:
            print("Usage: ./day03.py <part_number> < input.txt",
                  file=sys.stderr)
