import logging
logger = logging.getLogger('member')
import otherFunctions as others

class member():

  def __init__(self, x, y, z, nome, lm,loadpathLvl, effectiveness=True,gapIndx = None):
    self.memberIndex = 0
    self.leftNode = x
    self.rightNode = y
    self.dLength = (self.calLength())*z
    self.length = self.calLength()
    self.name = nome
    self.leftMember = lm
    self.state = True
    self.rigidLength = (self.length)*(1-z)
    self.deformPossibility = True

    #assigning the loadpathLevel to the nodes
    self.leftNode.loadpathLevel = loadpathLvl
    self.rightNode.loadpathLevel = loadpathLvl

    #new attribute introduced to account for gaps
    self.structural = effectiveness  #this will change to "False" if the member was a gap
    self.gapIndex = gapIndx  #index (position) of the gap with respect to the rest of the gaps within the loadpath

    #History definition of the member
    self.history = []
    
  def calLength(self):
    return abs(self.leftNode.position - self.rightNode.position)

  def deform(self,x):
    #storing the current configuration before defroming the member
    others.storeMembersConfig([self])
    
    logger.debug("member {} has deformed with amount {}".format(self.name,x))
    self.leftNode.changePosition (x)
    self.changeDeformLength(x)
    if self.leftMember != None:
      logger.debug("a motion has been transfered from member {} to its adjacent member {}".format(self.name,self.leftMember.name))
      self.transmotion(x)

  def changeDeformLength(self, change):
    logger.debug("member {} has changed its deformable legnth by {}".format(self.name,change))
    self.dLength -= change

  def transmotion(self,x):
    #storing the current configuration before deforming the left member
    others.storeMembersConfig([self.leftMember])
    
    self.leftMember.leftNode.changePosition(x)
    logger.debug("a motion has been transfered from member {} to its adjacent member {}".format(self.name,self.leftMember.name))
    if self.leftMember.leftMember != None:
      self.leftMember.transmotion(x)

  def changeState(self,switch):
    logger.debug("member {} has changed its state state to {}".format(self.name,switch))
    self.state = switch

  def canDeform(self, state):
    logger.debug("member {} has changed its deformPossibility to {}".format(self.name,state))
    self.deformPossibility = state

  def addAdjacentMember(self, adjMem):
    self.leftMember = adjMem
