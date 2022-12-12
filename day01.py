"""https://adventofcode.com/2022/day/1"""

from utils import read_input


def calculate_calories_per_elf():
    lines = read_input(__file__)

    calories_per_elf = [0]
    for line in lines:
        if not line:
            calories_per_elf.append(0)
        else:
            calories_per_elf[-1] += int(line)

    return sorted(calories_per_elf, reverse=True)


def part1():
    calories = calculate_calories_per_elf()
    print(calories[0])


def part2():
    calories = calculate_calories_per_elf()
    print(sum(calories[:3]))


part1()
part2()
