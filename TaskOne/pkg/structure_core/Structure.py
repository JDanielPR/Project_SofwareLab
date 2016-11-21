import itertools
from ..tree_core.tree import Tree
from .. import GapsHandeling

## debugging purpose
DEBUG = True
STEPWISE = False
if DEBUG:
  import pygame
  pygame.init()
  size = [1500, 500]
  screen = pygame.display.set_mode(size)
  # Define some colors as global constants
  BLACK = (  0,   0,   0)
  WHITE = (255, 255, 255)
  RED   = (255,   0,   0)
  GREEN = (  0, 255,   0)
  BLUE  = (  0,   0, 255)


class Structure():
  '''Structure class groups all of the nodes, components, crossComponents, and
gaps all together in a single entity'''
  
  def __init__(self, listLoadpaths, listCrossComponents = None):
    self.listLoadpaths = listLoadpaths
    self.listCrossComponents = listCrossComponents
    
    self.listGaps = [comp for lp in self.listLoadpaths
                     for comp in lp.listComponents
                     if comp.isGap]

  def draw(self):
    if not DEBUG:
      return
    screen.fill(WHITE)
    offset = 800
    y_scaling = 20
    for lp in self.listLoadpaths:
      for comp in lp.listComponents:
        comp.draw(screen, offset, y_scaling)
        
    for crossComp in self.listCrossComponents:
      crossComp.draw(screen, offset, y_scaling)
    # update the screen
    pygame.display.flip()
    if STEPWISE:
      any_key = input("press any key to go on")
    
  def task_one(self):
    """solves"""
    # generate tree
    tree = Tree(self)

    tree.add_children()
    self.draw() ###
    while tree.activeNode is not tree.root or not tree.end():
        while not tree.end():
            tree.go_down()
            tree.deform()
            self.draw() ###
            tree.add_children()
            self.draw() ###
            
        while tree.end():
            tree.go_up()
            self.draw() ###
            if tree.activeNode is tree.root:
                break
    if DEBUG:
      pygame.quit()
    return tree.savers[0].i_s, tree.savers[0].d_h

  def task_two(self, blackbox):
    """solves"""
    # generate tree
    tree = Tree(self)
    
    tree.add_children()
    if not tree.end():
      tree.go_down()
    else:
      return False, False

    # surf the tree
    while True:
      if not tree.surf(blackbox):
        return False, False # no more right neighbours
      if tree.end():
        break
    # completely deformed structure
    return tree.savers[0].i_s, [tree.savers[0].ood]

  def reset_connections_to_barrier_and_firewall(self):
    # undo all connections
    for loadpath in self.listLoadpaths:
      for component in loadpath.listComponents:
        component.connectedToBarrier = False
        component.connectedToFirewall = False
        component.leftNode.onBarrier = False
        component.leftNode.onFirewall = False
        component.rightNode.onBarrier = False
        component.rightNode.onFirewall = False
    for crossComp in self.listCrossComponents:
      crossComp.connectedToBarrier = False
      crossComp.connectedToFirewall = False
      crossComp.leftNode.onBarrier = False
      crossComp.leftNode.onFirewall = False
      crossComp.rightNode.onBarrier = False
      crossComp.rightNode.onFirewall = False
    # redo all connections
    for loadpath in self.listLoadpaths:
      leftLimit = min(comp.leftNode.position
                      for comp in loadpath.listComponents)
      rightLimit = max(comp.rightNode.position
                       for comp in loadpath.listComponents)
      frontNodes = [comp.leftNode
                    for comp in loadpath.listComponents
                    if comp.leftNode.position == leftLimit]
      backNodes = [comp.rightNode
                   for comp in loadpath.listComponents
                   if comp.rightNode.position == rightLimit]
      for frontNode in frontNodes:
        frontNode.onBarrier = True
        for comp in frontNode.towardsFirewall:
          comp.link_to_barrier()
      for backNode in backNodes:
        backNode.onFirewall = True
        for comp in backNode.towardsBarrier:
          comp.link_to_firewall()
    self.draw()

  def get_deforming_components(self):
##    ###########################################################################
##    ## 1. update the connectedToTheBarrier and connectedToTheFirewall
##    ##    attributes
##    # loop over closed gaps
##    for gap in self.listGaps:
##      if gap.deformable_length() == 0:
##        # propagate the connection to the barrier
##        if any(component.connectedToBarrier
##               for component in gap.leftNode.towardsBarrier) \
##               or gap.leftNode.onBarrier:
##          for component in gap.rightNode.towardsFirewall:
##            component.link_to_barrier()
##        # propagate the connection to the firewall
##        if any(component.connectedToFirewall
##               for component in gap.rightNode.towardsFirewall) \
##               or gap.rightNode.onFirewall:
##          for component in gap.leftNode.towardsBarrier:
##            component.link_to_firewall()
##    # loop over broken connections
##    for crossComponent in self.listCrossComponents:
##      if crossComponent.broken:
##        # propagate the disconnections
##        crossComponent.unlink_from_barrier()
##        crossComponent.unlink_from_firewall()
##    ###########################################################################
##    ## 2. create a list of tuples, one for each group of components to deform
    structureArray = [ ]
    for loadpath in self.listLoadpaths:
      structureArray.append(loadpath.valid_components())


    return list(itertools.product(*structureArray))
      
      
