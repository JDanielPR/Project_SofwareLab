import itertools
from ..tree_core.tree import Tree
from .. import GapsHandeling

class Structure():
  '''Structure class groups all of the nodes, components, crossComponents, and
gaps all together in a single entity'''
  def __init__(self, listLoadpaths, listCrossComponents = None):
    self.listLoadpaths = listLoadpaths
    self.listCrossComponents = listCrossComponents
    
    self.listGaps = [ ]
    self.invalidComponents = [ ]
    
##  def create_blocks():
##    # create blocks
##    list of blocks 
##    for node in nodes:
##      for block in list of blocks:
##        if node not in block:
##          list of blocks . append(Block(node))
##    # qualify blocks
##    for block in list of blocks:
##      block.end_to_end()
##
##    def stuff
##
##    #
##    for gap in self.listGaps:
##      leftBlock, = [block for block in list of block
##                   if gap.leftNode in block]
##      rightBlock, = [...gap.rightNode
##
##      if leftBlock.end_to_end or rightBlock.end_to_end:
##                     # no priority
##      else:
##                     # priority
##                     
##
##    [[lp1],
##     [lp2],
##     [lp3]
##     ]
##      
    

    
          
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

  def priority_determiner(self):
    """Initialize self.invalidComponents"""
    for gap in self.listGaps:
      validComponents = [comp for comp in gap.leftNode.connectivity
                         if comp.is_valid()]
      if len(validComponents) == 1:
        self.invalidComponents.append(validComponents[0])
        
      validComponents = [comp for comp in gap.rigthNode.connectivity
                         if comp.is_valid()]
      if len(validComponents) == 1:
        self.invalidComponents.append(validComponents[0])
      

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
  def task_one(self):

    tree = self.possibilities_tree_generator()

    tree.add_children()
    while tree.activeNode is not tree.root or not tree.end():
        while not tree.end():
            tree.go_down()
            tree.deform()
            tree.add_children()
            
        while tree.end():
            tree.go_up()
            if tree.activeNode is tree.root:
                break
    return tree.savers[0].i_s, tree.savers[0].d_h

  def task_two(self, blackbox):
    """solves"""

    # generate tree
    tree = self.possibilities_tree_generator()
    
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
'''    
  def possibilities_tree_generator(self):
    # Add all of the loadpaths to a list called "structure array" for the sake
    # of the possibilities tree generation using the embedded module itertools
    structureArray = []
    for loadpath in self.listLoadpaths:
      structureArray.append(loadpath.listComponents)

    # Generate the possibilities tree
    possibilities = list(itertools.product(*structureArray))
    tree = Tree(possibilities, self)

##    # Add children to the root and set the first child as activeNode
##    tree.deform() # nothing happens when performing the root step
##    tree.add_children()
##    tree.go_down()
    
    return tree
'''

  def get_deforming_components( self ):
    for gap in self.listGaps:
      if any( component.connectedToBarrier for component in gap.leftNode.towardsBarrier ):
        for component in gap.rightNode.towardsFirewall:
          component.link_to_barrier()

      if any( component.connectedToFirewall for component in gap.rightNode.towardsFirewall ):
        for component in gap.leftNode.towardsBarrier:
          component.link_to_firewall()

    for crossComponent in self.listCrossComponents:
      if crossComponent.broken:
        
      if any( component.connectedToBarrier for component in crossComponent.leftNode.towardsBarrier ):
        
    structureArray = [ ]
    for loadpath in self.listLoadpaths:
      structureArray.append( loadpath.valid_components() )

    return( list(itertools.product(*structureArray)) )
      
      
