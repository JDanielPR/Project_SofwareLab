import logging
logger = logging.getLogger('CrossComponentLogger')

import otherFunctions as others

class CrossComponent():

  def __init__(self, nodeOne, nodeTwo, deformableLength):

    self.firstNode = nodeOne  #the first node is chosen as the one closest to the barrier 
    self.secondNode = nodeTwo
    self.deformableLength = deformableLength
    self.originalDiffOfNodes = self.firstNode.position - self.secondNode.position#Means "original Difference Of Nodes". this number is always Negative

    self.NoContNoElong = False  #Mean "No Contraction No Elongation". if this is True, then the member should not have any relative motion between its two nodes anymore
    self.validToResume = 1
    self.failureCausingCrossMember = None

    #list where the history of the states of the cross component are stored
    self.history = []


#this function checks the configuration of the crossMember after the carried out branch of possibilitiesTree
#if this cofiguration violates the porposed assumptions, then it will return False, otherwise True
  def checkNewCrossComponentConfig(self):
    
    #store the state of the cross member
    others.storeCrossMembersConfig(self)
    
    logger.debug("a cross component is being examined against a deformation step")

    self.validToResume = 1

    currentDiffOfNodes = self.firstNode.position - self.secondNode.position#this should remain a value less than zero
    
    if self.NoContNoElong == False:
      differenceCurrentAndOriginal = abs(self.originalDiffOfNodes)  -abs(currentDiffOfNodes)
      if differenceCurrentAndOriginal > self.deformableLength or currentDiffOfNodes >= 0:  #the second part of the if statement condition refers to the fact that we may have a flip over 
        self.validToResume = 0
        self.failureCausingCrossMember = self  #becuase this cross member has prevented the current deformartion step from progressing, it will be classified as a failure causing member
        logger.debug("a cross component has indicated that this deformation step has violated an assumption of flipping over or defoming more than allowed")

      if differenceCurrentAndOriginal == self.deformableLength:
        self.NoContNoElong = True
        logger.debug("a cross component has reached its deformation limit and is no longer allowed to deform")

    else:
      if abs(currentDiffOfNodes) != self.deformableLength:
        logger.debug("a cross component has indicated that this deformation step has violated an assumption of moving after finishing deforming")
        self.validToResume = 0
        self.failureCausingCrossMember = self  #becuase this cross member has prevented the current deformartion step from progressing, it will be classified as a failure causing member



