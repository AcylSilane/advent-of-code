"""Solution to day 7"""
from __future__ import annotations
from typing import Optional, List, TextIO, Dict


class Node:
    """A node of a filesystem, e.g. a directory or a file."""

    def __init__(self, name: str, parent: Optional[Node], size=0):
        self.name = name
        self.parent = parent
        self.children = []
        self.size = size
        if self.parent:
            self.parent.add_node(self)

    def add_node(self, other: Node):
        self.children.append(other)
        self.calculate_size()

    def calculate_size(self, propagate=True):
        self.size = sum([child.size for child in self.children])
        self.parent.calculate_size()

    def __getitem__(self, node: str) -> Node:
        for child in self.children:
            if child.name == node:
                return child
        else:
            raise FileNotFoundError(f"{node} in {self} was not found.")

    def __repr__(self) -> str:
        return f"<{self.__class__} at {id(self)}, name={self.name}, " + \
               f"parent={self.parent.name if self.parent else None}, size={self.size}," + \
               f"children={[child.name for child in self.children]}>"


class Root(Node):
    def __init__(self):
        super().__init__(name="/", parent=None)

    def calculate_size(self, propagate=True):
        self.size = sum([child.size for child in self.children])


class File(Node):
    """A file on the system."""

    def __init__(self, name: str, parent: Node, size: int):
        super().__init__(name=name, parent=parent, size=size)


class Filesystem:
    """A filesystem, basically a tree with extra steps."""

    def __init__(self, fp: TextIO):
        self.fp = fp
        self.root = Root()
        self.working_directory = self.root
        self.seen = [self.root]

        self.commands = {
            "cd": self.change_directory,
            "ls": self.list_stuff
        }

    def consume_command(self, command=None) -> Filesystem:
        if self.fp.closed:
            return self

        if command is None and self.fp:
            command = self.fp.readline()

        argv = command.strip().split()
        self.commands[argv[1]](argv[1:])
        return self

    def change_directory(self, argv: List[str]) -> Filesystem:
        directory = argv[1]
        if directory == "/":
            self.working_directory = self.root
        elif directory == "..":
            self.working_directory = self.working_directory.parent
        else:
            self.working_directory = self.working_directory[directory]
        return self

    def list_stuff(self, argv: List[str]) -> Filesystem:
        while not self.fp.closed:
            line = self.fp.readline()

            if not line:
                self.fp.close()
            elif line.startswith("$"):
                self.consume_command(line)
                break
            elif line.startswith("dir"):
                dirname = line.strip().split()[-1]
                new_node = Node(name=dirname, parent=self.working_directory)
                self.seen.append(new_node)
            else:
                size, filename = line.strip().split()
                File(name=filename, parent=self.working_directory, size=int(size))
        return self

    def get_directory_sizes(self, ptr=None, memo=None) -> Dict[str, int]:

        dirs = {}
        if not ptr:
            ptr = self.root

        if not isinstance(ptr, File):
            dirs[ptr.name] = ptr.size

        for child in ptr.children:
            dirs.update(self.get_directory_sizes(ptr=child))

        return dirs

    def draw(self, ptr=None, indent=0) -> None:
        if ptr is None:
            ptr = self.root

        print("   " * indent + "|--" + f"{ptr.name}, {ptr.size}")
        for child in ptr.children:
            self.draw(ptr=child, indent=indent + 1)


if __name__ == "__main__":
    TOTAL_DISK = 70000000
    REQUIRED_SPACE = 30000000
    with open("input.log", "r") as inp:
        fs = Filesystem(inp)
        while not inp.closed:
            fs.consume_command()

    current_space = TOTAL_DISK - fs.root.size
    missing_space = REQUIRED_SPACE - current_space

    print(f"Part 1: {sum([node.size for node in fs.seen if node.size <= 100000])}")

    print(f"Part 2: {min([node for node in fs.seen if node.size >= missing_space], key=lambda node: node.size).size}")

