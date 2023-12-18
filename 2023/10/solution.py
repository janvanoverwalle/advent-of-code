"""https://adventofcode.com/2023/day/10"""

import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from enum import StrEnum
from typing import NamedTuple
from utils import read_input


class Tiles(StrEnum):
    PIPE_NS = '|'
    PIPE_EW = '-'
    BEND_NE = 'L'
    BEND_NW = 'J'
    BEND_SE = 'F'
    BEND_SW = '7'
    GROUND = '.'
    START_POS = 'S'

    @classmethod
    def names(cls):
        return [t.name for t in cls]

    @classmethod
    def values(cls):
        return [t.value for t in cls]


class Directions(StrEnum):
    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'

    @classmethod
    def opposite(cls, direction):
        match direction:
            case cls.NORTH:
                return cls.SOUTH
            case cls.EAST:
                return cls.WEST
            case cls.SOUTH:
                return cls.NORTH
            case cls.WEST:
                return cls.EAST


class Position(NamedTuple):
    x: int
    y: int

    def __add__(self, other: 'Position'):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Position'):
        return Position(self.x - other.x, self.y - other.y)


CONNECTION_MAP = {
    Directions.NORTH: (Tiles.PIPE_NS, Tiles.BEND_SE, Tiles.BEND_SW),
    Directions.EAST: (Tiles.PIPE_EW, Tiles.BEND_NW, Tiles.BEND_SW),
    Directions.SOUTH: (Tiles.PIPE_NS, Tiles.BEND_NE, Tiles.BEND_NW),
    Directions.WEST: (Tiles.PIPE_EW, Tiles.BEND_NE, Tiles.BEND_SE)
}


clean_grid = []  # Not used currently
def set_clean_grid_position(dirty_grid: list[str], pos: Position):
    if len(clean_grid) != len(dirty_grid):
        for i in range(len(dirty_grid)):
            clean_grid.append(['.'] * len(dirty_grid[i]))

    clean_grid[pos.y][pos.x] = get_tile_at(dirty_grid, pos).value


def find_start_position(grid: list[str]):
    for y, row in enumerate(grid):
        try:
            x = row.index('S')
            start_pos = Position(x, y)
            break
        except ValueError:
            continue
    return start_pos


def get_tile_at(grid: list[str], pos: Position):
    if pos is None:
        return None
    if pos.y < 0 or pos.y >= len(grid):
        return None
    if pos.x < 0 or pos.x >= len(grid[pos.y]):
        return None
    return Tiles(grid[pos.y][pos.x])


def get_direction_to(from_pos: Position, to_pos: Position):
    diff_pos = to_pos - from_pos
    if diff_pos.x > 0:
        return Directions.EAST
    if diff_pos.x < 0:
        return Directions.WEST
    if diff_pos.y > 0:
        return Directions.SOUTH
    if diff_pos.y < 0:
        return Directions.NORTH


def get_adjacent_positions(grid: list[str], pos: Position):
    positions = [
        Position(pos.x, pos.y-1),  # North
        Position(pos.x+1, pos.y),  # East
        Position(pos.x, pos.y+1),  # South
        Position(pos.x-1, pos.y)  # West
    ]

    for i in range(len(positions)):
        v = get_tile_at(grid, positions[i])
        if v is None:
            positions[i] = None

    return positions


def get_adjacent_tiles(grid: list[str], pos: Position):
    positions = get_adjacent_positions(grid, pos)
    return [None if p is None else get_tile_at(grid, p) for p in positions]


def tile_connects_to(grid: list[str], from_pos: Position, to_pos: Position):
    if from_pos is None or to_pos is None:
        return False

    from_value = get_tile_at(grid, from_pos)
    to_value = get_tile_at(grid, to_pos)
    direction = get_direction_to(from_pos, to_pos)

    #print(f'  {from_pos}: {from_value}')
    #print(f'  {to_pos}: {to_value}')
    #print(f'  Direction: {direction}')

    if Tiles.GROUND in (from_value, to_value):
        return False

    if from_value == Tiles.START_POS:
        return to_value in CONNECTION_MAP[direction]

    t, d = from_value.name.split('_', 1)
    if direction not in d:
        return False

    return to_value in CONNECTION_MAP[direction]


def get_connecting_positions(grid: list[str], pos: Position):
    tile = get_tile_at(grid, pos)
    north, east, south, west = get_adjacent_positions(grid, pos)
    if tile == Tiles.START_POS:
        return [
            north if get_tile_at(grid, north) in CONNECTION_MAP[Directions.NORTH] else None,
            east if get_tile_at(grid, east) in CONNECTION_MAP[Directions.EAST] else None,
            south if get_tile_at(grid, south) in CONNECTION_MAP[Directions.SOUTH] else None,
            west if get_tile_at(grid, west) in CONNECTION_MAP[Directions.WEST] else None
        ]

    return [p if tile_connects_to(grid, pos, p) else None for p in [north, east, south, west]]


def get_connecting_tiles(grid: list[str], pos: Position):
    positions = get_connecting_positions(grid, pos)
    return [None if p is None else get_tile_at(grid, p) for p in positions]


def _traverse_pipes_rec(grid: list[str], pos: Position, acc: list, backward=False, direction: Directions=None) -> list[Position]:
    positions = get_connecting_positions(grid, pos)
    directions = list(Directions)

    if direction:
        del positions[directions.index(direction)]
        del directions[directions.index(direction)]

    #print(positions)
    #print([get_tile_at(grid, p).value for p in positions])

    if backward:
        positions.reverse()
        directions.reverse()

    if all(p is None for p in positions):
        acc.append(get_tile_at(grid, pos))
        return

    index: int
    for i, p in enumerate(positions):
        if p:
            index = i
            break

    next_pos = positions[index]
    next_dir = directions[index]

    #print(f'  {get_tile_at(grid, pos).value} > {get_tile_at(grid, next_pos).value}')

    acc.append(get_tile_at(grid, pos))
    _traverse_pipes(grid, next_pos, acc, backward, Directions.opposite(next_dir))


def _traverse_pipes(grid: list[str], pos: Position, backward=False, direction: Directions=None) -> list[Position]:
    set_clean_grid_position(grid, pos)

    positions = get_connecting_positions(grid, pos)
    directions = list(Directions)

    if direction:
        del positions[directions.index(direction)]
        del directions[directions.index(direction)]

    #print(positions)
    #print([get_tile_at(grid, p).value for p in positions])

    if backward:
        positions.reverse()
        directions.reverse()

    if all(p is None for p in positions):
        return None, None

    index: int
    for i, p in enumerate(positions):
        if p:
            index = i
            break

    next_pos = positions[index]
    next_dir = directions[index]

    #print(f'  {get_tile_at(grid, pos).value} > {get_tile_at(grid, next_pos).value}')

    return next_pos, Directions.opposite(next_dir)


def traverse_pipes(grid: list[str], pos: Position, backward=False) -> list[Position]:
    next_pos = pos
    direction: Directions = None
    result = [get_tile_at(grid, next_pos)]

    while True:
        next_pos, direction = _traverse_pipes(grid, next_pos, backward, direction)
        if next_pos is None:
            return result
        result.append(get_tile_at(grid, next_pos))

    result = []
    _traverse_pipes_rec(grid, pos, result, backward)
    return result


def determine_farthest_steps_from_start():
    lines = read_input(__file__, example=False)
    start_pos = find_start_position(lines)
    result = traverse_pipes(lines, start_pos)
    #print(''.join(result))
    return len(result)//2


def part1():
    print(determine_farthest_steps_from_start())


def part2():
    pass


part1()
part2()
