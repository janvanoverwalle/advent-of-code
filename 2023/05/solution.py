"""https://adventofcode.com/2023/day/5"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from utils import read_input


maps: dict[str, list[str]] = {}


def create_maps(lines: list[str]) -> None:
    index = 0
    try:
        while lines:
            name = lines[index].split(' ', 1)[0]
            maps[name] = []
            index+=1
            while lines[index]:
                maps[name].append([int(s) for s in lines[index].split(' ')])
                index += 1
            index += 1
    except IndexError:
        pass


def get_mapped_number(name: str, number: int) -> int:
    for line in maps[name]:
        dest_start, src_start, range_length = line
        if src_start <= number <= src_start + range_length:
            return dest_start + (number - src_start)
    return number


def traverse_maps(number: int) -> int:
    _number = number
    for m in maps.keys():
        _number = get_mapped_number(m, _number)
    return _number


def part1():
    lines = read_input(__file__)
    seeds = [int(s) for s in lines[0].split(':', 1)[1].strip().split(' ')]
    create_maps(lines[2:])
    lowest_location = min(traverse_maps(seed) for seed in seeds)
    print(lowest_location)


def part2():
    pass


part1()
part2()
