import nextstep
import itertools
import gapsHandeling
import otherFunctions

class Structure():
'''
Structure class groups all of the nodes, components,
crossComponents, and gaps all together in a single entity
'''
  def __init__(self, listLoadpaths, listCrossComponents = None):
    self.listLoadpaths = listLoadpaths
    self.listCrossComponents = listCrossComponents

  def solve(self):
    '''
    Function polishes and solves the given structure from xml.
    '''

    #this line adds gaps in between the normal members
    gapsHandeling.gapsInsertor(self.listLoadpaths)

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

