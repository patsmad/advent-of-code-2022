from get_input import get_input

day_num = 23
raw_input = get_input(day_num)

test_input = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""".strip()

input = raw_input

class Elf:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.possible_moves = [self.north, self.south, self.west, self.east]
        self.start = 0

    def north(self):
        return [(self.x, self.y - 1), (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)]

    def south(self):
        return [(self.x, self.y + 1), (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)]

    def east(self):
        return [(self.x + 1, self.y), (self.x + 1, self.y - 1), (self.x + 1, self.y + 1)]

    def west(self):
        return [(self.x - 1, self.y), (self.x - 1, self.y - 1), (self.x - 1, self.y + 1)]

    def all_directions(self):
        return [(self.x, self.y - 1), (self.x + 1, self.y - 1), (self.x + 1, self.y), (self.x + 1, self.y + 1),
                (self.x, self.y + 1), (self.x - 1, self.y + 1), (self.x - 1, self.y), (self.x - 1, self.y - 1)]

    def proposed_move(self, elf_position_set):
        occupied_positions = set(self.all_directions()) & elf_position_set
        if len(occupied_positions) > 0:
            for i in range(len(self.possible_moves)):
                positions = self.possible_moves[(i + self.start) % len(self.possible_moves)]()
                if len(occupied_positions & set(positions)) == 0:
                    return positions[0]

    def get_matching_move(self, my_move, proposed_moves):
        for elf, move in proposed_moves.items():
            if elf != self and move == my_move:
                return elf

    def move(self, proposed_moves):
        my_move = proposed_moves[self]
        matching_elf = self.get_matching_move(my_move, proposed_moves)
        if matching_elf is None:
            self.x, self.y = my_move[0], my_move[1]
        self.start = (self.start + 1) % len(self.possible_moves)
        return matching_elf is None

    def new_move(self, move):
        if move is not None:
            self.x, self.y = move[0], move[1]
        return move is not None

def print_elves(elves):
    min_x = min([elf.x for elf in elves])
    max_x = max([elf.x for elf in elves])
    min_y = min([elf.y for elf in elves])
    max_y = max([elf.y for elf in elves])
    elf_positions = [(elf.x, elf.y) for elf in elves]
    print('\n'.join([''.join(['#' if (i, j) in elf_positions else '.' for i in range(min_x, max_x + 1)]) for j in range(min_y, max_y + 1)]))

def run_round(elves):
    elf_positions = set([(elf.x, elf.y) for elf in elves])
    proposed_moves = {elf: elf.proposed_move(elf_positions) for elf in elves}

    move_to_elves = {}
    for elf, move in proposed_moves.items():
        if move not in move_to_elves:
            move_to_elves[move] = []
        move_to_elves[move].append(elf)
        elf.start = (elf.start + 1) % len(elf.possible_moves)

    moves = 0
    for move, move_elves in move_to_elves.items():
        if len(move_elves) == 1:
            moves += move_elves[0].new_move(move)
    return moves


# part 1
elves = []
for j, line in enumerate(input.split('\n')):
    for i, maybe_elf in enumerate(line):
        if maybe_elf == '#':
            elves.append(Elf(i, j))

for round in range(10):
    print(round)
    moves = run_round(elves)

min_x = min([elf.x for elf in elves])
max_x = max([elf.x for elf in elves])
min_y = min([elf.y for elf in elves])
max_y = max([elf.y for elf in elves])

print((max_x - min_x + 1) * (max_y - min_y + 1) - len(elves))

# part 2

elves = []
for j, line in enumerate(input.split('\n')):
    for i, maybe_elf in enumerate(line):
        if maybe_elf == '#':
            elves.append(Elf(i, j))

moves = 1
round = 0
while moves != 0:
    round += 1
    moves = run_round(elves)
    if round % 100 == 0:
        print(round, moves)
print(round, moves)
