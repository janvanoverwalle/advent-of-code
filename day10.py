"""https://adventofcode.com/2022/day/10"""

from utils import read_input, read_example_input


class CPU:
    num_cycles: int
    registers: dict
    command_cycle_cost: dict
    commands: list[str]
    command_index : int
    next_command: str
    next_command_cycle_cost: int

    def __init__(self, commands: list[str]):
        self.command_cycle_cost = {
            'noop': 1,
            'addx': 2
        }

        self.commands = commands

    def __iter__(self):
        self.num_cycles = 0
        self.registers = {
            'X': 1
        }
        self.command_index = 0
        self.next_command = None
        self.next_command_cycle_cost = 0
        return self

    def __next__(self):
        if self.next_command and self.next_command_cycle_cost <= 0:
            self.execute_command(self.next_command)
            self.next_command = None
            self.command_index += 1

        if not self.next_command:
            if self.command_index >= len(self.commands):
                raise StopIteration
            self.next_command = self.commands[self.command_index]
            self.next_command_cycle_cost = self.command_cycle_cost[self.next_command.split()[0]]

        self.next_command_cycle_cost -= 1
        self.num_cycles += 1
        return self.num_cycles

    @property
    def register_x(self):
        return self.registers['X']

    @register_x.setter
    def register_x(self, value):
        self.registers['X'] = value

    @property
    def signal_strength(self):
        return self.num_cycles * self.register_x

    def execute_command(self, command: str):
        parsed_command = command.split()
        if parsed_command[0] == 'noop':
            return
        if parsed_command[0] == 'addx':
            self.register_x += int(parsed_command[1])


class CRT:
    screen_buffer: list[str]
    width: int
    height: int

    def __init__(self, width=40, height=6) -> None:
        self.screen_buffer = []
        self.width = width
        self.height = height

    def draw_pixel(self, lit=False):
        self.screen_buffer.append('#' if lit else '.')

    def print(self):
        line = ''
        for i, p in enumerate(self.screen_buffer):
            line += p
            if i % self.width == self.width-1:
                print(line)
                line = ''


def part1():
    lines = read_input(__file__)
    cpu = CPU(lines)
    print(sum(cpu.signal_strength for cycle in cpu if cycle % 40 == 20))


def part2():
    lines = read_input(__file__)
    cpu = CPU(lines)
    crt = CRT()
    for cycle in cpu:
        crt.draw_pixel(lit=cpu.register_x-1 <= (cycle-1)%40 <= cpu.register_x+1)
    crt.print()


part1()
part2()
