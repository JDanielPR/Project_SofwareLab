import logging
logger = logging.getLogger('crossMemberClassLogger')

import otherFunctions as others

class crossMember():

  def __init__(self, nodeOne, nodeTwo, defLength):

    self.firstNode = nodeOne  #the first node is chosen as the one closest to the barrier 
    self.secondNode = nodeTwo
    self.horizDefLength = defLength
    self.originalHorizDiffOfNodes = self.firstNode.position - self.secondNode.position#this number is always Negative

    self.NoContNoElong = False  #if this is True, then the member should not have any relative motion between its two nodes
    self.validToResume = 1
    self.failureCausingCrossMember = None

    #History definition of the crossMember
    self.history = []


#this function checks the configuration of the crossMember after the carried out branch of elementTree
#if this cofiguration violates our assumptions, then it will return False, otherwise True
  def checkNewCrossMembConfig(self):
    
    #store the state of the cross member
    others.storeCrossMembersConfig([self])
    
    logger.debug("a cross member is being examined against a deformation step")

    self.validToResume = 1

    CurrentHorizDiffOfNodes = self.firstNode.position - self.secondNode.position#this should remain a value less than zero
    print('CurrentHorizDiffOfNodes',CurrentHorizDiffOfNodes)
    
    if self.NoContNoElong == False:
      diffCurrentAndOriginal = abs(self.originalHorizDiffOfNodes)  -abs(CurrentHorizDiffOfNodes)
      if diffCurrentAndOriginal > self.horizDefLength or CurrentHorizDiffOfNodes >= 0:  #the second part of the if statement condition refers to the fact that we may have a flip over 
        self.validToResume = 0
        self.failureCausingCrossMember = self  #becuase this cross member has prevented the current deformartion step from progressing, it will be classified as a failure causing member
        logger.debug("a cross member has indicated that this deformation step has violated an assumption related to it (flipping over or defoming more than allowed)")

      if diffCurrentAndOriginal == self.horizDefLength:
        self.NoContNoElong = True
        logger.debug("a cross member has reached its deformation limit and is no longer allowed to deform")

    else:
      if abs(CurrentHorizDiffOfNodes) != self.horizDefLength:
        logger.debug("a cross member has indicated that this deformation step has violated an assumption related to it (moving after finishing deforming)")
        self.validToResume = 0
        self.failureCausingCrossMember = self  #becuase this cross member has prevented the current deformartion step from progressing, it will be classified as a failure causing member



