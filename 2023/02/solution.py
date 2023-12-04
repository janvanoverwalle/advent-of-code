"""https://adventofcode.com/2023/day/2"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from utils import read_input


def check_sets(s: str) -> bool:
    for cube in s.strip().split(','):
        amount, color = cube.strip().split(' ', 1)
        amount = int(amount)
        color = color.strip()
        if color == 'red' and amount > 12:
            return False
        if color == 'green' and amount > 13:
            return False
        if color == 'blue' and amount > 14:
            return False
    return True


def determine_possible_games() -> int:
    lines = read_input(__file__)
    possible_game_ids = []
    for line in lines:
        game, results = line.split(':', 1)
        game_id = int(game.split(' ', 1)[1])
        is_possible = True
        for s in results.strip().split(';'):
            if not check_sets(s):
                is_possible = False
        if is_possible:
            possible_game_ids.append(game_id)
    return sum(possible_game_ids)


def check_results(results: str) -> list[int]:
    fewest_cubes = [0, 0, 0]
    for s in results.strip().split(';'):
        for cube in s.strip().split(','):
            amount, color = cube.strip().split(' ', 1)
            amount = int(amount)
            if color == 'red' and amount > fewest_cubes[0]:
                fewest_cubes[0] = amount
            elif color == 'green' and amount > fewest_cubes[1]:
                fewest_cubes[1] = amount
            elif color == 'blue' and amount > fewest_cubes[2]:
                fewest_cubes[2] = amount
    return fewest_cubes


def determine_fewest_cubes() -> int:
    lines = read_input(__file__)
    final_power = 0
    for line in lines:
        results = line.split(':', 1)[1]
        fewest_cubes = check_results(results)
        power = fewest_cubes.pop()
        while fewest_cubes:
            power *= fewest_cubes.pop()
        final_power += power
    return final_power


def part1():
    print(determine_possible_games())


def part2():
    print(determine_fewest_cubes())


part1()
part2()
