"""https://adventofcode.com/2022/day/2"""

from utils import read_input


STR_ROCK = 'ROCK'
STR_PAPER = 'PAPER'
STR_SCISSOR = 'SCISSOR'

VAL_LOSS = 0
VAL_DRAW = 3
VAL_WIN = 6


input_map_part1 = {
    'A': STR_ROCK,
    'B': STR_PAPER,
    'C': STR_SCISSOR,
    'X': STR_ROCK,
    'Y': STR_PAPER,
    'Z': STR_SCISSOR
}

input_map_part2 = {
    'A': STR_ROCK,
    'B': STR_PAPER,
    'C': STR_SCISSOR,
    'X': VAL_LOSS,
    'Y': VAL_DRAW,
    'Z': VAL_WIN
}

reverse_input_map_part2 = {
    STR_ROCK: 'X',
    STR_PAPER: 'Y',
    STR_SCISSOR: 'Z'
}

input_points = {
    STR_ROCK: 1,
    STR_PAPER: 2,
    STR_SCISSOR: 3
}

input_beaten_by = {
    STR_ROCK: STR_PAPER,
    STR_PAPER: STR_SCISSOR,
    STR_SCISSOR: STR_ROCK
}

input_beats = {
    STR_ROCK: STR_SCISSOR,
    STR_PAPER: STR_ROCK,
    STR_SCISSOR: STR_PAPER
}


def evaluate_round(input1: str, input2: str):
    score = input_points[input_map_part1[input2]]
    if input_map_part1[input1] == input_map_part1[input2]:
        score += VAL_DRAW
    elif input_beaten_by[input_map_part1[input1]] == input_map_part1[input2]:
        score += VAL_WIN
    elif input_beaten_by[input_map_part1[input2]] == input_map_part1[input1]:
        score += VAL_LOSS
    return score


def determine_round_input(input1: str, outcome: str):
    if input_map_part2[outcome] == VAL_DRAW:
        return input_map_part2[input1]
    if input_map_part2[outcome] == VAL_WIN:
        return input_beaten_by[input_map_part2[input1]]
    if input_map_part2[outcome] == VAL_LOSS:
        return input_beats[input_map_part2[input1]]


def part1():
    lines = read_input(__file__)
    total_score = sum(evaluate_round(*l.split()) for l in lines)
    print(total_score)


def part2():
    lines = read_input(__file__)
    inputs = [(lambda i, o: (i, determine_round_input(i, o)))(*l.split()) for l in lines]
    total_score = sum(evaluate_round(i1, reverse_input_map_part2[i2]) for i1, i2 in inputs)
    print(total_score)


part1()
part2()
