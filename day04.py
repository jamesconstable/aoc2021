#! /usr/bin/env python

'''
Solvers and example test cases for Day 4 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/4>
'''

from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, List, Tuple
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 4, part 1
    '''
    draw_order, boards = parse_input(lines)
    for drawn in draw_order:
        for board in boards:
            update(board, drawn)
            if is_complete(board):
                return score(board, drawn)

    raise ValueError("No winning board for given draw order")


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 4, part 2
    '''
    draw_order, boards = parse_input(lines)
    for drawn in draw_order:
        filtered = []
        for board in boards:
            update(board, drawn)
            if not is_complete(board):
                filtered.append(board)

        # Check if we've just completed the final board.
        match (boards, filtered):
            case ([board], []):
                return score(board, drawn)
            case (_, []):
                raise ValueError("A tie was reached; no single losing board")
        boards = filtered

    raise ValueError("No winning board for given draw order")


class CellState(Enum):
    '''
    Represents the state of a single bingo cell.
    '''
    MARKED = auto()
    UNMARKED = auto()


@dataclass
class BingoCell:
    '''
    Represents a single cell on a bingo board.
    '''
    value: int
    state: CellState


Board = List[List[BingoCell]]


def update(board: Board, drawn: int) -> None:
    '''
    Updates board by marking off any instances of drawn.
    '''
    for row in board:
        for cell in row:
            if cell.value == drawn:
                cell.state = CellState.MARKED


def is_complete(board: Board) -> bool:
    '''
    Checks if board is in a winning configuration, i.e. there is one row or
    column that has been fully marked.
    '''
    # Check for a fully marked row
    for row in board:
        complete = True
        for cell in row:
            if cell.state == CellState.UNMARKED:
                complete = False
                break
        if complete:
            return True

    # Check for a fully marked column
    for i in range(len(board[0])):
        complete = True
        for row in board:
            if row[i].state == CellState.UNMARKED:
                complete = False
                break
        if complete:
            return True

    return False


def score(board: Board, last_drawn: int) -> int:
    '''
    Calculates the score of a board given its state and the last number drawn.
    A board's score is defined as the sum of all its unmarked numbers
    multiplied by the final number.
    '''
    total = 0
    for row in board:
        for cell in row:
            if cell.state == CellState.UNMARKED:
                total += cell.value
    return total * last_drawn


def parse_input(lines: Iterable[str]) -> Tuple[List[int], List[Board]]:
    '''
    Parses the problem input into a tuple containing the bingo draw order and a
    list of the boards represented as 2D lists.
    '''
    line_iter = iter(lines)
    draw_order = [int(i) for i in next(line_iter).strip().split(',')]

    # Skip blank line between draw order and boards
    next(line_iter)

    boards = []
    while (line := next(line_iter, '')) != '':
        board = []
        for _ in range(5):
            board.append([BingoCell(int(x), CellState.UNMARKED)
                          for x in line.split()])
            line = next(line_iter, '')
        boards.append(board)
        if line is None:
            break

    return (draw_order, boards)


class TestDay04(unittest.TestCase):
    '''
    Example test cases for Day 4, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def setUp(self):
        self.data = [
            '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,'
            '3,26,1',
            '',
            '22 13 17 11  0',
            ' 8  2 23  4 24',
            '21  9 14 16  7',
            ' 6 10  3 18  5',
            ' 1 12 20 15 19',
            '',
            ' 3 15  0  2 22',
            ' 9 18 13 17  5',
            '19  8  7 25 23',
            '20 11 10 24  4',
            '14 21 16 12  6',
            '',
            '14 21 17 24  4',
            '10 16 15  9 19',
            '18  8 23 26 20',
            '22 11 13  6  5',
            ' 2  0 12  3  7']

    def test_part1_example(self):
        self.assertEqual(part1(self.data), 4512)

    def test_part2_example(self):
        self.assertEqual(part2(self.data), 1924)
