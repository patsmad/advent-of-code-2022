from get_input import get_input

day_num = 1
raw_input = get_input(day_num)
# part 1
sorted_calories = sorted([sum(map(int, elf_food.split('\n'))) for elf_food in raw_input.strip().split('\n\n')])
print(sorted_calories[-1])

# part 2
print(sum(sorted_calories[-3:]))
