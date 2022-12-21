from get_input import get_input

day_num = 20
raw_input = get_input(day_num)

test_input = """
1
2
-3
3
-2
0
4
""".strip()

input = raw_input

class Node:
    def __init__(self, num):
        self.num = num
        self.left = None
        self.right = None

def get_nodes(key, input):
    nodes = [Node(int(num) * key) for num in input.split('\n')]
    for i in range(len(nodes)):
        nodes[i].left = nodes[i - 1]
        nodes[i].right = nodes[(i + 1) % len(nodes)]
    return nodes

def swap(node):
    right_node = node.right
    left_node = node.left
    node.right = right_node.right
    node.left = right_node
    right_node.left = left_node
    left_node.right = right_node
    right_node.right.left = node
    right_node.right = node

def get_final_order(nodes):
    final_order = []
    zero_node = [n for n in nodes if n.num == 0][0]
    for _ in range(len(nodes)):
        final_order.append(zero_node)
        zero_node = zero_node.right
    return final_order

def run(nodes, mixes):
    for i in range(mixes):
        node_to_move = nodes[i % len(nodes)]
        cycled_number = nodes[i % len(nodes)].num % (len(nodes) - 1)
        for _ in range(cycled_number):
            swap(node_to_move)

    return get_final_order(nodes)

# part 1
nodes = get_nodes(1, input)
final_order = run(nodes, len(nodes))

s = 0
for i in [1000, 2000, 3000]:
    s += final_order[i % len(final_order)].num
print(s)

# part 2

nodes = get_nodes(811589153, input)
nodes = run(nodes, len(nodes) * 10)
final_order = get_final_order(nodes)

s = 0
for i in [1000, 2000, 3000]:
    s += nodes[i % len(nodes)].num
print(s)
