from get_input import get_input

day_num = 14
raw_input = get_input(day_num)

test_input = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip()

input = raw_input

class Cavern:
    def __init__(self, cavern_input, with_floor):
        self.input = cavern_input
        self.occupied_spots = {}
        for line in cavern_input.split('\n'):
            points = [tuple(map(int, point.split(','))) for point in line.split(' -> ')]
            current = points[0]
            for point in points[1:]:
                dx = (current[0] < point[0]) - (current[0] > point[0])
                if dx != 0:
                    for i in range(current[0], point[0] + dx, dx):
                        self.occupied_spots[(i, current[1])] = '#'
                dy = (current[1] < point[1]) - (current[1] > point[1])
                if dy != 0:
                    for j in range(current[1], point[1] + dy, dy):
                        self.occupied_spots[(current[0], j)] = '#'
                current = point
        self.min_x = min([a[0] for a in self.occupied_spots.keys()])
        self.max_x = max([a[0] for a in self.occupied_spots.keys()])
        self.min_y = min([a[1] for a in self.occupied_spots.keys()])
        self.max_y = max([a[1] for a in self.occupied_spots.keys()])
        if with_floor:
            self.max_y += 2
            for i in range(self.min_x - self.max_y, self.max_x + self.max_y):
                self.occupied_spots[(i, self.max_y)] = '#'
            self.min_x = self.min_x - self.max_y
            self.max_x = self.max_x + self.max_y
        self.sand = 0

    def __str__(self):
        return '\n'.join([''.join([self.occupied_spots.get((i, j), '.') for i in range(self.min_x, self.max_x + 1)]) for j in range(self.min_y, self.max_y + 1)])

    def new_position(self, position):
        if (position[0], position[1] + 1) not in self.occupied_spots:
            return (position[0], position[1] + 1)
        if (position[0] - 1, position[1] + 1) not in self.occupied_spots:
            return (position[0] - 1, position[1] + 1)
        if (position[0] + 1, position[1] + 1) not in self.occupied_spots:
            return (position[0] + 1, position[1] + 1)

    def add_sand(self):
        sand_position = (500, 0)
        new_sand_position = self.new_position(sand_position)
        while sand_position[1] < self.max_y and new_sand_position is not None:
            sand_position = new_sand_position
            new_sand_position = self.new_position(sand_position)
        if sand_position[1] < self.max_y and sand_position not in self.occupied_spots:
            return sand_position

    def add_all_sand(self):
        sand_position = self.add_sand()
        while sand_position is not None:
            self.sand += 1
            self.occupied_spots[sand_position] = 'o'
            sand_position = self.add_sand()



# part 1
cavern = Cavern(input, with_floor=False)

cavern.add_all_sand()
print(cavern.sand)

# part 2

cavern = Cavern(input, with_floor=True)

cavern.add_all_sand()
print(cavern.sand)