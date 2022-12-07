from get_input import get_input

class Directory:
    def __init__(self, name, parent_directory=None):
        self.name = name
        self.parent_directory = parent_directory
        self.dir = []
        self.files = {}

    def sum(self):
        return sum(self.files.values()) + sum([d.sum() for d in self.dir])

    def find_dir(self, dir):
        matching_directories = [d for d in self.dir if d.name == dir]
        if len(matching_directories) > 0:
            return matching_directories[0]

    def all_sub_dir(self):
        sub_dirs = [self]
        for d in self.dir:
            sub_dirs += d.all_sub_dir()
        return sub_dirs

    def __str__(self):
        parent = self.parent_directory.name if self.parent_directory is not None else 'None'
        sub_dir = ', '.join([d.name for d in self.dir]) if len(self.dir) > 0 else 'None'
        files = ', '.join([f'{file_name} ({file_size})' for file_name, file_size in self.files.items()])
        return f'{self.name}; parent: {parent}; sub_dir: {sub_dir}; files: {files}; sum: {self.sum()}'

class Computer:
    def __init__(self, current_directory, commands):
        self.commands = commands.split('\n')
        self.i = 1 # First line is just setting current_directory
        self.current_directory = current_directory

    def cd(self, line):
        new_directory = line.split('$ cd ')[1]
        if new_directory == '..':
            self.current_directory = self.current_directory.parent_directory
        else:
            self.current_directory = self.current_directory.find_dir(new_directory)

    def ls_dir(self, line):
        new_directory = Directory(line.split('dir ')[1], self.current_directory)
        if self.current_directory.find_dir(new_directory.name) is None:
            self.current_directory.dir.append(new_directory)

    def ls_file(self, line):
        file_size, file_name = line.split(' ')
        self.current_directory.files[file_name] = int(file_size)

    def ls(self):
        while self.i < len(self.commands) - 1 and self.commands[self.i + 1][0] != '$':
            self.i += 1
            line = self.commands[self.i].strip()
            if line[:4] == 'dir ':
                self.ls_dir(line)
            else:
                self.ls_file(line)

    def run(self):
        while self.i < len(self.commands):
            line = self.commands[self.i].strip()
            if line[:5] == '$ cd ':
                self.cd(line)
            elif line[:4] == '$ ls':
                self.ls()
            self.i += 1

    def part_1(self):
        return sum([d.sum() for d in top_directory.all_sub_dir() if d.sum() <= 100000])

    def part_2(self):
        unused_needed = 70000000 - top_directory.sum()
        space_needed = 30000000 - unused_needed
        return sorted([d for d in top_directory.all_sub_dir() if d.sum() > space_needed], key=lambda d: d.sum())[0].sum()


day_num = 7
raw_input = get_input(day_num)

test_input = """
$ cd /
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
7214296 k
""".strip()

input = raw_input
top_directory = Directory('/')
computer = Computer(top_directory, input)
computer.run()

# part 1
print(computer.part_1())

# part 2
print(computer.part_2())