from get_input import get_input

day_num = 10
raw_input = get_input(day_num)

test_input = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".strip()

input = raw_input

class Computer:
    def __init__(self, instructions):
        self.values = self.process(instructions)

    def process(self, instructions):
        values = [1]
        for instruction in instructions.split('\n'):
            if instruction == 'noop':
                values.append(values[-1])
            else:
                values.append(values[-1])
                values.append(values[-1] + int(instruction.split(' ')[1]))
        return values

    def part1(self):
        s = 0
        for d in [20, 60, 100, 140, 180, 220]:
            s += d * c.values[d - 1]
        return s

    def draw(self):
        pixels = ['#' if abs(i % 40 - self.values[i] % 40) <= 1 else '.' for i in range(240)]
        print('\n'.join([''.join(pixels[(i-1)*40:i*40]) for i in range(7)]))

c = Computer(input)

# part 1
print(c.part1())

# part 2
c.draw()
