#### Fix me
##import Node
##import Component
##
##class Block:
##    def __init__(self, node):
##        self.listNodes = set(node)
##        self.listComponents = set()
##        for node in self.listNodes:
##            for comp in node.connectivities:
##                if comp.isGap:
##                    pass
##                else:
##                    self.listNodes.add(comp.leftNode)
##                    self.listNodes.add(comp.rightNode)
##                    self.listComponents.add(comp)
##                    
##        self.end_to_end = None 
##
##    def __contains__(self, nodeOrComp):
##        if type(nodeOrComp) is Node:
##            return nodeOrComp in self.listNodes
##        if type(nodeOrComp) is Component:
##            return nodeOrComp in self.listComponents
##
##    def end_to_end(self):
##        """Set self.end_to_end to True of False."""
##        
##
