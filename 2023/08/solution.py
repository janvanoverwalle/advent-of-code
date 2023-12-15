"""https://adventofcode.com/2023/day/8"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

import math
from utils import read_input


direction_map = {
    'R': 1,
    'L': 0
}


def parse_nodes(nodes: list[str]) -> dict[str, list[str]]:
    node_map = {}
    for node in nodes:
        curr_node, dest_nodes = node.split('=', 1)
        node_map[curr_node.strip()] = [n.strip() for n in dest_nodes.strip()[1:-1].split(',')]
    return node_map


def determine_steps_to_reach_end():
    lines = read_input(__file__)
    directions = lines[0]
    nodes = parse_nodes(lines[2:])

    num_steps = 0
    direction_index = 0
    curr_node = 'AAA'
    while curr_node != 'ZZZ':
        #print(f'{curr_node} > {nodes[curr_node]}')
        num_steps += 1
        direction = directions[direction_index]
        #print(f'  Going {direction}')
        curr_node = nodes[curr_node][direction_map[direction]]
        #print(f'  {curr_node}')
        direction_index = (direction_index + 1) % len(directions)
    return num_steps


def determine_ghost_steps_to_reach_end():
    lines = read_input(__file__)
    directions = lines[0]
    nodes = parse_nodes(lines[2:])

    num_steps = 0
    direction_index = 0
    current_nodes = [n for n in nodes.keys() if n.endswith('A')]
    steps_to_end_node = [-1] * len(current_nodes)
    while any(s < 0 for s in steps_to_end_node):
        num_steps += 1
        direction = direction_map[directions[direction_index]]
        direction_index = (direction_index + 1) % len(directions)

        for index, node in enumerate(current_nodes):
            if steps_to_end_node[index] > 0:
                continue
            current_nodes[index] = nodes[node][direction]
            if current_nodes[index].endswith('Z'):
                steps_to_end_node[index] = num_steps

    return math.lcm(*steps_to_end_node)


def part1():
    print(determine_steps_to_reach_end())


def part2():
    print(determine_ghost_steps_to_reach_end())


part1()
part2()
