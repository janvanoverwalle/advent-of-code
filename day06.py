"""https://adventofcode.com/2022/day/6"""

from utils import read_input


def find_first_n_distinct_characters(datastream, n=4):
    buffer = list(datastream[::-1])  # Reverse the string and convert to list
    marker = []
    while buffer:
        marker.append(buffer.pop())
        if len(marker) < n:
            continue
        if len(set(marker)) != n:
            marker.pop(0)  # Remove the first element
            continue
        return len(datastream) - len(buffer)


def part1():
    lines = read_input(__file__)
    positions = []
    for datastream in lines:
        pos = find_first_n_distinct_characters(datastream)
        positions.append(pos)
    print(positions)


def part2():
    lines = read_input(__file__)
    positions = []
    for datastream in lines:
        pos = find_first_n_distinct_characters(datastream, 14)
        positions.append(pos)
    print(positions)


part1()
part2()
