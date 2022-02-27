#! /usr/bin/env python

'''
Solvers and example test cases for Day 8 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/8>
'''

import itertools
from typing import Dict, Iterable, List, Optional, Sequence
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 8, part 1
    '''
    total = 0
    for line in lines:
        outputs = line.strip().split(' | ')[1].split()
        unique_digits = [i for i in outputs if len(i) in [2, 4, 3, 7]]
        total += len(unique_digits)
    return total


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 8, part 2
    '''
    total = 0
    for line in lines:
        inputs_str, outputs_str = line.strip().split(' | ')
        inputs = [sorted(i) for i in inputs_str.split()]
        outputs = [sorted(i) for i in outputs_str.split()]
        mapping = find_mapping(inputs, list(canonical.keys()))
        value = 0
        for output in outputs:
            value *= 10
            value += canonical[''.join(sorted(mapping[i] for i in output))]
        total += value
    return total


canonical = {
    'abcefg':  0,
    'cf':      1,
    'acdeg':   2,
    'acdfg':   3,
    'bcdf':    4,
    'abdfg':   5,
    'abdefg':  6,
    'acf':     7,
    'abcdefg': 8,
    'abcdfg':  9
}


def find_mapping(given: Sequence[Sequence[str]],
                 target: Sequence[Sequence[str]]) \
        -> Dict[str, str]:
    '''
    Attempts to find a mapping from the string sequences in given to the string
    sequences in target, and returns the satisfying mapping. If more than one
    mapping is possible, only the first one found will be returned. Raises a
    ValueError if given and target are not isomorphic.
    '''
    given = sorted(given, key=len)
    target = sorted(target, key=len)
    if (result := _find_mapping(given, target, {})) is not None:
        return result
    raise ValueError('No consistent mapping is possible for the given input')


def _find_mapping(given: List[Sequence[str]],
                  target: List[Sequence[str]],
                  mapping: Dict[str, str]) \
        -> Optional[Dict[str, str]]:
    '''
    Recursive helper function for find_mapping. For best performance, given and
    target should have their elements sorted by length prior to calling.
    '''
    # Base case: if every word has already been matched to a target, then the
    # mapping is complete.
    if len(given) == len(target) == 0:
        return mapping

    for i, candidate in enumerate(target):
        # A valid candidate must be the same length as the input.
        if len(candidate) != len(given[0]):
            continue

        # A valid candidate mustn't conflict in any way with the bindings that
        # have already been made.
        success = True
        for letter in given[0]:
            if letter in mapping and mapping[letter] not in candidate:
                success = False
                break
        if not success:
            continue

        unmapped_given = set(given[0]) - set(mapping.keys())
        unmapped_candidate = set(candidate) - set(mapping.values())

        # Try every matching of unmapped letters in turn to see if any permit a
        # fully consistent mapping for the rest of the input.
        for permutation in itertools.permutations(unmapped_candidate):
            new_mapping = mapping.copy()
            new_mapping.update(zip(unmapped_given, permutation))
            result = _find_mapping(given[1:], target[:i] + target[i+1:],
                                   new_mapping)
            if result is not None:
                # A complete mapping has been found!
                return result

    # No complete mapping could be built from this starting point
    return None


class TestDay08(unittest.TestCase):
    '''
    Example test cases for Day 8, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | '
            'fdgacbe cefdb cefbgd gcbe',
            'edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | '
            'fcgedb cgb dgebacf gc',
            'fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | '
            'cg cg fdcagb cbg',
            'fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | '
            'efabcd cedba gadfec cb',
            'aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | '
            'gecf egdcabf bgf bfgea',
            'fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | '
            'gebdcfa ecba ca fadegcb',
            'dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | '
            'cefg dcbef fcge gbcadfe',
            'bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | '
            'ed bcgafe cdgba cbgef',
            'egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | '
            'gbdfcae bgc cg cgb',
            'gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | '
            'fgae cfgab fg bagce'
        ]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 26)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 61229)
