"""https://adventofcode.com/2022/day/xx"""

import re

from utils import read_input, read_example_input


def get_stacks(input: list[str]):
    stacks = []
    for line in input:
        if not line.strip():
            break
        crates = [line[i] for i in range(1, len(line), 4)]
        if ''.join(crates) == ''.join(str(i) for i in range(1, len(crates)+1)):
            break
        for index, crate in enumerate(crates):
            if not crate.strip():
                continue
            while len(stacks) < index+1:
                stacks.append([])
            stacks[index].insert(0, crate)
    return stacks


def get_instructions(input: list[str]):
    instructions = []
    for line in input:
        match = re.match(r'move ([0-9]+) from ([0-9]+) to ([0-9]+)', line)
        if not match:
            continue
        instructions.append(tuple(map(lambda x: int(x), match.groups())))
    return instructions


def execute_CM9000_instruction(stacks, instruction):
    for _ in range(instruction[0]):
        crate = stacks[instruction[1]-1].pop()
        stacks[instruction[2]-1].append(crate)


def execute_CM9001_instruction(stacks, instruction):
    crates = list(stacks[instruction[1]-1][-instruction[0]:])
    stacks[instruction[1]-1] = stacks[instruction[1]-1][:-instruction[0]]
    stacks[instruction[2]-1].extend(crates)


def part1():
    lines = read_input(__file__)
    stacks = get_stacks(lines)
    instructions = get_instructions(lines)
    for instruction in instructions:
        execute_CM9000_instruction(stacks, instruction)
    print(''.join([s[-1] for s in stacks]))


def part2():
    lines = read_input(__file__)
    stacks = get_stacks(lines)
    instructions = get_instructions(lines)
    for instruction in instructions:
        execute_CM9001_instruction(stacks, instruction)
    print(''.join([s[-1] for s in stacks]))


part1()
part2()
