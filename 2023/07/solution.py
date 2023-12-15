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

card_value_map_with_jokers = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
    'J': 1
}


def get_card_value_map(uses_jokers=False):
    if uses_jokers:
        return card_value_map_with_jokers
    return card_value_map


class Hand:
    cards: str
    bid: int
    type: int
    rank: int

    def __init__(self, line: str, uses_jokers=False) -> None:
        segments = line.split()
        self.cards = segments[0]
        self.bid = int(segments[1])
        self.type = 0
        self.rank = 0
        self._uses_jokers = uses_jokers

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

    def _contains_jokers(self) -> bool:
        return 'J' in self.cards

    def _calculate_card_value_map(self, cards: str=None) -> dict[str, int]:
        if not cards:
            cards = self.cards
        card_value_map_for_hand = {}
        for v in cards:
            if v not in card_value_map_for_hand:
                card_value_map_for_hand[v] = 0
            card_value_map_for_hand[v] += 1
        return card_value_map_for_hand

    def _calculate_type(self, cards: str=None) -> int:
        if not cards:
            cards = self.cards
        hand_set = set(cards)
        if len(hand_set) == 1:
            return 7  # Five of a kind
        elif len(hand_set) == 2:
            value_map = self._calculate_card_value_map(cards=cards)
            return 6 if max(value_map.values()) == 4 else 5  # Four of a kind (6) or Full house (5)
        elif len(hand_set) == 3:
            value_map = self._calculate_card_value_map(cards=cards)
            return 4 if max(value_map.values()) == 3 else 3  # Three of a kind (4) or Two pair (3)
        elif len(hand_set) == 4:
            return 2  # One pair
        elif len(hand_set) == 5:
            return 1  # High card
        else:
            return 0

    def _determine_type(self) -> int:
        if not self._uses_jokers or not self._contains_jokers():
            self.type = self._calculate_type()
            return self.type

        cvm = self._calculate_card_value_map(cards=self.cards.replace('J', ''))
        max_keys = [max(cvm, key=cvm.get)]
        for k, v in cvm.items():
            if k in max_keys:
                continue
            if v == cvm[max_keys[0]]:
                max_keys.append(k)

        self.type = max(self._calculate_type(cards=self.cards.replace('J', k)) for k in max_keys)
        return self.type

    def _compare_cards(self, card1: str, card2: str):
        cvm = get_card_value_map(uses_jokers=self._uses_jokers)
        if cvm[card1] == cvm[card2]:
            return 0
        return 1 if cvm[card1] > cvm[card2] else 2

    def compare(self, other: 'Hand'):
        '''Returns whichever hand is considered stronger.'''
        for i in range(len(self.cards)):
            res = self._compare_cards(self.cards[i], other.cards[i])
            if res == 1:
                return self
            if res == 2:
                return other


def determine_total_winnings(uses_jokers=False):
    lines = read_input(__file__)
    hands = [Hand(line, uses_jokers=uses_jokers) for line in lines]
    hands.sort()
    return sum(hand.bid * (index+1) for index, hand in enumerate(hands))


def part1():
    print(determine_total_winnings())


def part2():
    print(determine_total_winnings(uses_jokers=True))


part1()
part2()
