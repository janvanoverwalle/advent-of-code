"""https://adventofcode.com/2023/day/6"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from utils import read_input


def calculate_distance(t: int, max_t: int) -> int:
    return (max_t-t) * t


def calculate_options(t: int, d: int) -> int:
    distances = [calculate_distance(i, t) for i in range(t)]
    return len([distance for distance in distances if distance > d])


def determine_number_of_ways_to_beat_record(times: list[int], distances: list[int]) -> int:
    result = 1
    for i in range(len(times)):
        t, d = times[i], distances[i]
        result *= calculate_options(t, d)
    return result


def part1():
    lines = read_input(__file__)
    times = [int(s) for s in lines[0].split(':', 1)[1].strip().split()]
    distances = [int(s) for s in lines[1].split(':', 1)[1].strip().split()]
    print(determine_number_of_ways_to_beat_record(times, distances))


def part2():
    lines = read_input(__file__, example=False)
    times = [int(lines[0].split(':', 1)[1].strip().replace(' ', ''))]
    distances = [int(lines[1].split(':', 1)[1].strip().replace(' ', ''))]
    print(determine_number_of_ways_to_beat_record(times, distances))


part1()
part2()
