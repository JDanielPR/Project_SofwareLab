import logging

logger = logging.getLogger('component')
logging.basicConfig(level=logging.DEBUG)

## debugging purpose
try:
  import pygame
except:
  pass
# Define some colors as global constants
BLACK       = (  0,   0,   0)
WHITE       = (255, 255, 255)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
BLUE        = (  0,   0, 255)
LIGHT_BLUE  = (102, 255, 255)
DARK_GREEN  = (  0, 100,   0)

class Component():
  """Defines the components in the topological model"""
 
  def __init__(self,
               leftNode, rightNode,
               rigidLength,
               componentsName,
               isGap = False):
    """Constructs the class structure_core.Component.Component.

    Args:
      leftNode:
        the node object that defines the left node of the component
      rightNode:
        the node object that defines the right node of the component
      rigidLength:
        scalar value of the rigid length of the component
      componentsName:
        string that represents the name of the component
    Returns:
      an object of the class.
    Raises:
      nothing is raised.
    """
    assert leftNode.position < rightNode.position    

    self.name = componentsName
    self.leftNode = leftNode
    self.rightNode = rightNode
    self.rigidLength = rigidLength
    self.isGap = isGap
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
    if self.isGap:
      color = LIGHT_BLUE
    else:
      color = BLUE
    level = (self.leftNode.loadpathLevel + 1) * y_scaling
    # draw deformable part
    x1 = self.leftNode.position + offset
    y1 = level
    x2 = x1 + self.length() - self.rigidLength
    y2 = level
    pygame.draw.line(screen, color, [x1, y1], [x2, y2], 7)
    if self.connectedToBarrier:
      pygame.draw.line(screen, DARK_GREEN, [x1, y1+3], [x2, y2+3], 2)
    if self.connectedToFirewall:
      pygame.draw.line(screen, RED, [x1, y1-3], [x2, y2-3], 2)
    # draw left node
    self.leftNode.draw(screen, offset, y_scaling)
    # draw rigid part
    x1 = x2
    x2 = x2 + self.rigidLength
    pygame.draw.line(screen, BLACK, [x1, y1], [x2, y2], 5)
    if self.connectedToBarrier:
      pygame.draw.line(screen, DARK_GREEN, [x1, y1+3], [x2, y2+3], 2)
    if self.connectedToFirewall:
      pygame.draw.line(screen, RED, [x1, y1-3], [x2, y2-3], 2)
    # draw right node
    self.rightNode.draw(screen, offset, y_scaling)

  def length(self):

    return self.rightNode.position - self.leftNode.position

  def deformable_length(self):
    """Calculates the current deformale length of the component.

    Args:
      nothing is taken.
    Returns:
      scalar value of the current deformable length of the component.
    Raises:
      nothins is raised.
    """
    if (self.connectedToBarrier \
        and self.connectedToFirewall) \
        or self.isGap:
      return self.length() - self.rigidLength
    else:
      return 0
      
  def moves(self, list_of_nodes):
    """Determines the nodes that are going to be moved as a result to the
        defomation step.

    Args:
      list_of_nodes:
        list that contains the nodes that are deforming their components
    Returns:
      list of the nodes that are going to be moved by the deformation step.
    Raises:
      nothing is raised.
    """
    return any(node.loadpathLevel == self.leftNode.loadpathLevel
               and
               node.position <= self.leftNode.position
               for node in list_of_nodes)

  def link_to_barrier(self):
    """Determine whether the component is connected to the barrier (no gap is
        standing in its way).

    Args:
      nothing is taken.
    Returns:
      nothing is returned.
    Raises:
      nothing is raised.
    """
    if self.connectedToBarrier:
      return
    self.connectedToBarrier = True
    if self.isGap and self.deformable_length() > 0:
      return
    else:
      for component in self.rightNode.towardsFirewall:
        component.link_to_barrier()

  def link_to_firewall(self):
    """Determine whether the component is connected to the firewall (no gap is
        standing in its way).

    Args:
      nothing is taken.
    Returns:
      nothing is returned.
    Raises:
      nothing is raised.
    """
    if self.connectedToFirewall:
      return
    self.connectedToFirewall = True
    if self.isGap and self.deformable_length() > 0:
      return
    else:
      for component in self.leftNode.towardsBarrier:
        component.link_to_firewall()
    
  def next_gap(self):
    """Determines whether there is another gap along the loadpath to be deformed.

    Args:
      nothing is taken.
    Returns:
      if there is no other gap left, it returns None, otherwise the gap object.
    Raises:
      nothing is raised.
    """
    # initialize the neighbour
    neighbour = None
    # iterate over the right neighbours until a gap is found
    while not neighbour \
          or not neighbour.isGap:
      # try to get the right neighbour
      try:
        neighbour, = [comp
                      for comp in neighbour.rightNode.towardsFirewall
                      if comp.rightNode.
                      loadpathLevel == self.rightNode.loadpathLevel]
      # at first neighbour is None and components should be searched in
      # self.rightNode.towardsFirewall
      except AttributeError:
        try:
          neighbour, = [comp
                        for comp in self.rightNode.towardsFirewall
                        if comp.rightNode.
                        loadpathLevel == self.rightNode.loadpathLevel]
        except ValueError:
          return None # if no neighbour could be found
      except ValueError:
        return None # if no neighbour could be found
    # neighbour is a gap, return it
    return neighbour
      
      
##  def unlink_from_barrier(self):
##    if not self.connectedToBarrier:
##      return
##
##    self.connectedToBarrier = False
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
      
