from get_input import get_input
import re

day_num = 15
raw_input = get_input(day_num)

test_input = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip()

input = raw_input

class Sensor:
    def __init__(self, sx, sy, bx, by):
        self.location = (sx, sy)
        self.closest_beacon = (bx, by)
        self.manhattan_distance = abs(sx - bx) + abs(sy - by)
        self.min_x = sx - self.manhattan_distance
        self.max_x = sx + self.manhattan_distance
        self.min_y = sy - self.manhattan_distance
        self.max_y = sy + self.manhattan_distance

    def within_range(self, x, y):
        return abs(self.location[0] - x) + abs(self.location[1] - y) <= self.manhattan_distance

class Cavern:
    def __init__(self, beacon_input):
        self.sensors = []
        pattern = 'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
        for line in beacon_input.split('\n'):
            self.sensors.append(Sensor(*map(int, re.match(pattern, line).groups())))
        self.beacons = list(set([s.closest_beacon for s in self.sensors]))
        self.min_x = min([sensor.min_x for sensor in self.sensors])
        self.max_x = max([sensor.max_x for sensor in self.sensors])
        self.min_y = min([sensor.min_y for sensor in self.sensors])
        self.max_y = max([sensor.max_y for sensor in self.sensors])

    def filter_sensors(self, y):
        return [s for s in self.sensors if s.min_y <= y and s.max_y >= y]

    def get_space(self, y, sensor):
        dx = sensor.manhattan_distance - abs(sensor.location[1] - y)
        return (sensor.location[0] - dx, sensor.location[0] + dx)

    def unavailable_nodes(self, y):
        unavailable_spaces = [self.get_space(y, s) for s in self.filter_sensors(y)] + \
                             [(b[0], b[0]) for b in self.beacons if b[1] == y]
        unavailable_spaces.sort()
        final_spaces = []
        while len(unavailable_spaces) > 0:
            space = unavailable_spaces.pop(0)
            while len(unavailable_spaces) > 0 and space[1] >= unavailable_spaces[0][0] - 1:
                overlapping_space = unavailable_spaces.pop(0)
                if overlapping_space[1] > space[1]:
                    space = (space[0], overlapping_space[1])
            final_spaces.append(space)
        return final_spaces

# test
c = Cavern(test_input)
N = 10
unavailable_nodes = c.unavailable_nodes(N)
print(unavailable_nodes[0][1] - unavailable_nodes[0][0])

for i in range(2 * N):
    unavailable_nodes = c.unavailable_nodes(i)
    if len(unavailable_nodes) > 1:
        print(4000000 * (max([a[0] for a in unavailable_nodes]) - 1) + i)

# part 1
c = Cavern(raw_input)
N = 2000000
unavailable_nodes = c.unavailable_nodes(N)
print(unavailable_nodes[0][1] - unavailable_nodes[0][0])

# part 2
for i in range(2 * N):
    unavailable_nodes = c.unavailable_nodes(i)
    if len(unavailable_nodes) > 1:
        print(4000000 * (max([a[0] for a in unavailable_nodes]) - 1) + i)
        break
