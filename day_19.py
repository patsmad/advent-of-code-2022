from get_input import get_input
import re

day_num = 19
raw_input = get_input(day_num)

test_input = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip()

input = raw_input

class Factory:
    pattern = "Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."

    def __init__(self, blueprint, max_value):
        self.id, self.costs = self.process_input(*map(int, re.match(self.pattern, blueprint).groups()))
        self.max_value = max_value
        # Max robot is because it is pointless to make more robots than the maximum cost for any robot for that object
        self.max_robot = [max([a[0] for a in self.costs]), max([a[1] for a in self.costs]), max([a[2] for a in self.costs]), self.max_value + 1]
        self.max_found = 0

    def process_input(self, id, ore_ore_cost, clay_ore_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost):
        return id, [[ore_ore_cost, 0, 0, 0], [clay_ore_cost, 0, 0, 0], [obsidian_ore_cost, obsidian_clay_cost, 0, 0], [geode_ore_cost, 0, geode_obsidian_cost, 0]]

    def can_make_robot(self, stock, next_robot):
        return all([self.costs[next_robot][i] <= stock[i] for i in range(3)])

    def find_maximum_geode(self, minute, stock, robots, next_robot):
        # Bounce if even when you make a geode robot every minute for the rest of the time you can't beat your current best
        if stock[3] + (robots[3] + self.max_value - minute) * (robots[3] + self.max_value - minute + 1) / 2 <= self.max_found:
            return stock[3] + robots[3]
        if minute == self.max_value:
            if stock[3] + robots[3] > self.max_found:
                self.max_found = stock[3] + robots[3]
            return stock[3] + robots[3]
        if not self.can_make_robot(stock, next_robot):
            return self.find_maximum_geode(minute + 1, [stock[i] + robots[i] for i in range(4)], robots, next_robot)
        else:
            new_stocks = [stock[i] + robots[i] - self.costs[next_robot][i] for i in range(4)]
            new_robots = [robots[i] + (i == next_robot) for i in range(4)]
            return max([self.find_maximum_geode(minute + 1, new_stocks, new_robots, j) for j in range(4) if new_robots[j] < self.max_robot[j]])

# part 1
import time
t = time.time()
s = 0
for blueprint in input.split('\n'):
    print(blueprint)
    factory = Factory(blueprint, 24)
    max_value = max([factory.find_maximum_geode(1, [0, 0, 0, 0], [1, 0, 0, 0], i) for i in range(2)])
    s += factory.id * max_value
    print(factory.id, max_value)
print(s)
print(time.time() - t)
print()


# part 2
t = time.time()
p = 1
for blueprint in input.split('\n')[:3]:
    print(blueprint)
    factory = Factory(blueprint, 32)
    max_value = max([factory.find_maximum_geode(1, [0, 0, 0, 0], [1, 0, 0, 0], i) for i in range(2)])
    p *= max_value
    print(factory.id, max_value)
print(p)
print(time.time() - t)
