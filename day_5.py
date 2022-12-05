import re
from get_input import get_input

day_num = 5
raw_input = get_input(day_num, strip=False)

test_input = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

input = raw_input

crates, movements = input.split('\n\n')

def process_instructions(movements_input):
    processes_movements = []
    for movement in movements_input.strip().split('\n'):
        processes_movements.append(tuple(map(int, re.findall('move ([0-9]*) from ([0-9]*) to ([0-9]*)', movement)[0])))
    return processes_movements

instructions = process_instructions(movements)

class Crane:
    def __init__(self, crate_input, move_fnc):
        self.stacks = self.process_crates(crate_input)
        self.ordered_idx = sorted(self.stacks.keys())
        self.move_fnc = move_fnc

    @staticmethod
    def process_crates(crate_input):
        lines = crate_input.split('\n')
        pile_indices = {int(value): idx for idx, value in enumerate(lines[-1]) if re.match('[0-9]{1}', value)}
        stacks = {idx: [] for idx in pile_indices}
        for line in lines[:-1][::-1]:
            for value, idx in pile_indices.items():
                if idx < len(line) and line[idx] != ' ':
                    stacks[value].append(line[idx])
        return stacks

    def move(self, instruction):
        self.stacks = self.move_fnc(self.stacks, instruction)

    def all_moves(self, instructions):
        for instruction in instructions:
            self.move(instruction)

    def output(self):
        return ''.join([self.stacks[i][-1] for i in self.ordered_idx])

def move9000(stacks, instruction):
    num, from_crate, to_crate = instruction
    for _ in range(num):
        stacks[to_crate].append(stacks[from_crate].pop())
    return stacks

def move9001(stacks, instruction):
    num, from_crate, to_crate = instruction
    temp_stack = []
    for _ in range(num):
        temp_stack.append(stacks[from_crate].pop())
    while len(temp_stack) > 0:
        stacks[to_crate].append(temp_stack.pop())
    return stacks

# part 1
crane = Crane(crates, move9000)
crane.all_moves(instructions)
print(crane.output())

# part 2
crane = Crane(crates, move9001)
crane.all_moves(instructions)
print(crane.output())
