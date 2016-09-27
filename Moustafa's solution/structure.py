import nextstep as ns
import itertools
import gapsHandeling
import otherFunctions

class structure():

  def __init__(self, listLPsObject, listCrsMembs = None):

    self.listLoadpaths = listLPsObject
    self.listCrossMembers = listCrsMembs

  def solve(self):

    structureArray = []
    #this like addes gaps in between the normal members
    gapsHandeling.gapsInsertor(self.listLoadpaths)
    #this line addes indeces to the members (normal and gaps) according to their position with respect to the barreir in their correponding loadpaths
    otherFunctions.indexor(self.listLoadpaths) 
    
    for i in self.listLoadpaths .listOfLoadpaths:
      structureArray.append(i.listOfMembers)

    #visualization of the given structure
    counter = 0
    for i in structureArray:
      print('Loadpath #',counter)
      for j in i:
        print(j.name)
      print('-----')
      counter += 1
      
    lpgroup = list(itertools.product(*(structureArray)))

    #prints the motion possibilities
    for i in lpgroup:
      for j in i:
        print(j.name)
        print('\n')
      print('-------')
    
    nstep = ns.nextstep(lpgroup,None,None,self.listCrossMembers, self.listLoadpaths)
