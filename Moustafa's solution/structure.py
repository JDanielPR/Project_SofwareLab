import nextstep
import itertools
import gapsHandeling
import otherFunctions

'''
Structure class groups all of the nodes, member, cross members, and gaps all together in a single entity
'''

class structure():

  def __init__(self, listLoadpathsObject, counter,listCrossMembers = None):

    self.listLoadpaths = listLoadpathsObject
    self.listCrossMembers = listCrossMembers
    self.counter = counter

  def solve(self):

    #this line adds gaps in between the normal members
    gapsHandeling.gapsInsertor(self.listLoadpaths)

    #this line adds indexes to the members (normal and gaps) according to their position with respect to the barrier in their corresponding loadpaths
    otherFunctions.indexor(self.listLoadpaths) 

    #add all of the loadpaths to a list called "structure array" for the sake of the possibilitiesTree generation
    structureArray = []
    for i in self.listLoadpaths .listOfLoadpaths:
      structureArray.append(i.listOfMembers)

    #generate the possibilitiesTree
    possibilitiesTree = list(itertools.product(*structureArray))

    #initiate the solution sequence of the strcuture starting from the created possiblitiesTree
    initializationStep = nextstep.nextstep(possibilitiesTree, None, None, self.listCrossMembers, self.listLoadpaths,self.counter)


'''
    #visualization of the given structure
    counter = 0
    for i in structureArray:
      print('Loadpath #',counter)
      for j in i:
        print(j.name)
      print('-----')
      counter += 1
'''
'''
    #prints the motion possibilities
    for i in lpgroup:
      for j in i:
        print(j.name)
        print('\n')
      print('-------')
'''

