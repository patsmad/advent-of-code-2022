from get_input import get_input

day_num = 6
raw_input = get_input(day_num)

test_input = """
mjqjpqmgbljsphdztnvjfqwrcgsmlb
""".strip()

input = raw_input

# part 1

def remove_value(c_dict, value):
    remaining_value = c_dict.pop(value)
    if remaining_value > 1:
        c_dict[value] = remaining_value - 1
    return c_dict

def find_unique_start(data, unique_c):
    i = 0
    c_dict = {}
    while len(c_dict) != unique_c:
        c_dict[data[i]] = c_dict.get(data[i], 0) + 1
        if i >= unique_c:
            c_dict = remove_value(c_dict, data[i - unique_c])
        i += 1
    return i

print(find_unique_start(input, 4))

# part 2
print(find_unique_start(input, 14))
