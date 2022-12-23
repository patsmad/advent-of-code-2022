from get_input import get_input

day_num = 22
raw_input = get_input(day_num, strip=False)
raw_cube_edges = [(0, 8), (1, 4), (2, 12), (3, 13), (5, 9), (6, 10), (7, 11)]

test_input = \
"""        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""
test_cube_edges = [(0, 4), (2, 8), (6, 11), (9, 13), (3, 12), (1, 5), (7, 10)]

input = raw_input
cube_edges = raw_cube_edges

class Node:
    def __init__(self, x, y, is_wall):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.neighbors = {}

movements = {
    0: (1, 0),
    1: (0, 1),
    2: (-1, 0),
    3: (0, -1)
}

class Person:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0

    def move(self, nodes):
        current_node = nodes[self.x, self.y]
        neighbor, new_direction = current_node.neighbors[self.direction]
        if not  neighbor.is_wall:
            self.x = neighbor.x
            self.y = neighbor.y
            self.direction = new_direction

class Map:
    def __init__(self, map_input, cube_edges=None):
        self.nodes = {}
        for i, line in enumerate(map_input.split('\n')):
            for j, point in enumerate(line):
                if point != ' ':
                    self.nodes[j + 1, i + 1] = Node(j + 1, i + 1, point == '#')
        self.min_x = min([a[0] for a in self.nodes])
        self.min_y = min([a[1] for a in self.nodes])
        self.max_x = max([a[0] for a in self.nodes])
        self.max_y = max([a[1] for a in self.nodes])
        if (self.max_x - self.min_x + 1) % 3 == 0:
            self.block_edge = (self.max_x - self.min_x + 1) // 3
        else:
            self.block_edge = (self.max_y - self.min_y + 1) // 3
        self.set_direct_neighbors()
        edges = self.get_edges()
        self.set_indirect_neighbors(edges, cube_edges)

    def set_direct_neighbors(self):
        for direction in [0, 1, 2, 3]:
            dx, dy = movements[direction]
            for node in self.nodes.values():
                key = (node.x + dx, node.y + dy)
                if key in self.nodes:
                    node.neighbors[direction] = (self.nodes[key], direction)

    def get_edges(self):
        edges = []
        for i in range(self.min_x, self.max_x + 1, self.block_edge):
            top = min([a[1] for a in self.nodes if a[0] == i])
            bottom = max([a[1] for a in self.nodes if a[0] == i])
            edges.append([(j, top, 3) for j in range(i, i + self.block_edge)])
            edges.append([(j, bottom, 1) for j in range(i, i + self.block_edge)])
        for i in range(self.min_y, self.max_y + 1, self.block_edge):
            left = min([a[0] for a in self.nodes if a[1] == i])
            right = max([a[0] for a in self.nodes if a[1] == i])
            edges.append([(left, j, 2) for j in range(i, i + self.block_edge)])
            edges.append([(right, j, 0) for j in range(i, i + self.block_edge)])
        return edges

    def connect_edges(self, edge_1, edge_2):
        for e1, e2 in zip(edge_1, edge_2):
            self.nodes[e1[0], e1[1]].neighbors[e1[2]] = (self.nodes[e2[0], e2[1]], (e2[2] + 2) % 4)
            self.nodes[e2[0], e2[1]].neighbors[e2[2]] = (self.nodes[e1[0], e1[1]], (e1[2] + 2) % 4)

    def set_indirect_neighbors(self, edges, cube_edges):
        if cube_edges is None:
            for i in range(0, len(edges), 2):
                self.connect_edges(edges[i], edges[i + 1])
        else:
            for idx_1, idx_2 in cube_edges:
                edge_1 = edges[idx_1]
                edge_2 = edges[idx_2]
                if ((edge_1[0][2] - 1) % 4 < 2) == ((edge_2[0][2] - 1) % 4 < 2):
                    self.connect_edges(edge_1, edge_2[::-1])
                else:
                    self.connect_edges(edge_1, edge_2)

    def to_string(self, person):
        lines = []
        for i in range(self.min_y, self.max_y + 1):
            line = ''
            for j in range(self.min_x, self.max_x + 1):
                if person.x == j and person.y == i:
                    line += 'p'
                elif (j, i) in self.nodes:
                    line += '#' if self.nodes[(j, i)].is_wall else '.'
                else:
                    line += ' '
            lines.append(line)
        return '\n'.join(lines)

map_input, movement_input = input.split('\n\n')
movement_list = []
current_movement = ''
for i in movement_input:
    if i == 'R':
        movement_list.append((int(current_movement), 'R'))
        current_movement = ''
    elif i == 'L':
        movement_list.append((int(current_movement), 'L'))
        current_movement = ''
    else:
        current_movement += i
movement_list.append((int(current_movement), 'L'))
movement_list.append((0, 'R'))

# part 1

m = Map(map_input)
person_y = min([a[1] for a in m.nodes])
person_x = min([a[0] for a in m.nodes if a[1] == person_y])
p = Person(person_x, person_y)

for movement in movement_list:
    for _ in range(movement[0]):
        p.move(m.nodes)
    if movement[1] == 'R':
        p.direction = (p.direction + 1) % 4
    if movement[1] == 'L':
        p.direction = (p.direction - 1) % 4
print(1000 * p.y + 4 * p.x + p.direction)

# part 2

m = Map(map_input, cube_edges=cube_edges)
person_y = min([a[1] for a in m.nodes])
person_x = min([a[0] for a in m.nodes if a[1] == person_y])
p = Person(person_x, person_y)

for movement in movement_list:
    for _ in range(movement[0]):
        p.move(m.nodes)
    if movement[1] == 'R':
        p.direction = (p.direction + 1) % 4
    if movement[1] == 'L':
        p.direction = (p.direction - 1) % 4
print(1000 * p.y + 4 * p.x + p.direction)
