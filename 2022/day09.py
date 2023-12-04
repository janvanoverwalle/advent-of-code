"""https://adventofcode.com/2022/day/9"""

from math import dist
from utils import read_input, read_example_input


def sign(n: float):
    return 1 if n > 0 else -1


class Grid:
    def __init__(self, num_knots=2) -> None:
        self.start_position = [0, 0]  # X, Y
        self.rope = []
        for _ in range(num_knots):
            self.rope.append(self.start_position[:])  # Create fresh copies
        self.grid = {}

        self.__update_grid()

    @property
    def head_position(self):
        return self.rope[0]

    @property
    def tail_position(self):
        return self.rope[-1]

    def __to_coord(self, position):
        return tuple(position)

    def __update_grid(self):
        self.grid[self.__to_coord(self.tail_position)] = '#'

    def __move_head(self, direction: str):
        if direction == 'U':
            self.head_position[1] += 1
        if direction == 'D':
            self.head_position[1] -= 1
        if direction == 'L':
            self.head_position[0] -= 1
        if direction == 'R':
            self.head_position[0] += 1
        self.__update_grid()

    def __move_tail(self, knot_index=1):
        if dist(self.rope[knot_index-1], self.rope[knot_index]) < 2:
            # Knot is adjecent to previous knot, so no need to move it
            return

        diff = [v-self.rope[knot_index][i] for i, v in enumerate(self.rope[knot_index-1])]
        for i in (0, 1):
            self.rope[knot_index][i] += (0 if diff[i] == 0 else sign(diff[i]))

        self.__update_grid()

    def print(self):
        keys = [k for k in self.grid.keys()]
        keys: list[tuple[int]]
        right = max(k[0] for k in keys)
        left = min(k[0] for k in keys)
        up = max(k[1] for k in keys)
        down = min(k[1] for k in keys)
        for y in range(up, down-1, -1):
            row = [self.grid.get(self.__to_coord((x, y)), '.') for x in range(left, right+1)]
            print(' '.join(row))
        print()

    def perform_motion(self, direction: str, amount: int):
        for _ in range(amount):
            self.__move_head(direction)
            for i in range(1, len(self.rope)):
                self.__move_tail(knot_index=i)

    def perform_motions(self, motions: list[str]):
        for motion in motions:
            direction, amount = motion.split()
            self.perform_motion(direction, int(amount))

    def count_visited_tail_positions(self):
        return len(self.grid)


def part1():
    lines = read_input(__file__)
    grid = Grid()
    grid.perform_motions(lines)
    #grid.print()
    print(grid.count_visited_tail_positions())


def part2():
    lines = read_input(__file__)
    grid = Grid(num_knots=10)
    grid.perform_motions(lines)
    #grid.print()
    print(grid.count_visited_tail_positions())


part1()
part2()
