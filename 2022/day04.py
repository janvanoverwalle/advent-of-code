"""https://adventofcode.com/2022/day/4"""

import re

from utils import read_input, read_example_input


def get_sections(pair: str):
    result = re.match(r'([0-9]+)-([0-9]+),([0-9]+)-([0-9]+)', pair)
    sections = tuple(map(lambda x: int(x), result.groups()))
    section1 = tuple(range(sections[0], sections[1]+1))  # range stop parameter is exclusive
    section2 = tuple(range(sections[2], sections[3]+1))  # range stop parameter is exclusive
    return section1, section2


def get_overlap(section1, section2):
    return tuple(sorted(set(section1).intersection(set(section2))))


def part1():
    lines = read_input(__file__)
    num_enveloping_pairs = 0
    for pair in lines:
        section1, section2 = get_sections(pair)
        overlap = get_overlap(section1, section2)
        if overlap == section1 or overlap == section2:
            num_enveloping_pairs += 1
    print(num_enveloping_pairs)


def part2():
    lines = read_input(__file__)
    num_overlapping_pairs = 0
    for pair in lines:
        section1, section2 = get_sections(pair)
        overlap = get_overlap(section1, section2)
        if overlap:
            num_overlapping_pairs += 1
    print(num_overlapping_pairs)


part1()
part2()
