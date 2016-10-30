import logging
logger = logging.getLogger('CrossComponentLogger')

class CrossComponent():
  '''
  This class stores the information related to a cross component
  and a method that checks whether a deformation step is valid
  with respect to this cross component
  '''

  def __init__(self,
               name,
               leftNode, rightNode,
               rigidLength):
    # the first node is chosen as the one closer to the barrier
    assert leftNode.position < rightNode.position
    self.name = name
    self.leftNode = leftNode 
    self.rightNode = rightNode
    self.rigidLength = rigidLength
    
    self.breakable = False
    self.broken = False

    self.leftNode.connectivity.append(self)
    self.rightNode.connectivity.append(self)

  def left_deforms(self, list_of_nodes):
    """True if the given deformation leading nodes would move the leftNode."""
    return any(node.loadpathLevel == self.leftNode.loadpathLevel 
               and 
               node.position <= self.leftNode.position 
               for node in list_of_nodes)

  def right_deforms(self, list_of_nodes):
    """True if the given deformation leading nodes would move the rightNode."""
    return any(node.loadpathLevel == self.rightNode.loadpathLevel 
               and 
               node.position <= self.rightNode.position 
               for node in list_of_nodes)
  
  def length(self):
    """Returns the length in x direction of the crossComponent."""
    return self.rightNode.position - self.leftNode.position
  
  def deformable_length(self):
    """Returns the deformable length in x direction of the crossComponent."""
    return self.length() - self.rigidLength

  def is_valid(self):
    return not self.broken
    
