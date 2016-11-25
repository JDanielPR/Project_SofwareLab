import logging
logger = logging.getLogger('CrossComponentLogger')

## debugging purpose
try:
  import pygame
except:
  pass
# Define some colors as global constants
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
DARK_GREEN  = (  0, 100,   0)

class CrossComponent():
  """Defiens the cross-components in the topological model"""

  def __init__(self,
               name,
               leftNode, rightNode,
               rigidLength):
    """Constructs the clas structure_core.CrossComponent.crossComponent.

    Args:
      name:
        string of the name of the cross_component
      leftNode:
        node object of the left node of the cross_component
      rightNode:
        node object of the right node of the cross_component
      rigidLength:
        scalar value of the rigid length of the cross_component
    Returns:
      an object of the class.
    Raises:
      nothing is raised.
    """
    # the first node is chosen as the one closer to the barrier
    assert leftNode.position < rightNode.position
    self.name = name
    self.leftNode = leftNode 
    self.rightNode = rightNode
    self.rigidLength = rigidLength
    
    self.breakable = False
    self.broken = False

    self.connectedToBarrier = None
    self.connectedToFirewall = None

    self.leftNode.towardsFirewall.append(self)
    self.rightNode.towardsBarrier.append(self)

  def __repr__(self):
    return self.name

  def draw(self, screen, offset, y_scaling):
    """Draws onto the screan the current statw of the structure (DEBUG purpose).

    Args:
      screan:
        defines the screan to output the debugging data and its properties
      offset:
        ...
      y_scaling:
        ...
    Returns:
      nothing is returned
    Raises:
      nothing is raised
    """
    level1 = (self.leftNode.loadpathLevel + 1) * y_scaling
    level2 = (self.rightNode.loadpathLevel + 1) * y_scaling
    x1 = int(self.leftNode.position + offset)
    y1 = int(level1)
    x2 = int(self.rightNode.position + offset)
    y2 = int(level2)
    # if rigid
    if self.length() == 0:
      # draw rigid part
      pygame.draw.line(screen, BLACK, [x1, y1], [x2, y2], 7)
      if self.connectedToBarrier:
        pygame.draw.line(screen, DARK_GREEN, [x1, y1+3], [x2, y2+3], 2)
      if self.connectedToFirewall:
        pygame.draw.line(screen, RED, [x1, y1-3], [x2, y2-3], 2)
    # if deformable
    else:
      xm = int(x1 + (1 - self.rigidLength/self.length()) * (x2 - x1))
      ym = int(y1 + (1 - self.rigidLength/self.length()) * (y2 - y1))
      # draw deformable and rigid part
      pygame.draw.line(screen, BLUE, [x1, y1], [xm, ym], 7)
      pygame.draw.line(screen, BLACK, [xm, ym], [x2, y2], 7)
      if self.connectedToBarrier:
        pygame.draw.line(screen, DARK_GREEN, [x1, y1+3], [x2, y2+3], 2)
      if self.connectedToFirewall:
        pygame.draw.line(screen, RED, [x1, y1-3], [x2, y2-3], 2)
    # draw nodes
    self.leftNode.draw(screen, offset, y_scaling)
    self.rightNode.draw(screen, offset, y_scaling)


  def left_deforms(self, list_of_nodes):
    """Determines whether the deformation step will move the left node of the
        cross_component.

    Args:
      list_of_nodes:
        list that contains the nodes that are deforming their components
    Returns:
      True if the defomation step will lead to motion to the left node, False otherwise.
    Raises:
      nothing is raised.
    """
    return any(node.loadpathLevel == self.leftNode.loadpathLevel 
               and 
               node.position <= self.leftNode.position 
               for node in list_of_nodes)

  def right_deforms(self, list_of_nodes):
    """Determines whether the deformation step will move the right node of the
        cross_component.

    Args:
      list_of_nodes:
        list that contains the nodes that are deforming their components
    Returns:
      True if the defomation step will lead to motion to the right node, False otherwise.
    Raises:
      nothing is raised.
    """
    return any(node.loadpathLevel == self.rightNode.loadpathLevel 
               and 
               node.position <= self.rightNode.position 
               for node in list_of_nodes)
  
  def length(self):
    """Calculates the current length of the cross_component.

    Args:
      nothing is taken.
    Returns:
      scalar value of the current length of the cross_component.
    Raises:
      nothing is raised.
    """
    return self.rightNode.position - self.leftNode.position
  
  def deformable_length(self):
    """Calculates the current deformale length of the cross_component.

    Args:
      nothing is taken.
    Returns:
      scalar value of the current deformable length of the cross_component.
    Raises:
      nothins is raised.
    """
    if self.connectedToBarrier \
       and self.connectedToFirewall:
      return self.length() - self.rigidLength
    else:
      return 0

  def is_valid(self):
    """Determines whether the cross_component is broken.

    Args:
      nothing is taken.
    Returns:
      True if the cross_component is not broken, False otherwise.
    Raises:
      nothing is raised.
    """
    return not self.broken

  def link_to_barrier(self):
    """Determine whether the cross_component is connected to the barrier 
        (no gap is standing in its way).

    Args:
      nothing is taken.
    Returns:
      nothing is returned.
    Raises:
      nothing is raised.
    """
    if self.connectedToBarrier or self.broken:
      return
    self.connectedToBarrier = True
    for component in self.rightNode.towardsFirewall:
      component.link_to_barrier()

  def link_to_firewall(self):# broken ###################
    """Determine whether the cross_component is connected to the firewall
        (no gap is standing in its way).

    Args:
      nothing is taken.
    Returns:
      nothing is returned.
    Raises:
      nothing is raised.
    """
    if self.connectedToFirewall or self.broken:
      return
    self.connectedToFirewall = True
    for component in self.leftNode.towardsBarrier:
      component.link_to_firewall()

##  def unlink_from_barrier(self):
##    # if it isn't connected to the barrier don't do anything
##    if not self.connectedToBarrier:
##      return
##    # else diconnect from barrier
##    self.connectedToBarrier = False
##    # if self was the only responsible for the propagation of the connection,
##    # disconnect also the right neighbours towards the firewall
##    if any(component.connectedToBarrier and
##           not component.isGap
##           for component in self.rightNode.towardsBarrier) \
##           or self.rightNode.onBarrier:
##      return
##    else:
##      for component in self.rightNode.towardsFirewall:
##        component.unlink_from_barrier()
##
##  def unlink_from_firewall(self):
##    if not self.connectedToFirewall:
##      return
##
##    self.connectedToBarrier = False
##    if any(component.connectedToFirewall and
##           not component.isGap
##           for component in self.leftNode.towardsFirewall) \
##           or self.leftNode.onFirewall:
##      return
##    else:
##      for component in self.leftNode.towardsBarrier:
##        component.unlink_from_firewall()

        
