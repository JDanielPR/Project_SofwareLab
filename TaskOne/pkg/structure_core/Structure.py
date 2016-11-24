##import itertools
##from ..tree_core.tree import Tree
##from .. import GapsHandeling

## debugging purpose
DEBUG = False
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
  """Groups all the entities of the topological model."""
  
  def __init__(self, listLoadpaths, listCrossComponents = None):
    """Constructor of the class structure_core.structure.Structure.

    Args:
      listLoadpaths:
        a list of structure_core.loadpath.Loadpath objects
      listCrossComponents:
        structure_core.cross_component.CrossComponent
    Returns:
      an object of the class.
    Raises:
      nothing is raised.
    """
    self.listLoadpaths = listLoadpaths
    self.listCrossComponents = listCrossComponents
    
    self.listGaps = [comp for lp in self.listLoadpaths
                     for comp in lp.listComponents
                     if comp.isGap]

  def draw(self):
    """Draws onto the screen the current state of the strucure (DEBUG purpose).

    Args:
      nothing is taken
    Returns:
      nothing is returned
    Raises:
      nothing is raised.    
    """
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
    """Finds all the Order of Deformation of the structure.

    self.task_one() -> [i_s, d_h].
    
    Args:
      nothing is taken
    Returns:
      i_s, a list of isdh.component.Component objects
      d_h, a list of dictionaries such as:
          {  isdh-comp1 : [DeformationStep1,
                           DeformationStep2,
                           ...],
             isdh-comp2 : [DeformationStep1,
                           DeformationStep2,
                           ...],
             isdh-comp3 : [DeformationStep1,
                           DeformationStep2,
                           ...],
          },
          where the keys are the elements of i_s and the values are lists of
          isdh.deformation_step.DeformationStep objects.
    Raises:
      nothing is raised.
    """
    # generate tree
    tree = Tree(self)
    # add children
    tree.add_children()
    self.draw() ###
    # loop until all Order of Deformation have been found, this happens when
    # the activeNode is the root and there are no more valid children
    while tree.activeNode is not tree.root or not tree.end():
      # while there are valid children, keep going down deforming
      while not tree.end():
        tree.go_down()
        tree.deform()
        self.draw() ###
        tree.add_children()
        self.draw() ###
      # while there are not valid children, keep going up undeforming
      while tree.end():
        tree.go_up()
        self.draw() ###
        if tree.activeNode is tree.root:
          break
    
    if DEBUG:
      pygame.quit()
    return tree.savers[0].i_s, tree.savers[0].d_h

  def task_two(self, blackbox):
    """Finds the physical Order of Deformation of the structure.

    self.task_one() -> [i_s, d_h].

    Args:
      blackbox:
        a function that decides whether the activeNode of the tree of the
        structure is the valid next deformationStep or not.
    Returns:
      i_s, a list of isdh.component.Component objects
      d_h, a list with one dictionary such as:
          {  isdh-comp1 : [DeformationStep1,
                           DeformationStep2,
                           ...],
             isdh-comp2 : [DeformationStep1,
                           DeformationStep2,
                           ...],
             isdh-comp3 : [DeformationStep1,
                           DeformationStep2,
                           ...],
          },
          where the keys are the elements of i_s and the values are lists of
          isdh.deformation_step.DeformationStep objects.
    Raises:
      exceptions raised by the blackbox, remain unhandled.
    """
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
    """Updates the connections of components, cross components and nodes.

    The attributes .connectedToBarrier and .connectedToFirewall of every
    structure_core.Component and structure_core.CrossComponent object are
    updated.
    The attributes .onBarrier and .onFirewall of every structure_core.Node
    object are updated.

    Args:
        nothing is taken
    Returns:
        nothing is returned
    Raises:
        nothing is raised
    """
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
      
      
