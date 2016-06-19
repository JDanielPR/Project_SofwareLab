import logging
memberLogging = logging.getLogger('nextstep')

class member():

  def __init__(self, x, y, z, nome, lm, effectiveness=True,gapIndx = None):
    self.leftNode = x
    self.rightNode = y
    self.dLength = (self.calLength())*z
    self.length = self.calLength()
    self.name = nome
    self.leftMember = lm
    self.state = True
    self.rigidLength = (self.length)*(1-z)
    self.deformPossibility = True

    #new attribute introduced to account for gaps
    self.structural = effectiveness  #this will change to "False" if the member was a gap
    self.gapIndex = gapIndx  #index (position) of the gap with respect to the rest of the gaps within the loadpath
    
  def calLength(self):
    return abs(self.leftNode.position - self.rightNode.position)

  def deform(self,x):
    self.leftNode.changePosition (x)
    self.changeDeformLength(x)
    if self.leftMember != None:
      self.leftMember.transmotion(x)

  def changeDeformLength(self, change):
    self.dLength -= change

  def transmotion(self,x):
    memberLogging.debug("a motion has been transfered to an adjacent member")
    memberLogging.debug("the leftNode of the adjacent member has been moved by {}".format(x))
    self.leftNode.changePosition(x)
    if self.leftMember != None:  
      self.leftMember.transmotion(x)

  def changeState(self,switch):
    self.state = switch

  def canDeform(self, state):
    self.deformPossibility = state

  def addAdjacentMember(self, adjMem):
    self.leftMember = adjMem
