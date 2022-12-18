from get_input import get_input

day_num = 18
raw_input = get_input(day_num)

test_input = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".strip()

input = raw_input

class Cube:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.neighbors = []

    def add_neighbor(self, cube):
        self.neighbors.append(cube)

class LavaField:
    def __init__(self, cube_input):
        self.cubes = {}
        for line in cube_input.split('\n'):
            x, y, z = map(int, line.split(','))
            self.cubes[(x, y, z)] = Cube(x, y, z)
        self.set_cube_neighbors()
        self.max_dim = max([max(key) for key in self.cubes])

    def set_cube_neighbors(self):
        for cube_key, cube in self.cubes.items():
            for d in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
                neighbor_key = (cube.x + d[0], cube.y + d[1], cube.z + d[2])
                if neighbor_key in self.cubes:
                    cube.neighbors.append(self.cubes[neighbor_key])

    def all_neighbors(self):
        return sum([6 - len(cube.neighbors) for cube in self.cubes.values()])

    def bfs(self):
        queue = []
        water = set()
        exterior_sides = 0
        for i in range(self.max_dim + 1):
            for j in range(self.max_dim + 1):
                water |= {(i, j, -1), (i, j, self.max_dim + 1), (i, -1, j), (i, self.max_dim + 1, j), (-1, i, j), (self.max_dim + 1, i, j)}
                queue += [(i, j, -1), (i, j, self.max_dim + 1), (i, -1, j), (i, self.max_dim + 1, j), (-1, i, j), (self.max_dim + 1, i, j)]
        while len(queue) > 0:
            key = queue.pop(0)
            for d in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
                new_key = (key[0] + d[0], key[1] + d[1], key[2] + d[2])
                if new_key in self.cubes:
                    exterior_sides += 1
                elif new_key not in water and all([d > -1 and d <= self.max_dim for d in new_key]):
                    water |= {new_key}
                    queue.append(new_key)
        return exterior_sides


# part 1
lf = LavaField(input)
print(lf.all_neighbors())

# part 2
print(lf.bfs())