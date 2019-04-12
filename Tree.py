class Tree:
    def __init__(self, data):
        self.data = data
        self.child = None

    def insert(self, data):
        self.child = Tree(data)
        return self.child

    def traverse(self, node):
        if node is None:
            return
        else:
            self.traverse(node.child)
            print(node.data)

if __name__ == '__main__':
    root = Tree(1)
    root.insert(2).insert(3).insert(4)
    root.traverse(root)