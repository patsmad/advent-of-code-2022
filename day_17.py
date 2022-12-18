from get_input import get_input

day_num = 17
raw_input = get_input(day_num)

test_input = """
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""".strip()

input = raw_input

class Rock:
    def __init__(self, spaces):
        self.spaces = spaces

    def check_left(self, occupied_spaces):
        return all([(space[0] - 1, space[1]) not in occupied_spaces and space[0] > 0 for space in self.spaces])

    def move_left(self):
        self.spaces = [(space[0] - 1, space[1]) for space in self.spaces]

    def check_right(self, occupied_spaces):
        return all([(space[0] + 1, space[1]) not in occupied_spaces and space[0] < 6 for space in self.spaces])

    def move_right(self):
        self.spaces = [(space[0] + 1, space[1]) for space in self.spaces]

    def check_down(self, occupied_spaces):
        return all([(space[0], space[1] - 1) not in occupied_spaces and space[1] > 0 for space in self.spaces])

    def move_down(self):
        self.spaces = [(space[0], space[1] - 1) for space in self.spaces]

    def tallest_point(self):
        return max([space[1] for space in self.spaces])

class Cavern:
    def __init__(self, wind):
        self.wind = wind
        self.repeat_values = {}
        self.reset()

    def reset(self):
        self.tallest_point = -1
        self.number_of_rocks = 0
        self.occupied_spaces = {}
        self.wind_idx = 0

    rock_fncs = [
        lambda i: [(2, i), (3, i), (4, i), (5, i)],
        lambda i: [(2, i + 1), (3, i + 1), (4, i + 1), (3, i), (3, i + 2)],
        lambda i: [(2, i), (3, i), (4, i), (4, i + 1), (4, i + 2)],
        lambda i: [(2, i), (2, i + 1), (2, i + 2), (2, i + 3)],
        lambda i: [(2, i), (3, i), (2, i + 1), (3, i + 1)]
    ]

    def new_rock(self):
        i = self.tallest_point + 4
        return Rock(self.rock_fncs[self.number_of_rocks % 5](i))

    def get_repeat_pattern(self):
        return '\n'.join([''.join([self.occupied_spaces.get((i, j), '.') for i in range(7)]) for j in range(self.tallest_point, self.tallest_point - 10, -1)])

    def move_rock(self, rock):
        settled = False
        while not settled:
            new_wind = self.wind[self.wind_idx]
            self.wind_idx = (self.wind_idx + 1) % len(self.wind)
            if self.wind_idx == 0:
                repeat_pattern = self.get_repeat_pattern()
                if repeat_pattern not in self.repeat_values:
                    self.repeat_values[repeat_pattern] = []
                self.repeat_values[repeat_pattern].append((self.number_of_rocks, self.tallest_point))
            if new_wind == '<':
                if rock.check_left(self.occupied_spaces):
                    rock.move_left()
            else:
                if rock.check_right(self.occupied_spaces):
                    rock.move_right()
            if rock.check_down(self.occupied_spaces):
                rock.move_down()
            else:
                for space in rock.spaces:
                    self.occupied_spaces[space] = '#'
                if rock.tallest_point() > self.tallest_point:
                    self.tallest_point = rock.tallest_point()
                self.number_of_rocks += 1
                settled = True

    def set_repeat_values(self):
        while all([len(repeats) < 2 for repeats in self.repeat_values.values()]):
            rock = self.new_rock()
            self.move_rock(rock)
        self.reset()

    def run(self, total_rocks):
        ((beginning_stones, beginning_tallest), (end_stones, end_tallest)) = [r for r in self.repeat_values.values() if len(r) == 2][0]
        dx = end_stones - beginning_stones
        beginning = (beginning_stones - dx) % dx
        leftover = (total_rocks - beginning) % dx
        cycles = (total_rocks - beginning) // dx

        while self.number_of_rocks < beginning + leftover:
            rock = self.new_rock()
            self.move_rock(rock)
        return self.tallest_point + (end_tallest - beginning_tallest) * cycles + 1

    def __str__(self):
        return '\n'.join([''.join([self.occupied_spaces.get((i, j), '.') for i in range(7)]) for j in range(self.tallest_point, -1, -1)])

# part 1
cavern_1 = Cavern(input)
cavern_1.set_repeat_values()
print(cavern_1.run(2022))

# part 2
cavern_2 = Cavern(input)
cavern_2.set_repeat_values()
print(cavern_2.run(1000000000000))