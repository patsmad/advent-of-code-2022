from get_input import get_input

day_num = 4
raw_input = get_input(day_num)

test_input = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip()

input = raw_input

# part 1

class ElfRange:
    def __init__(self, pair):
        self.left, self.right = map(int, pair.split('-'))

    def contains(self, other):
        return self.left <= other.left and self.right >= other.right

    def overlap_side(self, other_side):
        return self.left <= other_side and self.right >= other_side

    def overlap(self, other):
        return self.overlap_side(other.left) or self.overlap_side(other.right)

    def __str__(self):
        return f'{self.left}-{self.right}'

class ElfPair:
    def __init__(self, raw_pair):
        self.left_elf, self.right_elf = map(ElfRange, raw_pair.split(','))

    def contains(self):
        return self.left_elf.contains(self.right_elf) or self.right_elf.contains(self.left_elf)

    def overlap(self):
        return self.left_elf.overlap(self.right_elf) or self.right_elf.contains(self.left_elf)

    def __str__(self):
        return f'{self.left_elf},{self.right_elf}'

elf_pairs = [ElfPair(pair) for pair in input.split('\n')]
print(sum([pair.contains() for pair in elf_pairs]))

# part 2
print(sum([pair.overlap() for pair in elf_pairs]))
