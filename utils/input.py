import os

from typing import Union


def __get_day_from_filename(filename):
    path = os.path.splitext(filename)[0]
    path = os.path.split(path)[-1]
    day = path.strip().lower().replace('day', '')
    return int(day)


def __read_input(path, split_lines=True):
    with open(path) as in_file:
        data = in_file.read()
        if split_lines:
            data = data.splitlines()
        return data


def read_example_input_by_day(day: int, split_lines=True):
    path = os.path.join('inputs', 'examples', f'day{day:0>2}.txt')
    return __read_input(path, split_lines=split_lines)


def read_input_by_day(day: int, split_lines=True):
    path = os.path.join('inputs', f'day{day:0>2}.txt')
    return __read_input(path, split_lines=split_lines)


def read_example_input_by_filename(filename: str, split_lines=True):
    day = __get_day_from_filename(filename)
    return read_example_input_by_day(day, split_lines=split_lines)


def read_input_by_filename(filename: str, split_lines=True):
    day = __get_day_from_filename(filename)
    return read_input_by_day(day, split_lines=split_lines)


def read_example_input(day_or_filename: Union[int, str], split_lines=True):
    try:
        return read_example_input_by_day(int(day_or_filename), split_lines=split_lines)
    except ValueError:
        return read_example_input_by_filename(day_or_filename, split_lines=split_lines)


def read_input(day_or_filename: Union[int, str], split_lines=True):
    try:
        return read_input_by_day(int(day_or_filename), split_lines=split_lines)
    except ValueError:
        return read_input_by_filename(day_or_filename, split_lines=split_lines)
