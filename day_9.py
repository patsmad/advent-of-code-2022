from get_input import get_input

day_num = 9
raw_input = get_input(day_num)

test_input = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""".strip()

def move_head(x, y, direction):
    if direction[0] == 'R':
        x += 1
    elif direction[0] == 'L':
        x -= 1
    elif direction[0] == 'D':
        y += 1
    else:
        y -= 1
    return x, y

def follow(Hx, Hy, Tx, Ty):
    if Hx - Tx == 2:
        Tx += 1
        Ty += (Hy > Ty) - (Hy < Ty)
    elif Hx - Tx == -2:
        Tx -= 1
        Ty += (Hy > Ty) - (Hy < Ty)
    elif Hy - Ty == 2:
        Tx += (Hx > Tx) - (Hx < Tx)
        Ty += 1
    elif Hy - Ty == -2:
        Tx += (Hx > Tx) - (Hx < Tx)
        Ty -= 1
    return Tx, Ty

def run(num_knots, input):
    knots = [(0, 0) for _ in range(num_knots)]
    visited_sites = [knots[-1]]
    for move in input.split('\n'):
        direction, steps = move.strip().split(' ')
        for step in range(int(steps)):
            knots[0] = move_head(knots[0][0], knots[0][1], direction)
            for i in range(1, len(knots)):
                knots[i] = follow(knots[i - 1][0], knots[i - 1][1], knots[i][0], knots[i][1])
            visited_sites.append(knots[-1])
    return visited_sites

# part 1
input = raw_input
print(len(set(run(2, input))))

# part 2

print(len(set(run(10, input))))
