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
        self.left_trees = []
        self.right_trees = []
        self.up_trees = []
        self.down_trees = []

    def add_left_tree(self, tree):
        self.left_trees.append(tree)

    def add_right_tree(self, tree):
        self.right_trees.append(tree)

    def add_up_tree(self, tree):
        self.up_trees.append(tree)

    def add_down_tree(self, tree):
        self.down_trees.append(tree)

    def count_visible(self, tree_vec):
        count = 0
        for tree in tree_vec:
            if tree.height < self.height:
                count += 1
            else:
                return count
        return count

    def visible_direction(self, tree_vec):
        return len(tree_vec) == self.count_visible(tree_vec)

    def visible(self):
        return self.visible_direction(self.right_trees) or \
               self.visible_direction(self.left_trees) or \
               self.visible_direction(self.up_trees) or \
               self.visible_direction(self.down_trees)

    def scenic_score(self):
        prod = 1
        for tree_vec in [self.right_trees, self.left_trees, self.up_trees, self.down_trees]:
            c = self.count_visible(tree_vec)
            prod *= c + 1 * (c != len(tree_vec))
        return prod

trees = {}
for y, line in enumerate(input.split('\n')):
    for x, height in enumerate(line):
        tree = Tree(x, y, height)
        for i in range(x-1, -1, -1):
            tree_to_left = trees[(i, y)]
            tree.add_left_tree(tree_to_left)
            tree_to_left.add_right_tree(tree)
        for j in range(y-1, -1, -1):
            tree_above = trees[(x, j)]
            tree.add_up_tree(tree_above)
            tree_above.add_down_tree(tree)
        trees[(x, y)] = tree

print(sum([tree.visible() for tree in trees.values()]))

# part 2
print(trees[sorted(trees, key=lambda pos: trees[pos].scenic_score(), reverse=True)[0]].scenic_score())