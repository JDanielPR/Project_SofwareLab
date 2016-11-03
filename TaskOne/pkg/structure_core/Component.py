import logging

logger = logging.getLogger('component')
logging.basicConfig(level=logging.DEBUG)

## debugging purpose
import pygame
# Define some colors as global constants
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

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
               isGap = False):
    
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

  def draw(self, screen):
    
    if self.isGap:
      color = GREEN
    else:
      color = BLUE
    level = self.leftNode.loadpathLevel
    level += 1
    level *= 20
    # draw deformable part
    x1 = self.leftNode.position + 20
    y1 = level
    x2 = x1 + self.deformable_length()
    y2 = level
    pygame.draw.line(screen, color, [x1, y1], [x2, y2], 5)
    # draw left node
    pygame.draw.circle(screen, RED, [int(x1), int(y1)], int(3))
    # draw rigid part
    x1 = x2
    x2 = x2 + self.rigidLength
    pygame.draw.line(screen, BLACK, [x1, y1], [x2, y2], 5)
    # draw right node
    pygame.draw.circle(screen, RED, [int(x2), int(y2)], int(3))

  def length(self):
    return self.rightNode.position - self.leftNode.position

  def deformable_length(self):
    return self.length() - self.rigidLength
      
  def moves(self, list_of_nodes):
    return any(node.loadpathLevel == self.leftNode.loadpathLevel
               and
               node.position <= self.leftNode.position
               for node in list_of_nodes)

  def link_to_barrier(self):
    if self.connectedToBarrier:
      return
    self.connectedToBarrier = True
    if self.isGap:
      return
    else:
      for component in self.rightNode.towardsFirewall:
        component.link_to_barrier()

  def link_to_firewall(self):
    if self.connectedToFirewall:
      return
    self.connectedToFirewall = True
    if self.isGap:
      return
    else:
      for component in self.leftNode.towardsBarrier:
        component.link_to_firewall()

  def unlink_from_barrier(self):
    if not self.connectedToBarrier:
      return

    self.connectedToBarrier = False
    if any(component.connectedToBarrier and
           not component.isGap
           for component in self.rightNode.towardsBarrier) \
           or self.rightNode.onBarrier:
      return
    else:
      for component in self.rightNode.towardsFirewall:
        component.unlink_from_barrier()

  def unlink_from_firewall(self):
    if not self.connectedToFirewall:
      return

    self.connectedToBarrier = False
    if any(component.connectedToFirewall and
           not component.isGap
           for component in self.leftNode.towardsFirewall) \
           or self.leftNode.onFirewall:
      return
    else:
      for component in self.leftNode.towardsBarrier:
        component.unlink_from_firewall()
      
