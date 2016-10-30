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
    self.connectedToBarrier = None
    self.conncetodToFirewall = None
    
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

  def link_to_barrier( self ):
    if self.connectedToBarrier:
      return
    self.conncetedToBarrier = True
    if self.isGap:
      return
    else:
      for component in self.rightNode.towardsFirewall:
        component.link_to_barrier()

  def link_to_firewall( self ):
    if self.connectedToFirewall:
      return
    self.connectedToFirewall = True
    if self.isGap:
      return
    else:
      for component in self.leftNode.towardsBarrier:
        component.link_to_firewall()

  def unlink_from_barrier( self ):
    if not self.connectedToBarrier:
      return

    self.connectedToBarrier = False
    if any( component.connectedToBarrier and
              not component.isGap
              for component in self.rightNode.towardsBarrier ):
      return
    else:
      for component in self.rightNode.towardsFirewall:
        component.unlink_from_barrier()

  def unlink_from_firewall( self ):
    if not self.connectedToFirewall:
      return

    self.connectedToBarrier = False
    if any( component.connectedToFirewall and
              not component.isGap
              for component in self.leftNode.towardsFirewall ):
      return
    else:
      for component in self.leftNode.towardsBarrier:
        component.unlink_from_firewall()
      
