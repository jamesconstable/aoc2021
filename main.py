#! /usr/bin/env python
'''
Command-line runner for Advent of Code 2021 solvers.
Usage: ./main.py <day_number> <part_number> < input.txt
'''

import sys

import day01
import day02
import day03
import day04
import day05
import day06
import day07
import day08
import day09
import day10
import day11
import day12
import day13
import day14


def exit_with_error(message: str, error_code: int = -1) -> None:
    '''
    Prints the given message to stderr and exits with the specified exit code
    (default is -1).
    '''
    print(message, file=sys.stderr)
    sys.exit(error_code)


def show_usage_and_exit() -> None:
    '''
    Prints the CLI usage message to stderr and exits with code -1.
    '''
    exit_with_error('Usage: ./main.py <day_number> <part_number> < input.txt')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        # Insufficient arguments given
        show_usage_and_exit()

    days = [day01, day02, day03, day04, day05, day06, day07, day08, day09,
            day10, day11, day12, day13, day14]
    try:
        day = int(sys.argv[1])
    except ValueError:
        # Day number couldn't be parsed as an int
        show_usage_and_exit()

    if 0 < day <= len(days):
        module = days[day-1]
    else:
        exit_with_error(
                f"Invalid day '{day}'; "
                f"day must be between 1 and {len(days)} inclusive.")

    match part := sys.argv[2]:
        case '1': fn = module.part1
        case '2': fn = module.part2
        case _:
            exit_with_error(
                    f"Invalid part '{part}'; part must be either 1 or 2.")

    print(fn(sys.stdin))
