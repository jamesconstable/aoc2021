#! /usr/bin/env python

'''
Solvers and example test cases for Day 17 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/17>
'''

from collections import defaultdict
import itertools
import math
from typing import Dict, Iterable, List, Tuple
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 17, part 1
    '''
    (x_lower, x_upper), (y_lower, y_upper) = read_input(lines)

    # The shot with the highest height will also be the one which hits the
    # target as close as possible to its bottom edge. Checking that it's
    # actually possible to land within the target's x bounds for the
    # corresponding timestep turns out not to be necessary for either the test
    # case or my puzzle input, but it's easy to design pathological cases where
    # this isn't the case, e.g. trying to hit a target at x=10 when t=2.
    for lower_bound in range(y_lower, y_upper+1, 1):
        max_y_height, _, t = max_valid_y(lower_bound)
        if next(valid_x_values_for_t(t, x_lower, x_upper), None) is not None:
            return max_y_height

    # As a last resort, we can always shoot the probe directly onto the target
    # for a maximum height of 0 :(
    return 0


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 17, part 2
    '''
    # The movement of the probe on each axis is fully independent, so we start
    # by finding all possible initial y velocities, grouped by the timestep(s)
    # at which that velocity puts the probe within the target's y-range, and
    # then do the same for the x-axis. We can then take the set product of both
    # groups at each timestep to find all possible launch options.
    (x_lower, x_upper), (y_lower, y_upper) = read_input(lines)
    _, max_init_y, max_t = max_valid_y(y_lower)
    init_y_options = y_values_by_t(y_lower, y_upper, max_init_y+1)

    init_x_options = defaultdict(list)
    for t in range(max_t+1):
        init_x_options[t] = list(valid_x_values_for_t(t, x_lower, x_upper))

    all_options = set()
    for t in init_y_options:
        for x, y in itertools.product(init_x_options[t], init_y_options[t]):
            all_options.add((x, y))
    return len(all_options)


def read_input(lines: Iterable[str]) \
        -> Tuple[Tuple[int, int], Tuple[int, int]]:
    '''
    Parses the problem input and returns the bounds of the target in the form:
    ((lower X bound, upper X bound), (lower Y bound, upper Y bound))
    '''
    _, _, x_range, y_range = list(lines)[0].split()
    x_lower, x_upper = (int(i) for i in x_range[2:-1].split('..'))
    y_lower, y_upper = (int(i) for i in y_range[2:].split('..'))
    return (x_lower, x_upper), (y_lower, y_upper)


def valid_x_values_for_t(t: int, lower: int, upper: int) -> Iterable[int]:
    '''
    Returns an iterator over all initial x velocities that will place the probe
    within the target range at time `t`.
    '''
    if t <= 0:
        return

    # The full horizontal range of the probe is equal to
    # `triangle(init_x_velocity)`, where `triangle(n)` is the nth triangular
    # number. After that, the probe remains at the same x-position forever.
    # Therefore, if any number in the range [lower, upper] is a triangular
    # number whose position in the triangular number series is less that the
    # timestep, we're guaranteed that we can keep the probe within the target
    # range.
    seen = set()
    init_x = math.ceil(inv_triangle(lower))
    while triangle(init_x) <= upper and init_x <= t:
        yield init_x
        seen.add(init_x)
        init_x += 1

    # We also need to check whether there are any initial velocities that will
    # have the probe passing through (but not landing in) the range at time t.
    init_x = math.ceil((lower + t**2/2)/t - 1/2)
    while init_x > t and init_x * t - triangle(t - 1) <= upper:
        if init_x not in seen:
            yield init_x
        init_x += 1


def max_valid_y(lower: int) -> Tuple[int, int, int]:
    '''
    Given a lower y bound for the target, finds the highest height attainable
    by the probe without overshooting the target, and returns a tuple
    containing that height, the initial y velocty needed to attain it, and the
    timestep at which the probe lands within the target.
    '''
    return triangle(-lower-1), -lower - 1, -2 * lower


def y_values_by_t(target_lower: int, target_upper: int, search_upper: int) \
        -> Dict[int, List[int]]:
    '''
    Returns all initial y velocities that put the probe within the target range
    at some timestep(s), grouped by those timestep(s).
    '''
    y_values = defaultdict(list)
    for init_y in range(target_lower, search_upper):
        t = 1
        height = init_y
        dy = init_y-1
        while height >= target_lower:
            if target_upper >= height:
                y_values[t].append(init_y)
            height += dy
            dy -= 1
            t += 1
    return y_values


def triangle(n: int) -> int:
    '''
    Calculates the nth triangular number.
    '''
    return n * (n+1) // 2


def inv_triangle(n: int) -> float:
    '''
    Calculates the triangular inverse, i.e. x such that triangle(x) = n.
    Result will be non-integral in the case of non-triangular number inputs.
    '''
    return (1 - math.sqrt(1 + 8*n)) / -2


class TestDay17(unittest.TestCase):
    '''
    Example test cases for Day 17, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = ['target area: x=20..30, y=-10..-5']

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 45)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 112)
