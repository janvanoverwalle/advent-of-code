"""https://adventofcode.com/2023/day/1"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from utils import read_input


DIGIT_MAP = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}


def find_calibration_value(include_substrings=False):
    lines = read_input(__file__)
    total = 0
    for line in lines:
        digits = []
        for index, char in enumerate(line):
            try:
                digits.append(int(char))
            except ValueError:
                if not include_substrings:
                    continue
                for k in DIGIT_MAP.keys():
                    if line[index:].startswith(k):
                        digits.append(DIGIT_MAP[k])
                        break
        total += int(f'{digits[0]}{digits[-1]}')
    return total


def part1():
    print(find_calibration_value())


def part2():
    print(find_calibration_value(include_substrings=True))


part1()
part2()
