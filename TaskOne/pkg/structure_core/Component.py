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
               isGap = False):
    
    assert leftNode.position < rightNode.position    

    self.name = componentsName
    self.leftNode = leftNode
    self.rightNode = rightNode
    self.rigidLength = rigidLength
    self.isGap = isGap
    
    self.leftNode.towardsFirewall.append(self)
    self.rightNode.towardsBarrier.append(self)

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

  def is_valid(self):
    return not self.isGap
