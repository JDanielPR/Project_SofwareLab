import nextstep as ns
import itertools 

class structure():

  def __init__(self, crossMemberObject):

    self.listLoadpaths = []
    self.listCrossMembers = crossMemberObject

  def solve(self):
    
    lpgroup = list(itertools.product(*(self.listLoadpaths)))

    #prints the motion possibilities
    for i in lpgroup:
      for j in i:
        print(j.name)
        print('\n')
    
    nstep = ns.nextstep(lpgroup,None,None)
