#! /usr/bin/env python

'''
Solvers and example test cases for Day 10 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/10>
'''

from typing import Iterable, Optional
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 10, part 1
    '''
    score = 0
    for line in lines:
        score += corruption_score(line)
    return score


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 10, part 2
    '''
    scores = []
    for line in lines:
        if (score := autocomplete_score(line)) is not None:
            scores.append(score)

    # Return the median score.
    scores.sort()
    return scores[len(scores) // 2]


def corruption_score(line: str) -> int:
    '''
    Computes the corruption score for line. A non-corrupted line will receive
    a score of 0, even if it is incomplete.
    '''
    stack = []
    for char in line.strip():
        match char:
            case '(' | '[' | '{' | '<':
                stack.append(char)
            case ')':
                if stack.pop() != '(':
                    return 3
            case ']':
                if stack.pop() != '[':
                    return 57
            case '}':
                if stack.pop() != '{':
                    return 1197
            case '>':
                if stack.pop() != '<':
                    return 25137
    return 0


def autocomplete_score(line: str) -> Optional[int]:
    '''
    Computes the autocomplete score for line. If the line is corrupted, None
    will be returned.
    '''
    if corruption_score(line) > 0:
        return None

    stack = []
    for char in line.strip():
        if char in '([{<':
            stack.append(char)
        else:
            stack.pop()

    score = 0
    while len(stack) > 0:
        score *= 5
        match stack.pop():
            case '(':
                score += 1
            case '[':
                score += 2
            case '{':
                score += 3
            case '<':
                score += 4
    return score


class TestDay10(unittest.TestCase):
    '''
    Example test cases for Day 10, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            '[({(<(())[]>[[{[]{<()<>>\n',
            '[(()[<>])]({[<{<<[]>>(\n',
            '{([(<{}[<>[]}>{[]{[(<()>\n',
            '(((({<>}<{<{<>}{[]{[]{}\n',
            '[[<[([]))<([[{}[[()]]]\n',
            '[{[{({}]{}}([{[{{{}}([]\n',
            '{<[[]]>}<{[{[{[]{()[[[]\n',
            '[<(<(<(<{}))><([]([]()\n',
            '<{([([[(<>()){}]>(<<{{\n',
            '<{([{{}}[<[[[<>{}]]]>[]]'
        ]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 26397)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 288957)
