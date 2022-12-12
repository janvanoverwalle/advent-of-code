"""https://adventofcode.com/2022/day/3"""

from utils import read_input, read_example_input
from string import ascii_letters


def get_priorities(*args):
    return [ascii_letters.index(i)+1 for i in args]


def part1():
    rucksacks = read_input(__file__)
    total_priorities = 0
    for rucksack in rucksacks:
        size = len(rucksack)
        compartment1 = rucksack[:size//2]
        compartment2 = rucksack[size//2:]
        shared_items = set(compartment1).intersection(set(compartment2))
        priorities = get_priorities(*shared_items)
        total_priorities += sum(priorities)
    print(total_priorities)


def part2():
    rucksacks = read_input(__file__)
    total_priorities = 0
    for i in range(0, len(rucksacks), 3):
        shared_items = set(rucksacks[i]).intersection(set(rucksacks[i+1])).intersection(set(rucksacks[i+2]))
        priorities = get_priorities(*shared_items)
        total_priorities += sum(priorities)
    print(total_priorities)


part1()
part2()
