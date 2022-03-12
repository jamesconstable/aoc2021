#! /usr/bin/env python

'''
Solvers and example test cases for Day 16 of the Advent of Code 2021.
Problem description: <https://adventofcode.com/2021/day/16>
'''

from __future__ import annotations
import abc
from collections import deque
from dataclasses import dataclass
from enum import Enum
from math import prod
from typing import Deque, Iterable, List
import unittest


def part1(lines: Iterable[str]) -> int:
    '''
    Solver for Day 16, part 1
    '''
    packet = parse_packet(deque(hex_to_bin(list(lines)[0].strip())))
    return sum(p.version for p in packet_iter(packet))


def part2(lines: Iterable[str]) -> int:
    '''
    Solver for Day 16, part 2
    '''
    return parse_packet(deque(hex_to_bin(list(lines)[0].strip()))).evaluate()


@dataclass  # type: ignore
class Packet(abc.ABC):
    '''
    Represents a packet transmitted using BITS.
    '''
    version: int
    type: PacketType

    @abc.abstractmethod
    def evaluate(self) -> int:
        '''
        Evaluates this packet.
        '''


@dataclass
class LiteralPacket(Packet):
    '''
    Represents a literal packet transmitted using BITS.
    '''
    value: int

    def evaluate(self) -> int:
        return self.value


@dataclass
class OperatorPacket(Packet):
    '''
    Represents an operator packet transmitted using BITS.
    '''
    subpackets: List[Packet]

    def evaluate(self) -> int:
        subresults = [p.evaluate() for p in self.subpackets]
        match self.type:
            case PacketType.SUM:
                result = sum(subresults)
            case PacketType.PRODUCT:
                result = prod(subresults)
            case PacketType.MINIMUM:
                result = min(subresults)
            case PacketType.MAXIMUM:
                result = max(subresults)
            case PacketType.GREATER_THAN:
                result = int(subresults[0] > subresults[1])
            case PacketType.LESS_THAN:
                result = int(subresults[0] < subresults[1])
            case PacketType.EQUAL_TO:
                result = int(subresults[0] == subresults[1])
        return result


class PacketType(Enum):
    '''
    Enum representing the different packet types.
    '''
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


def parse_packet(data: Deque[int]) -> Packet:
    '''
    Parses a sequence of binary bits into a Packet, possible containing its
    own subpackets. To enable efficient processing, input stream must be
    provided as a deque.
    '''
    version = pop_bits(3, data)
    match (packet_type := PacketType(pop_bits(3, data))):
        case PacketType.LITERAL:
            # Packet represents a literal, consisting of groups of 5 bits with
            # the first bit in each group flagging whether there are more
            # groups to follow (1 for yes, 0 for no).
            value = 0
            while data.popleft() == 1:
                value = value << 4 | pop_bits(4, data)
            value = value << 4 | pop_bits(4, data)
            return LiteralPacket(version, PacketType.LITERAL, value)

        case _:
            length_type_id = data.popleft()
            subpackets = []
            if length_type_id == 0:
                # The next 15 bits represent the total length in bits of the
                # contained sub-packets.
                bit_length = pop_bits(15, data)
                initial_len = len(data)
                while bit_length > initial_len - len(data):
                    subpackets.append(parse_packet(data))
            else:
                # The next 11 bits represent the number of sub-packets
                # immediately contained by this packet.
                subpacket_count = pop_bits(11, data)
                for _ in range(subpacket_count):
                    subpackets.append(parse_packet(data))
            return OperatorPacket(version, packet_type, subpackets)


def pop_bits(n: int, data: Deque[int]) -> int:
    '''
    Removes `n` bits from the start of `data` and returns their integer
    interpretation.
    '''
    total = 0
    for _ in range(n):
        total = (total << 1) | data.popleft()
    return total


def hex_to_bin(data: str) -> List[int]:
    '''
    Converts a hex string into a list of the bits in its binary representation.
    '''
    return [int(i) for i in bin(int(data, 16))[2:].zfill(4*len(data))]


def packet_iter(packet: Packet) -> Iterable[Packet]:
    '''
    Returns a pre-order iterator over `packet` and all its subpackets.
    '''
    yield packet
    if isinstance(packet, OperatorPacket):
        for subpacket in packet.subpackets:
            yield from packet_iter(subpacket)


class TestDay16(unittest.TestCase):
    '''
    Example test cases for Day 16, as specified in the problem description
    '''
    # pylint: disable=missing-function-docstring

    def test_part1_example1(self):
        self.assertEqual(part1(['8A004A801A8002F478']), 16)

    def test_part1_example2(self):
        self.assertEqual(part1(['620080001611562C8802118E34']), 12)

    def test_part1_example3(self):
        self.assertEqual(part1(['C0015000016115A2E0802F182340']), 23)

    def test_part1_example4(self):
        self.assertEqual(part1(['A0016C880162017C3686B18A3D4780']), 31)

    def test_part2_example1(self):
        self.assertEqual(part2(['C200B40A82']), 3)

    def test_part2_example2(self):
        self.assertEqual(part2(['04005AC33890']), 54)

    def test_part2_example3(self):
        self.assertEqual(part2(['880086C3E88112']), 7)

    def test_part2_example4(self):
        self.assertEqual(part2(['CE00C43D881120']), 9)

    def test_part2_example5(self):
        self.assertEqual(part2(['D8005AC2A8F0']), 1)

    def test_part2_example6(self):
        self.assertEqual(part2(['F600BC2D8F']), 0)

    def test_part2_example7(self):
        self.assertEqual(part2(['9C005AC2F8F0']), 0)

    def test_part2_example8(self):
        self.assertEqual(part2(['9C0141080250320F1802104A08']), 1)
