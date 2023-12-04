"""https://adventofcode.com/2022/day/7"""

from utils import read_input, read_example_input


class File:
    def __init__(self, name: str, parent: 'File', size=0):
        self.name = name
        self.parent = parent
        self.size = size

    def __str__(self) -> str:
        return f'{self.name} (file, size={self.size})'


class Directory(File):
    def __init__(self, name: str, parent: File=None, children: list[File]=None):
        super().__init__(name, parent=parent)

        self.children = children if children else []

    def __str__(self) -> str:
        return f'{self.name} (dir)'


class FileSystem:
    root: Directory
    cd: Directory

    def __init__(self, lines: list[str]):
        self.root = None

        for line in lines:
            segments = line.strip().split()
            if segments[0] == '$':
                self.__parse_command(segments[1:])
            else:
                # `ls` is the only command that generates output in this scenario
                self.__parse_command_output(segments)

    def __parse_command(self, command: list[str]):
        if command[0] != 'cd':
            return

        if command[1] == '/':
            if not self.root:
                self.root = Directory(command[1])
            self.cd = self.root
            return

        if command[1] == '..':
            self.cd = self.cd.parent
            return

        for c in self.cd.children:
            if not isinstance(c, Directory):
                continue
            if c.name == command[1]:
                self.cd = c
                return

    def __parse_command_output(self, output: list[str]):
        new_child = None
        if output[0] == 'dir':
            new_child = Directory(output[1], parent=self.cd)
        else:
            new_child = File(output[1], parent=self.cd, size=int(output[0]))
        if new_child:
            self.cd.children.append(new_child)

    @property
    def cwd(self):
        cd = self.cd
        cwd = [cd.name]
        while cd.parent:
            cd = cd.parent
            cwd.append(cd.name)
        return cwd.reverse()

    def __print_w_indent(self, msg: str, indent=0):
        print(('  ' * indent) + f'- {msg}')

    def __print_directory(self, directory: Directory, indent=0):
        self.__print_w_indent(str(directory), indent=indent)
        for child in directory.children:
            if isinstance(child, Directory):
                self.__print_directory(child, indent=indent+1)
            else:
                self.__print_w_indent(str(child), indent=indent+1)

    def print(self):
        self.__print_directory(self.root)

    def get_subdirectories(self, directory: Directory=None, recursive=False):
        if not directory:
            directory = self.root
        if not recursive:
            return directory.children
        dirs = [directory]
        for object in directory.children:
            if not isinstance(object, Directory):
                continue
            dirs.extend(self.get_subdirectories(object, recursive=recursive))
        return dirs

    def calculate_directory_size(self, directory: Directory=None):
        if not directory:
            directory = self.root
        total_size = 0
        for object in directory.children:
            if isinstance(object, Directory):
                total_size += self.calculate_directory_size(object)
            else:
                total_size += object.size
        return total_size


def part1():
    lines = read_input(__file__)
    fs = FileSystem(lines)
    #fs.print()

    total_size = 0
    dirs = fs.get_subdirectories(recursive=True)
    for d in dirs:
        size = fs.calculate_directory_size(d)
        if size <= 100000:
            total_size += size
    print(total_size)


def part2():
    lines = read_input(__file__)
    fs = FileSystem(lines)
    #fs.print()

    total_space_available = 70000000
    total_space_required = 30000000
    unused_space = total_space_available - fs.calculate_directory_size()
    space_needed = total_space_required - unused_space

    dirs = fs.get_subdirectories(recursive=True)
    smallest_dir = None
    smallest_size = -1
    for d in dirs:
        size = fs.calculate_directory_size(d)
        if not smallest_dir or (size > space_needed and size < smallest_size):
            smallest_dir = d
            smallest_size = size
    print(smallest_size)


part1()
part2()
