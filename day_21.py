from get_input import get_input

day_num = 21
raw_input = get_input(day_num)

test_input = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip()

input = raw_input

class Monkeys:
    def __init__(self, input):
        self.lambdas = {}
        for line in input.split('\n'):
            split_line = line.split(' ')
            name, operation = self.process_line(split_line)
            if name == 'root':
                self.root_left = split_line[1]
                self.root_right = split_line[3]
            self.lambdas[name] = operation

    def process_line(self, split_line):
        if len(split_line) == 2:
            return split_line[0][:-1], lambda: int(split_line[1])
        else:
            if '+' == split_line[2]:
                return split_line[0][:-1], lambda: self.lambdas[split_line[1]]() + self.lambdas[split_line[3]]()
            elif '-' == split_line[2]:
                return split_line[0][:-1], lambda: self.lambdas[split_line[1]]() - self.lambdas[split_line[3]]()
            elif '*' == split_line[2]:
                return split_line[0][:-1], lambda: self.lambdas[split_line[1]]() * self.lambdas[split_line[3]]()
            elif '/' == split_line[2]:
                return split_line[0][:-1], lambda: self.lambdas[split_line[1]]() // self.lambdas[split_line[3]]()

# part 1
m = Monkeys(input)
print(m.lambdas['root']())

# part 2
m.lambdas['root'] = lambda: m.lambdas[m.root_left]() == m.lambdas[m.root_right]()
m.lambdas['humn'] = lambda: 0
diff = m.lambdas[m.root_left]() - m.lambdas[m.root_right]()
m.lambdas['humn'] = lambda: 1000
new_diff = m.lambdas[m.root_left]() - m.lambdas[m.root_right]()
slope = (new_diff - diff) / 1000
test_change = - int(diff / slope)
m.lambdas['humn'] = lambda: test_change
print(m.lambdas['root']())
print(test_change)
