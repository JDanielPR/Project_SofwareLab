import logging

logger = logging.getLogger('component')
logging.basicConfig(level=logging.DEBUG)

class Component():
  '''
  Component class contains all of the information
  related to both structural and gap components
  and the methods that act upon these attributes
  '''
  def __init__(self,
               leftNode, rightNode,
               rigidLength,
               componentsName,
               rightComponent = None,
               isStructural=True,
               gapIndex = None):
    
    assert leftNode.position < rightNode.position    
    self.name = componentsName
    self.leftNode = leftNode
    self.rightNode = rightNode
    self.rigidLength = rigidLength
    self.isStructural = isStructural  # change in self.isGap
    self.gapIndex = gapIndex  
##    self.history = [ ]
##    self.componentIndex = 0 
##    self.rightComponent = None

  def __repr__(self):
    return self.name

  def length(self):
    return self.rightNode.position - self.leftNode.position

  def deformable_length(self):
    return self.length() - self.rigidLength
      
  def moves(self, list_of_nodes):
    return any(node.loadpathLevel == self.leftNode.loadpathLevel
               and
               node.position <= self.leftNode.position
               for node in list_of_nodes)

  def change_gap_index(self,newGapIndex):

    self.gapIndex = newGapIndex
