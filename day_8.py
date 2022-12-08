from get_input import get_input

day_num = 8
raw_input = get_input(day_num)

test_input = """
30373
25512
65332
33549
35390
""".strip()

input = raw_input

# part 1

class Tree:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.other_trees = []

    def add_tree(self, tree):
        self.other_trees.append(tree)

    def to_the_left(self, tree):
        return self.x - tree.x

    def to_the_right(self, tree):
        return tree.x - self.x

    def above(self, tree):
        return self.y - tree.y

    def below(self, tree):
        return tree.y - self.y

    def visible_direction(self, fnc):
        return all([t.height < self.height for t in self.other_trees if fnc(t) > 0])

    def visible(self):
        return self.visible_direction(self.to_the_left) or \
               self.visible_direction(self.to_the_right) or \
               self.visible_direction(self.above) or \
               self.visible_direction(self.below)


trees = {}
for y, line in enumerate(input.split('\n')):
    for x, height in enumerate(line):
        tree = Tree(x, y, height)
        for i in range(x-1, -1, -1):
            tree_to_left = trees[(i, y)]
            tree.add_tree(tree_to_left)
            tree_to_left.add_tree(tree)
        for j in range(y-1, -1, -1):
            tree_below = trees[(x, j)]
            tree.add_tree(tree_below)
            tree_below.add_tree(tree)
        trees[(x, y)] = tree

print(sum([tree.visible() for tree in trees.values()]))

# part 2
