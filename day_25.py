from get_input import get_input
import math

day_num = 25
raw_input = get_input(day_num)

test_input = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""".strip()

input = raw_input

to_numbers = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}

to_string = {
    -2: '=',
    -1: '-',
    0: '0',
    1: '1',
    2: '2'
}

# part 1

s = 0
for line in input.split('\n'):
    numbers = [to_numbers[a] for a in line]
    s += sum([5**(len(numbers) - i - 1) * n for i, n in enumerate(numbers)])

out = []
for i in range(int(math.log(s, 5)) + 1):
    val = (s % (5**(i+1))) // 5**i
    val = val - 5 * (val > 2)
    s -= val * 5**i
    out.append(to_string[val])
print(''.join(out[::-1]))

# part 2
