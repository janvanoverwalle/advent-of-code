"""https://adventofcode.com/2022/day/11"""

from utils import read_input, read_example_input


class MonkeyBusiness:
    monkeys: list['Monkey']
    lcm: int

    @classmethod
    def calculate_lcm(cls):
        cls.lcm = 1
        for monkey in cls.monkeys:
            cls.lcm *= monkey.test

    @classmethod
    def get_monkey_business(cls, num_rounds: int):
        if num_rounds > 1000:
            cls.calculate_lcm()
        for _ in range(1, num_rounds+1):
            monkey: Monkey
            for monkey in cls.monkeys:
                monkey.do_turn()
        active_monkeys = sorted(cls.monkeys, key=lambda m: m.num_inspected_items, reverse=True)  # Descending
        return active_monkeys[0].num_inspected_items * active_monkeys[1].num_inspected_items


class Monkey:
    index: int
    starting_items: list[int]
    operation: str  # formula
    test: int  # divisible by
    if_true: int  # throw to monkey with index
    if_false: int  # throw to monkey with index
    num_inspected_items: int
    use_lcm: bool

    def __init__(self, use_lcm=False):
        self.num_inspected_items = 0
        self.use_lcm = use_lcm

    @classmethod
    def from_input(cls, input: list[str], use_lcm=False):
        monkey = cls(use_lcm=use_lcm)
        for line in input:
            line = line.strip()
            if line.startswith('Monkey'):
                monkey.index = int(line.split()[1].strip()[:-1])  # remove ':'
            elif line.startswith('Starting'):
                monkey.starting_items = [int(i.strip()) for i in line.split(':')[1].split(',')]
            elif line.startswith('Operation'):
                monkey.operation = line.split('=')[1].strip()
            elif line.startswith('Test'):
                monkey.test = int(line.split('divisible by')[1].strip())
            elif line.startswith('If true'):
                monkey.if_true = int(line.split('monkey')[1].strip())
            elif line.startswith('If false'):
                monkey.if_false = int(line.split('monkey')[1].strip())
            else:
                print(f'Unknown input: {line}')
        return monkey

    def __inspect(self, item):
        self.num_inspected_items += 1
        return eval(self.operation.replace('old', str(item)))  # Could write a parser, but input is known so meh

    def __relief(self, item):
        return item % MonkeyBusiness.lcm if self.use_lcm else int(item//3)

    def __test(self, item):
        return self.if_true if item % self.test == 0 else self.if_false

    def __throw(self, monkey_index, item):
        self.starting_items.pop(0)
        MonkeyBusiness.monkeys[monkey_index].starting_items.append(item)

    def do_turn(self):
        items = self.starting_items[:]
        for item in items:
            _item = self.__relief(self.__inspect(item))
            self.__throw(self.__test(_item), _item)


def split_lines(lines: list[str]):
        chunk = []
        for line in lines:
            if line.strip():
                chunk.append(line)
                continue
            yield chunk
            chunk = []
        if chunk:
            yield chunk


def part1():
    lines = read_input(__file__)
    MonkeyBusiness.monkeys = [Monkey.from_input(chunk) for chunk in split_lines(lines)]
    print(MonkeyBusiness.get_monkey_business(num_rounds=20))


def part2():
    lines = read_input(__file__)
    MonkeyBusiness.monkeys = [Monkey.from_input(chunk, use_lcm=True) for chunk in split_lines(lines)]
    print(MonkeyBusiness.get_monkey_business(num_rounds=10000))


part1()
part2()
