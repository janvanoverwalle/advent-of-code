"""https://adventofcode.com/2022/day/8"""

from functools import reduce
from utils import read_input, read_example_input


def convert_to_height_map(data: list[str]):
    return [[int(v) for v in row] for row in data]


def is_visible(height_map: list[list[int]], x: int, y: int):
    if x <= 0 or y <= 0 or y >= len(height_map)-1 or x >= len(height_map[y])-1:
        return True
    height = height_map[y][x]
    row = height_map[y][:]
    column = [r[x] for r in height_map]
    if all(height > v for v in row[:x]):
        return True
    if all(height > v for v in row[x+1:]):
        return True
    if all(height > v for v in column[:y]):
        return True
    if all(height > v for v in column[y+1:]):
        return True
    return False


def count_visible_trees(height_map: list[list[int]]):
    num_visible_trees = 0
    for y, r in enumerate(height_map):
        for x in range(len(r)):
            if is_visible(height_map, x, y):
                num_visible_trees += 1
    return num_visible_trees


def calculcate_scenic_score(height_map: list[list[int]], x: int, y: int):
    height = height_map[y][x]
    distances = [0, 0, 0, 0]

    # Up
    for i in range(y-1, -1, -1):
        distances[0] += 1
        if height_map[i][x] >= height:
            break

    # Left
    for i in range(x-1, -1, -1):
        distances[1] += 1
        if height_map[y][i] >= height:
            break

    # Right
    for i in range(x+1, len(height_map[y]), 1):
        distances[2] += 1
        if height_map[y][i] >= height:
            break

    # Down
    for i in range(y+1, len(height_map), 1):
        distances[3] += 1
        if height_map[i][x] >= height:
            break

    return reduce((lambda a, b: a * b), distances)


def get_highest_scenic_score(height_map: list[list[int]]):
    highest_scenic_score = 0
    for y, r in enumerate(height_map):
        for x in range(len(r)):
            scenic_score = calculcate_scenic_score(height_map, x, y)
            if scenic_score > highest_scenic_score:
                highest_scenic_score = scenic_score
    return highest_scenic_score


def part1():
    lines = read_input(__file__)
    height_map = convert_to_height_map(lines)
    print(count_visible_trees(height_map))


def part2():
    lines = read_input(__file__)
    height_map = convert_to_height_map(lines)
    print(get_highest_scenic_score(height_map))


part1()
part2()
