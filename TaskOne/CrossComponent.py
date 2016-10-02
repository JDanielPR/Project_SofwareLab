import logging
logger = logging.getLogger('CrossComponentLogger')

import otherFunctions as others

class CrossComponent():

  def __init__(self,
               leftNode, rightNode,
               deformableLength):

    self.leftNode = leftNode  # the first node is chosen as the one closest 
                              # to the barrier 
    self.rightNode = rightNode

# THIS CHANGES DURING DEFORMATION !!!
    self.deformableLength = deformableLength
    
    self.originalDiffOfNodes = self.leftNode.position - self.rightNode.position
    # means "original Difference Of Nodes". this number is always Negative
    self.noContNoElong = False # Mean "No Contraction No Elongation". if this 
                               # is True, then the member should not have any 
                               # relative motion between its two nodes anymore
    self.validToResume = 1
    self.failureCausingCrossMember = None

    #list where the history of the states of the cross component are stored
    self.history = [ ]

# this function checks the configuration of the crossMember after the carried 
# out branch of possibilitiesTree if this cofiguration violates the porposed 
# assumptions, then it will return False, otherwise True
  def check_new_cross_component_config(self):
    
    #store the state of the cross member
    others.storeCrossMembersConfig(self)

    logger.debug("a cross component is being examined against a deformation \
step")

    self.validToResume = 1

    currentDiffOfNodes = self.leftNode.position - self.rightNode.position
    # this should remain a value less than zero
    
    if self.noContNoElong == False:
      differenceCurrentAndOriginal = abs(self.originalDiffOfNodes) - \
                                     abs(currentDiffOfNodes)
      if differenceCurrentAndOriginal > self.deformableLength or \
         currentDiffOfNodes >= 0: # the second part of the if statement
                                  # condition refers to the fact that we may
                                  # have a flip over 
        self.validToResume = 0
        self.failureCausingCrossMember = self # becuase this cross member has
                                              # prevented the current
                                              # deformartion step from
                                              # progressing, it will be
                                              # classified as a failure
                                              # causing member
        logger.debug("a cross component has indicated that this deformation \
step has violated an assumption of flipping over or defoming more than \
allowed")

      if differenceCurrentAndOriginal == self.deformableLength:
        self.NoContNoElong = True
        logger.debug("a cross component has reached its deformation limit and \
is no longer allowed to deform")

    else:
      if abs(currentDiffOfNodes) != self.deformableLength:
        logger.debug("a cross component has indicated that this deformation \
step has violated an assumption of moving after finishing deforming")
        self.validToResume = 0
        self.failureCausingCrossMember = self # becuase this cross member has
                                              # prevented the current
                                              # deformartion step from
                                              # progressing, it will be
                                              # classified as a failure causing
                                              # member
