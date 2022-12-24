from get_input import get_input

day_num = 24
raw_input = get_input(day_num)

test_input = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".strip()

input = raw_input

class Blizzard:
    movement = {
        '^': (0, -1),
        'v': (0, 1),
        '>': (1, 0),
        '<': (-1, 0)
    }

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def position(self, minute, width, height):
        return ((self.x + minute * self.movement[self.direction][0]) % width, (self.y + minute * self.movement[self.direction][1]) % height)

class Map:
    def __init__(self, map_input):
        split_input = map_input.split('\n')
        self.width = len(split_input[0][1:-1])
        self.height = len(split_input[1:-1])
        self.blizzards = []
        for j, line in enumerate(split_input[1:-1]):
            for i, position in enumerate(line[1:-1]):
                if position != '.':
                    self.blizzards.append(Blizzard(i, j, position))
        self.walls = set([(-1, i) for i in range(-1, self.height + 1)] +
                     [(self.width, i) for i in range(-1, self.height + 1)] +
                     [(i, -1) for i in range(1, self.width)] +
                     [(i, self.height) for i in range(self.width - 1)] +
                     [(0, -2), (self.width - 1, self.height + 1)])
        self.end = (self.width - 1, self.height)
        self.start = (0, -1)

    def filter_blizzards(self, x, y):
        return [b for b in self.blizzards if (abs(b.x - x) <= 1 and b.direction in ['v', '^']) or (abs(b.y - y) <= 1 and b.direction in ['<', '>'])]

    def print_map(self, minute):
        blizzard_positions = {b.position(minute, m.width, m.height): b.direction for b in self.blizzards}
        print('\n'.join([''.join(['.' if (i, j) not in blizzard_positions else blizzard_positions[i, j] for i in range(self.width)]) for j in range(self.height)]))

class PlayerState:
    def __init__(self, x, y, minute):
        self.x = x
        self.y = y
        self.minute = minute

    def next_states(self):
        return [(self.x + 1, self.y), (self.x, self.y + 1), (self.x - 1, self.y), (self.x, self.y - 1), (self.x, self.y)]

def trip(m, minute, start, end):
    queue = [PlayerState(start[0], start[1], minute)]
    seen_states = set()
    while len(queue) > 0:
        state = queue.pop(0)
        if (state.x, state.y) == end:
            return state.minute
        possible_blizzards = m.filter_blizzards(state.x, state.y)
        next_blizzard_positions = {b.position(state.minute + 1, m.width, m.height) for b in possible_blizzards} | m.walls
        possible_next_positions = {s for s in state.next_states()}
        next_states = {(p[0], p[1], state.minute + 1) for p in possible_next_positions - next_blizzard_positions}
        for next_state in next_states - seen_states:
            queue.append(PlayerState(next_state[0], next_state[1], next_state[2]))
        seen_states |= next_states


m = Map(input)

# part 1
minutes = trip(m, 0, m.start, m.end)
print(minutes)

# part 2
minutes = trip(m, minutes, m.end, m.start)
minutes = trip(m, minutes, m.start, m.end)
print(minutes)