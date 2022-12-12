from get_input import get_input

day_num = 12
raw_input = get_input(day_num)

test_input = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()

input = test_input

# part 1

class Node:
    def __init__(self, letter):
        self.elevation = self.get_elevation(letter)
        self.shorted_path_length = None
        self.shorted_path_node = None
        self.edges = []

    def get_elevation(self, letter):
        if letter not in ['S', 'E']:
            return ord(letter)
        elif letter == 'S':
            return ord('a')
        else:
            return ord('z')

nodes = {}
for i in range(len(input)):
    for j in range(len(input[i])):
        nodes[(i,j)] = Node(input[i][j])
        if i > 0:
            if nodes[(i,j)].elevation >= nodes[(i-1,j)].elevation:
                nodes[(i, j)].edges.append(nodes[(i-1,j)])
            if nodes[(i,j)].elevation <= nodes[(i-1,j)].elevation:
                nodes[(i-1,j)].edges.append(nodes[(i, j)])
        if j > 0:
            if nodes[(i, j)].elevation >= nodes[(i, j-1)].elevation:
                nodes[(i, j)].edges.append(nodes[(i, j-1)])
            if nodes[(i, j)].elevation <= nodes[(i, j-1)].elevation:
                nodes[(i, j-1)].edges.append(nodes[(i, j)])

q = []
print(nodes)

# part 2
