import itertools
from ..tree_core.tree import Tree
from .. import GapsHandeling

class Structure():
  '''Structure class groups all of the nodes, components, crossComponents, and
gaps all together in a single entity'''
  def __init__(self, listLoadpaths, listCrossComponents = None):
    self.listLoadpaths = listLoadpaths
    self.listCrossComponents = listCrossComponents

  def init_right_components(self):
    for loadpath in self.listLoadpaths:
      for component in loadpath.listComponents:
        # create a list of possible rightComponents
        rightComponents = [rightComponent
                           for rightComponent in loadpath.listComponents
                           if rightComponent.leftNode == component.rightNode]

        if len(rightComponents) is not 0:
          # there should be only one!
          assert len(rightComponents) == 1

          # assign to components its rightComponent
          [component.rightComponent] = rightComponents

  def solve(self):
    '''
    Function polishes and solves the given structure from xml.
    '''

    #this line adds gaps in between the normal members
    GapsHandeling.gapsInsertor(self.listLoadpaths)

    #this line adds indexes to the members (normal and gaps)
    #according to their position with respect to the barrier in
    #their corresponding loadpaths
    otherFunctions.indexor(self.listLoadpaths) 

    #add all of the loadpaths to a list called "structure array"
    #for the sake of the possibilitiesTree generation
    structureArray = []
    for loadpath in self.listLoadpaths:
      structureArray.append(loadpath.listOfMembers)

    #generate the possibilitiesTree
    possibilitiesTree = list(itertools.product(*structureArray)) 

    #initiate the solution sequence of the strcuture starting
    #from the created possiblitiesTree
    initializationStep = nextstep.nextstep(possibilitiesTree,
                                           None, None, self.listCrossMembers,
                                           self.listLoadpaths)

  def task_two(self, blackbox):
    """solves"""

    # generate tree
    tree = self.possibilities_tree_generator() # the first child is
                                               # the activeNode
    # surf the tree
    while not tree.end:
      if not tree.surf(blackbox):
        return False, False # no more right neighbours

    # completely deformed structure
    return tree.savers[0].i_s, [tree.savers[0].ood]
    
  def possibilities_tree_generator(self):
    # Add all of the loadpaths to a list called "structure array" for the sake
    # of the possibilities tree generation using the embedded module itertools
    structureArray = []
    for loadpath in self.listLoadpaths:
      structureArray.append(loadpath.listComponents)

    # Generate the possibilities tree
    possibilities = list(itertools.product(*structureArray))
    tree = Tree(possibilities, self)

    # Add children to the root and set the first child as activeNode
    tree.deform() # nothing happens when performing the root step
    tree.add_children()
    tree.go_down()
    
    return tree
