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

input = raw_input.split('\n')

# part 1

class Node:
    def __init__(self, letter):
        self.letter = letter
        self.elevation = self.get_elevation(self.letter)
        self.is_start = self.letter == 'S'
        self.is_end = self.letter == 'E'
        self.steps = None
        self.edges = []

    def get_elevation(self, letter):
        if letter not in ['S', 'E']:
            return ord(letter)
        elif letter == 'S':
            return ord('a')
        else:
            return ord('z')

def get_nodes(input):
    input_nodes = {}
    for i in range(len(input)):
        for j in range(len(input[i])):
            input_nodes[(i, j)] = Node(input[i][j])
            if i > 0:
                if input_nodes[(i, j)].elevation >= input_nodes[(i-1, j)].elevation - 1:
                    input_nodes[(i, j)].edges.append(input_nodes[(i-1, j)])
                if input_nodes[(i, j)].elevation <= input_nodes[(i-1, j)].elevation + 1:
                    input_nodes[(i-1, j)].edges.append(input_nodes[(i, j)])
            if j > 0:
                if input_nodes[(i, j)].elevation >= input_nodes[(i, j-1)].elevation - 1:
                    input_nodes[(i, j)].edges.append(input_nodes[(i, j-1)])
                if input_nodes[(i, j)].elevation <= input_nodes[(i, j-1)].elevation + 1:
                    input_nodes[(i, j-1)].edges.append(input_nodes[(i, j)])
    return input_nodes

def get_steps(start_node):
    q = []
    q.append(start_node)
    while len(q) > 0:
        node = q.pop(0)
        if node.is_end:
            return node.steps
        for child_node in node.edges:
            if child_node.steps is None:
                child_node.steps = node.steps + 1
                q.append(child_node)

nodes = get_nodes(input)
start_node = [n for n in nodes.values() if n.is_start][0]
start_node.steps = 0
steps = get_steps(start_node)
print(steps)

# part 2
nodes = get_nodes(input)
possible_start_nodes = [n for n in nodes.values() if n.elevation == 97]
pseudo_node = Node('a')
pseudo_node.steps = -1
pseudo_node.edges = possible_start_nodes
steps = get_steps(pseudo_node)
print(steps)
