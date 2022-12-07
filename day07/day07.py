from __future__ import annotations


TEST_INPUT = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

TOTAL_SPACE = 70000000
SPACE_NEEDED = 30000000


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def __repr__(self):
        return f"File({self.name}, size={self.size})"

    def get_size(self) -> int:
        return self.size


class Dir:
    def __init__(self, name: str):
        self.name = name
        self.subdirs = []
        self.files = []

    def __repr__(self):
        return f"Dir({self.name})"

    def add_subdir(self, subdir: Dir):
        self.subdirs.append(subdir)

    def add_file(self, file: File):
        self.files.append(file)

    def get_size(self) -> int:
        return sum(file.get_size() for file in self.files) + sum(
            subdir.get_size() for subdir in self.subdirs
        )


class FileSystem:
    def __init__(self):
        self.dirs = {}

    def __repr__(self):
        return f"FileSystem({self.dirs})"

    def dir_exist(self, dir_name: str) -> bool:
        return dir_name in self.dirs.keys()

    def add_dir(self, dir: Dir):
        self.dirs[dir.name] = dir

    def add_subdir(self, dir_name: str, subdir: Dir):
        self.dirs[dir_name].add_subdir(subdir)

    def add_file(self, dir_name: str, file: File):
        self.dirs[dir_name].add_file(file)

    def get_dir(self, dir_name: str) -> Dir:
        return self.dirs[dir_name]

    def get_total_size(self) -> int:
        return self.dirs["/"].get_size()

    def get_total_size_less_than(self, max_size: int) -> int:
        return sum(
            dir.get_size() for dir in self.dirs.values() if dir.get_size() <= max_size
        )

    def get_smallest_dir_greater_than(self, min_size: int) -> Dir:
        return min(
            (dir for dir in self.dirs.values() if dir.get_size() >= min_size),
            key=lambda dir: dir.get_size(),
        )


def create_filesystem(input: str) -> FileSystem:
    commands = input.splitlines()
    path = []
    filesystem = FileSystem()
    for command in commands:
        if command.startswith("$ cd"):
            dir_name = command.split("cd")[1].strip()
            if dir_name == "..":
                path.pop()
            else:
                path.append(dir_name)
        elif command.startswith("$ ls"):
            dir_name = "/".join(path).replace("//", "/")
            if not filesystem.dir_exist(dir_name):
                filesystem.add_dir(Dir(dir_name))
        elif command.startswith("dir"):
            dir_name = ("/".join(path) + "/" + command.split("dir")[1].strip()).replace(
                "//", "/"
            )
            parent_dir_name = "/".join(path).replace("//", "/")
            filesystem.add_dir(Dir(dir_name))
            filesystem.add_subdir(parent_dir_name, filesystem.get_dir(dir_name))
        else:
            file_size = int(command.split(" ")[0])
            file_name = command.split(" ")[1]
            dir_name = "/".join(path).replace("//", "/")
            filesystem.add_file(dir_name, File(file_name, file_size))
    return filesystem


test_filesystem = create_filesystem(TEST_INPUT)
assert test_filesystem.get_total_size_less_than(100000) == 95437

unused_space = TOTAL_SPACE - test_filesystem.get_total_size()
space_to_delete = SPACE_NEEDED - unused_space
assert (
    test_filesystem.get_smallest_dir_greater_than(space_to_delete).get_size()
    == 24933642
)


with open("input.txt") as f:
    filesystem = create_filesystem(f.read())
    print(filesystem.get_total_size_less_than(100000))
    unused_space = TOTAL_SPACE - filesystem.get_total_size()
    space_to_delete = SPACE_NEEDED - unused_space
    print(filesystem.get_smallest_dir_greater_than(space_to_delete).get_size())
