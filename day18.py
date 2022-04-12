#! /usr/bin/env python

'''
Solvers and example test cases for Day 18 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/18>
'''

from __future__ import annotations
import abc
import math
from typing import Iterable, List, Optional, Tuple
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 18, part 1
    '''
    total = None
    for line in lines:
        number = parse_line(line)
        if total is None:
            total = number
        else:
            total += number

    assert total is not None
    return total.magnitude()


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 18, part 2
    '''
    max_magnitude = 0
    numbers = [parse_line(line) for line in lines]
    for i, number1 in enumerate(numbers):
        for j, number2 in enumerate(numbers):
            if i == j:
                continue
            if (current := (number1 + number2).magnitude()) > max_magnitude:
                max_magnitude = current
    return max_magnitude


class SnailfishNumber(abc.ABC):
    '''
    Abstract base class for snailfish numbers. To keep running times
    reasonable, many snailfish number methods are destructive; unless
    specifed otherwise, the object upon which the call was made should be
    considered invalid after the call, and the returned object used in its
    place.
    '''

    def __add__(self, other):
        return SnailfishPair(self.clone(), other.clone()).reduce()

    def reduce(self) -> SnailfishNumber:
        '''
        Returns the reduced form of this snailfish number, invalidating `self`
        in the process.
        '''
        result = self
        changed = True
        while changed:
            result, changed = result.explode()
            if not changed:
                result, changed = result.split()
        return result

    @abc.abstractmethod
    def explode(self, depth: int = 0) -> Tuple[SnailfishNumber, bool]:
        '''
        Attempts to explode this snailfish number, returning a tuple containing
        the result and a Boolean indicating whether or not an explosion took
        place. This snailfish number is invalidated in the process.
        '''

    @abc.abstractmethod
    def split(self) -> Tuple[SnailfishNumber, bool]:
        '''
        Attempts to split this snailfish number, returning a tuple containing
        the result and a Boolean indicating whether or not a split took place.
        This snailfish number is invalidated in the process.
        '''

    @abc.abstractmethod
    def magnitude(self) -> int:
        '''
        Returns the magnitude of this snailfish number. Non-destructive.
        '''

    @abc.abstractmethod
    def leftmost_value(self) -> SnailfishValue:
        '''
        Returns the leftmost value in this snailfish number. Non-destructive.
        '''

    @abc.abstractmethod
    def rightmost_value(self) -> SnailfishValue:
        '''
        Returns the rightmost value in this snailfish number. Non-destructive.
        '''

    @abc.abstractmethod
    def clone(self) -> SnailfishNumber:
        '''
        Returns a deep copy of this snailfish number. Non-destructive.
        '''


class SnailfishValue(SnailfishNumber):
    '''
    Represents a value (leaf node) within the snailfish number system.
    '''

    def __init__(self,
                 value: int,
                 prev_value: Optional[SnailfishValue] = None,
                 next_value: Optional[SnailfishValue] = None):
        self.value = value
        self.prev = prev_value
        self.next = next_value

    def explode(self, depth=0) -> Tuple[SnailfishNumber, bool]:
        return self, False

    def split(self) -> Tuple[SnailfishNumber, bool]:
        if self.value >= 10:
            left = SnailfishValue(int(self.value / 2), self.prev, None)
            right = SnailfishValue(math.ceil(self.value / 2), left, self.next)
            left.next = right
            if self.prev is not None:
                self.prev.next = left
            if self.next is not None:
                self.next.prev = right
            return SnailfishPair(left, right), True
        return self, False

    def magnitude(self) -> int:
        return self.value

    def leftmost_value(self) -> SnailfishValue:
        return self

    def rightmost_value(self) -> SnailfishValue:
        return self

    def clone(self) -> SnailfishValue:
        return SnailfishValue(self.value)


class SnailfishPair(SnailfishNumber):
    '''
    Represents a pair (internal node) within the snailfish number system.
    '''

    def __init__(self, left: SnailfishNumber, right: SnailfishNumber):
        self.left = left
        self.right = right
        self.left.rightmost_value().next = self.right.leftmost_value()
        self.right.leftmost_value().prev = self.left.rightmost_value()

    def explode(self, depth=0) -> Tuple[SnailfishNumber, bool]:
        if depth == 4:
            assert isinstance(self.left, SnailfishValue)
            assert isinstance(self.right, SnailfishValue)
            new_value = SnailfishValue(0, self.left.prev, self.right.next)
            if self.left.prev is not None:
                self.left.prev.value += self.left.value
                self.left.prev.next = new_value
            if self.right.next is not None:
                self.right.next.value += self.right.value
                self.right.next.prev = new_value
            return new_value, True

        left_result, changed = self.left.explode(depth+1)
        if changed:
            return SnailfishPair(left_result, self.right), True
        right_result, changed = self.right.explode(depth+1)
        return SnailfishPair(self.left, right_result), changed

    def split(self) -> Tuple[SnailfishNumber, bool]:
        left_result, changed = self.left.split()
        if changed:
            return SnailfishPair(left_result, self.right), True

        right_result, changed = self.right.split()
        return SnailfishPair(self.left, right_result), changed

    def magnitude(self) -> int:
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    def leftmost_value(self) -> SnailfishValue:
        return self.left.leftmost_value()

    def rightmost_value(self) -> SnailfishValue:
        return self.right.rightmost_value()

    def clone(self) -> SnailfishPair:
        return SnailfishPair(self.left.clone(), self.right.clone())


def parse_line(line: str) -> SnailfishNumber:
    '''
    Parses the given string into a SnailfishNumber.
    '''
    stack: List[SnailfishNumber] = []
    for char in line.strip():
        match char:
            case ']':
                right = stack.pop()
                stack.append(SnailfishPair(stack.pop(), right))
            case ',' | '[':
                pass
            case _:
                value = SnailfishValue(int(char))
                stack.append(value)
    return stack.pop()


class TestDay18(unittest.TestCase):
    '''
    Example test cases for Day 18, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            '[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n',
            '[[[5,[2,8]],4],[5,[[9,9],0]]]\n',
            '[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n',
            '[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n',
            '[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n',
            '[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n',
            '[[[[5,4],[7,7]],8],[[8,3],8]]\n',
            '[[9,3],[[9,9],[6,[4,9]]]]\n',
            '[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n',
            '[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'
            ]

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 4140)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 3993)
