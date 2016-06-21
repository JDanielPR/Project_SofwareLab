import nextstep as ns
import itertools
import gapsHandeling

class structure():

  def __init__(self, listLPsObject):

    self.listLoadpaths = listLPsObject
    #self.listCrossMembers = listCrsMembs

  def solve(self):

    structureArray = []

    gapsHandeling.gapsInsertor(self.listLoadpaths)
    
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
    
    nstep = ns.nextstep(lpgroup,None,None)
