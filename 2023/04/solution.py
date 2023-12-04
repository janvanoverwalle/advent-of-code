"""https://adventofcode.com/2023/day/4"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from utils import read_input


def parse_card(card: str):
    numbers = card.split(':', 1)[1]
    winning_numbers, my_numbers = numbers.split('|', 1)
    winning_numbers = [int(n) for n in winning_numbers.split()]
    my_numbers = [int(n) for n in my_numbers.split()]
    return winning_numbers, my_numbers


def calculate_card_points(winning_numbers: list[int], my_numbers: list[int]):
    points = 0
    for n in my_numbers:
        if n not in winning_numbers:
            continue
        if points == 0:
            points = 1
        else:
            points *= 2
    return points


def calculate_matching_numbers(winning_numbers: list[int], my_numbers: list[int]):
    matches = 0
    for n in my_numbers:
        if n in winning_numbers:
            matches += 1
    return matches


def process_card(cards, index: int, winning_numbers: list[int], my_numbers: list[int], depth=0):
    amount = calculate_matching_numbers(winning_numbers, my_numbers)
    print(f'{"  " * depth}[{index+1}] {amount}')
    if amount == 0:
        return 0
    r = list(range(1, amount+1))
    for i in r:
        amount += process_card(cards, index + i, *cards[index + i], depth=depth+1)
    return amount


def determine_card_points():
    lines = read_input(__file__)
    total_points = 0
    for line in lines:
        winning_numbers, my_numbers = parse_card(line)
        total_points += calculate_card_points(winning_numbers, my_numbers)
    return total_points


def determine_amount_cards():
    lines = read_input(__file__, example=False)
    cards = []
    for line in lines:
        cards.append(parse_card(line))

    copies = {}
    final_amount = 0
    for index, card in enumerate(cards):
        amount = 1
        if index in copies:
            amount += copies[index]
        final_amount += amount
        matches = calculate_matching_numbers(*card)
        for i in range(index+1, index+matches+1):
            if i not in copies:
                copies[i] = 0
            copies[i] += amount

    return final_amount


def part1():
    print(determine_card_points())


def part2():
    print(determine_amount_cards())


part1()
part2()
