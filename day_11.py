from get_input import get_input
import re

day_num = 11
raw_input = get_input(day_num)

test_input = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()

input = raw_input

class Monkey:
    def __init__(self, monkey_input, divide_by):
        number_input, items_input, operation_input, test_input, true_input, false_input = monkey_input.split('\n')
        self.number = re.findall('Monkey (\d+):', number_input)[0]
        self.items = list(map(int, items_input.split(': ')[1].split(', ')))
        self.operation_str = operation_input
        self.operation = lambda old: eval(self.operation_str.split('new = ')[1])
        self.test_item = int(re.findall('divisible by (\d+)', test_input)[0])
        self.true_action = re.findall('throw to monkey (\d+)', true_input)[0]
        self.false_action = re.findall('throw to monkey (\d+)', false_input)[0]
        self.inspect_num = 0
        self.divide_by = divide_by
        self.common_factor = 1

    def pop_item_change_worry(self):
        self.inspect_num += 1
        item = self.items.pop(0)
        item = self.operation(item)
        item = item // self.divide_by
        item = item % self.common_factor
        return item

    def add_item(self, item):
        self.items.append(item)

    def throw(self, item):
        return self.true_action if item % self.test_item == 0 else self.false_action

    def __str__(self):
        return 'Monkey {}, items: {}'.format(self.number, ', '.join(map(str, self.items)))

def get_monkeys(input, divide_by):
    monkeys = []
    for monkey_input in input.split('\n\n'):
        monkeys.append(Monkey(monkey_input, divide_by))
    return monkeys

def set_common_factor(monkeys):
    common_factor = 1
    for monkey in monkeys:
        common_factor *= monkey.test_item
    for monkey in monkeys:
        monkey.common_factor = common_factor

def rounds(N, monkeys):
    num_to_monkey = {monkey.number: monkey for monkey in monkeys}
    for _ in range(N):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                item = monkey.pop_item_change_worry()
                throw_to = monkey.throw(item)
                num_to_monkey[throw_to].add_item(item)

def answer(divide_by, N):
    monkeys = get_monkeys(input, divide_by)
    set_common_factor(monkeys)
    rounds(N, monkeys)
    top_two = sorted(monkeys, key=lambda monkey: monkey.inspect_num, reverse=True)[:2]
    return top_two[0].inspect_num * top_two[1].inspect_num

# part 1
print(answer(3, 20))

# part 2

print(answer(1, 10000))
