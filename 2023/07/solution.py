"""https://adventofcode.com/2023/day/7"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from utils import read_input


card_value_map = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}


class Hand:
    cards: str
    bid: int
    type: int
    rank: int

    def __init__(self, line: str) -> None:
        segments = line.split()
        self.cards = segments[0]
        self.bid = int(segments[1])
        self.type = 0
        self.rank = 0

        self._determine_type()

    def __str__(self) -> str:
        return f'cards: {self.cards}, bid: {self.bid}, type: {self.type}'

    def __repr__(self) -> str:
        return f'Hand(cards={self.cards}, bid={self.bid}, type={self.type})'

    def __eq__(self, other: 'Hand') -> bool:
        if self.cards == other.cards:
            return True
        if self.type != other.type:
            return False
        return self.compare(other) is None

    def __lt__(self, other: 'Hand') -> bool:
        if self.type < other.type:
            return True
        if self.type > other.type:
            return False
        return self.compare(other) == other

    def __le__(self, other: 'Hand') -> bool:
        if self.type < other.type:
            return True
        if self.type > other.type:
            return False
        return self.compare(other) in (other, None)

    def __gt__(self, other: 'Hand') -> bool:
        if self.type > other.type:
            return True
        if self.type < other.type:
            return False
        return self.compare(other) == self

    def __ge__(self, other: 'Hand') -> bool:
        if self.type > other.type:
            return True
        if self.type < other.type:
            return False
        return self.compare(other) in (self, None)

    def _calculate_card_value_map(self):
        if hasattr(self, '_card_value_map'):
            return self._card_value_map
        self._card_value_map = {}
        for v in self.cards:
            if v not in self._card_value_map:
                self._card_value_map[v] = 0
            self._card_value_map[v] += 1
        return self._card_value_map

    def _determine_type(self):
        hand_set = set(self.cards)
        if len(hand_set) == 1:
            self.type = 7  # Five of a kind
        elif len(hand_set) == 2:
            value_map = self._calculate_card_value_map()
            self.type = 6 if max(value_map.values()) == 4 else 5  # Four of a kind (6) or Full house (5)
        elif len(hand_set) == 3:
            value_map = self._calculate_card_value_map()
            self.type = 4 if max(value_map.values()) == 3 else 3  # Three of a kind (4) or Two pair (3)
        elif len(hand_set) == 4:
            self.type = 2  # One pair
        elif len(hand_set) == 5:
            self.type = 1  # High card
        else:
            return 0

    def _compare_cards(self, card1: str, card2: str):
        if card_value_map[card1] == card_value_map[card2]:
            return 0
        return 1 if card_value_map[card1] > card_value_map[card2] else 2

    def compare(self, other: 'Hand'):
        '''Returns whichever hand is considered stronger.'''
        for i in range(len(self.cards)):
            res = self._compare_cards(self.cards[i], other.cards[i])
            if res == 1:
                return self
            if res == 2:
                return other


def determine_total_winnings():
    lines = read_input(__file__, example=True)
    hands = [Hand(line) for line in lines]
    hands.sort()
    return sum(hand.bid * (index+1) for index, hand in enumerate(hands))


def part1():
    print(determine_total_winnings())


def part2():
    pass


part1()
part2()
