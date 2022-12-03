from get_input import get_input

day_num = 3
raw_input = get_input(day_num)

test_input = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".strip()

input = raw_input

elves_backpacks = input.split('\n')

# part 1

def split_compartments(bag):
    mid_point = len(bag) // 2
    return bag[:mid_point], bag[mid_point:]

def get_shared_items(lists):
    return set.intersection(*map(set, lists))

def get_item_priority(item):
    return ord(item.upper()) - 64 + (item.upper() == item) * 26

def get_priority(shared_items):
    return sum([get_item_priority(shared_item) for shared_item in shared_items])

shared_items = [get_shared_items(split_compartments(elf_backpack)).pop() for elf_backpack in elves_backpacks]
print(get_priority(shared_items))

# part 2
shared_items = [get_shared_items(elves_backpacks[i:i+3]).pop() for i in range(0, len(elves_backpacks), 3)]
print(get_priority(shared_items))
