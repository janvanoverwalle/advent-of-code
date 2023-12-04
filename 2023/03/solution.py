"""https://adventofcode.com/2023/day/3"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

import string

from utils import read_input


def parse_schematic(lines: list[str]):
    grid: list[list[str]] = []
    symbol_positions: list[tuple[int]] = []
    for y, line in enumerate(lines):
        grid.append([])
        for x, char in enumerate(line):
            grid[-1].append(char)
            if char not in (string.digits + '.'):
                symbol_positions.append((x, y))
    return grid, symbol_positions


def check_symbol(grid: list[list[str]], x: int, y: int) -> list[int]:
    positions_to_check = [
        (x-1, y-1),
        (x-1, y),
        (x-1, y+1),
        (x, y-1),
        (x, y),
        (x, y+1),
        (x+1, y-1),
        (x+1, y),
        (x+1, y+1),
    ]
    part_numbers = []
    for pos in positions_to_check:
        try:
            if grid[pos[1]][pos[0]] in string.digits:
                n = get_number_at_position(grid, pos[0], pos[1])
                part_numbers.append(n)
        except IndexError:
            continue
    return list(set(part_numbers))


def get_number_at_position(grid: list[list[str]], x: int, y: int) -> int:
    try:
        while grid[y][x] in string.digits:
            x -= 1
        x += 1
    except IndexError:
        x = 0

    digits = ''
    try:
        while grid[y][x] in string.digits:
            digits += grid[y][x]
            x += 1
    except IndexError:
        pass

    return int(digits)


def determine_missing_part():
    lines = read_input(__file__)
    grid, symbol_positions = parse_schematic(lines)
    sum_part_numbers = 0
    for pos in symbol_positions:
        sum_part_numbers += sum(check_symbol(grid, pos[0], pos[1]))
    return sum_part_numbers


def get_gear_ratio(grid, x, y):
    numbers = check_symbol(grid, x, y)
    if len(numbers) != 2:
        return -1
    ratio = numbers.pop()
    while numbers:
        ratio *= numbers.pop()
    return ratio


def determine_gear_ratios():
    lines = read_input(__file__)
    grid, symbol_positions = parse_schematic(lines)
    sum_ratios = 0
    for pos in symbol_positions:
        symbol = grid[pos[1]][pos[0]]
        if symbol != '*':
            continue
        ratio = get_gear_ratio(grid, pos[0], pos[1])
        if ratio < 0:
            continue  # Not a gear
        sum_ratios += ratio
    return sum_ratios


def part1():
    print(determine_missing_part())


def part2():
    print(determine_gear_ratios())


part1()
part2()
