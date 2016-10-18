
class NodeTree:
    def __init__(self, data, parent = None):
        self.data = data # (comp1, comp5)
        self.parent = parent
        self.children = [ ]
        self.isValid = True
        self.amount = None

    def __repr__(self):
        return self.data
    
    def add_child(self, data):
        child = NodeTree(data, self)
        child.check() # stupid but simpler!
        self.children.append(child)

    def check(self):
        self.determine_amount()
        if self.amount == 0:
            self.isValid = False
            
    def determine_amount():
        """Computes the correct value for self.amount"""
        
        raise Exception # not implemented
    
class Tree:
    def __init__(self, possibilities):
        self.possiblities = possibilities
        self.root = NodeTree('ROOT')
        self.activeNode = self.root
        self.end = False

    def __repr__(self):
        return self.activeNode

    def add_children(self):
        for data in possibilities:
            self.activeNode.add_child(data)

    def go_down(self):
        """Changes the activeNode to its first valid child.

If there isn't any active child, the activeNode is the rightest child and the
tree attribute .end is set to True.
This function should not raise any exception"""
        self.deform()
        
        self.activeNode = self.activeNode.children[0]
        
        if self.activeNode.isValid:
            return
        else:
            try:
                self.go_right()
            except StopIteration:
                self.end = True

    def go_up(self):
        self.end = False # carefully think about that!
        self.undeform()
        self.activeNode = self.activeNode.parent

    def go_right(self):
        """Changes the activeNode to its right neighbour.

If the neighbour doesn't exist, a StopIteration exception is raised.""" 
        
        children = iter(self.activeNode.parent.children)
        for child in children:
            if child == self.activeNode:
                child = next(children)
                break
        self.activeNode = child
        
        if self.activeNode.isValid:
            return
        else:
            self.go_right()

    def deform(self):
        """Deforms the structure according to the active node"""
        # if self.activeNode is the ROOT, just pass
        if self.activeNode is self.root:
            return
        # for each component in data deform
        amount = self.activeNode.amount
        for component in self.activeNode.data:
            component.deform(amount)

    def undeform(self):
        """Undeforms the structure according to the active node"""
        # if self.activeNode is the ROOT, just pass
        if self.activeNode is self.root:
            return
        # for each component in data deform
        amount = self.activeNode.parent.amount
        for component in self.activeNode.parent.data:
            component.deform(-amount) # mind the minus, here we UN-deform

    def surf(self, blackbox):
        """Changes the activeNode.

It goes down or right according to the blackbox response.
"""

        activeNodeIsCorrect = blackbox(self) # what if active node is correct
                                            # but it is not valid?
                                            # could this happen???
                                            # check first within the blackbox
                                            # to avoid this case
                                            # activeNode.isValid = False
                                            # => activeNodeIsCorrect = False

        if activeNodeIsCorrect:
            self.deform()
            self.add_children()
            self.go_down()
          
        else:
            try self.go_right():
                pass
            except StopIteration:
                return False # no more right neighbours
            
        return True
