
class NodeTree:
    def __init__(self, data, parent = None):
        assert type(data) is str
        self.data = data
        self.parent = parent
        self.children = [ ]
        self.nextChild = 

    def add_child(self, x):
        data = self.data + x
        child = NodeTree(data, self)
        self.children.append(child)

    def __repr__(self):
        return self.data
        
class Tree:
    def __init__(self, possibilities):
        self.possiblities = possibilities
        self.root = NodeTree('ROOT')
        self.activeNode = self.root

    def __repr__(self):
        return self.activeNode.repr()

    def add_children(self):
        for x in possibilities:
            self.activeNode.add_child(x)

    def go_down(self):
        previous = self.activeNode
        self.activeNode = self.activeNode.children[0]
        actual = self.activeNode
        print('{} -> {}'.format(previous, actual))
        
    def go_up(self):
        previous = self.activeNode
        self.activeNode = self.activeNode.parent
        actual = self.activeNode
        print('{} -> {}'.format(previous, actual))

    def go_right(self):
        previous = self.activeNode
        self.activeNode = self.activeNode.parent
        actual = self.activeNode
        print('{} -> {}'.format(previous, actual))
        
possibilities = ['a', 'b', 'c', 'd']

pt = Tree(possibilities)
