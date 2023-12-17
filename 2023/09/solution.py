"""https://adventofcode.com/2023/day/9"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from utils import read_input


def predict_next_value(data: list[int]) -> int:
    differences = []
    for i in range(0, len(data)-1):
        differences.append(data[i+1] - data[i])

    if all(v == 0 for v in differences):
        return data[-1]

    return predict_next_value(differences) + data[-1]


def predict_previous_value(data: list[int]) -> int:
    differences = []
    for i in range(0, len(data)-1):
        differences.append(data[i+1] - data[i])

    if all(v == 0 for v in differences):
        return data[0]

    return data[0] - predict_previous_value(differences)


def determine_sum_of_forward_extrapolated_values() -> int:
    lines = read_input(__file__)
    return sum(predict_next_value([int(v) for v in line.split()]) for line in lines)


def determine_sum_of_backward_extrapolated_values() -> int:
    lines = read_input(__file__)
    return sum(predict_previous_value([int(v) for v in line.split()]) for line in lines)


def part1():
    print(determine_sum_of_forward_extrapolated_values())


def part2():
    print(determine_sum_of_backward_extrapolated_values())


part1()
part2()
