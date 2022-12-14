from get_input import get_input

day_num = 13
raw_input = get_input(day_num)

test_input = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()

input = raw_input.split('\n\n')

def compare_ints(left, right):
    return 1 if left < right else -1 if left > right else 0

def compare_list_list(left, right):
    for left_item, right_item in zip(left, right):
        comparison = choose_compare[type(left_item), type(right_item)](left_item, right_item)
        if comparison != 0:
            return comparison
    return 1 if len(left) < len(right) else -1 if len(left) > len(right) else 0

def compare_int_list(left, right):
    return compare_list_list([left], right)

def compare_list_int(left, right):
    return compare_list_list(left, [right])

choose_compare = {
    (int, int): compare_ints,
    (int, list): compare_int_list,
    (list, int): compare_list_int,
    (list, list): compare_list_list
}

class InputUnit:
    def __init__(self, input_str):
        self.input_unit = eval(input_str)

    def compare(self, other_unit):
        return compare_list_list(self.input_unit, other_unit.input_unit)

# part 1
pairs = [list(map(InputUnit, pair.split('\n'))) for pair in input]
s = 0
for i, pair in enumerate(pairs):
    if pair[0].compare(pair[1]) == 1:
        s += i + 1
print(s)

# part 2
all_units = [a for b in pairs for a in b]
unit_6 = InputUnit('[[6]]')
unit_2 = InputUnit('[[2]]')
value_6 = sum([unit_6.compare(unit) == -1 for unit in all_units + [unit_2]]) + 1
value_2 = sum([unit_2.compare(unit) == -1 for unit in all_units + [unit_6]]) + 1
print(value_6 * value_2)
