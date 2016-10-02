import logging
logger = logging.getLogger('CrossComponentLogger')

import otherFunctions as others

class CrossComponent():
  '''
  This class stores the information related to a cross component
  and a method that checks whether a deformation step is valid
  with respect to this cross component
  '''

  def __init__(self,
               leftNode, rightNode,
               deformableLength):

    self.leftNode = leftNode  # the first node is chosen as the one closest 
                              # to the barrier 
    self.rightNode = rightNode

# THIS CHANGES DURING DEFORMATION !!!
    self.deformableLength = deformableLength
    self.originalDiffOfNodes = self.leftNode.position - self.rightNode.position
    self.noContNoElong = False 
    self.deformationStepIsValid = 1
    self.failureCausingCrossComponent = None

    #list where the history of the states of the cross component are stored
    self.history = [ ]

# this function checks the configuration of the crossMember after the carried 
# out branch of possibilitiesTree if this cofiguration violates the porposed 
# assumptions, then it will return False, otherwise True
  def check_new_cross_component_config(self):
    '''
    Function checks whether a defromation step is valid to the cross component
    '''
    
    #store the state of the cross member
    others.store_cross_component_config(self)

    logger.debug("a cross component is being examined against a deformation \
step")

    self.deformationStepIsValid = 1 #1 means True; 0 means False
    deformableLength = self.rigitNode.position - self.leftNode.position - self.rigidLength
    currentDiffOfNodes = self.leftNode.position - self.rightNode.position
    
    if self.noContNoElong == False:
      differenceCurrentAndOriginal = abs(self.originalDiffOfNodes) - \
                                     abs(currentDiffOfNodes)
      if differenceCurrentAndOriginal > deformableLength or \
         currentDiffOfNodes >= 0: # the second part of the if statement
                                  # condition refers to the fact that we may
                                  # have a flip over 
        self.deformationStepIsValid = 0
        self.failureCausingCrossComponent = self 
        logger.debug("a cross component has indicated that this deformation \
step has violated an assumption of flipping over or defoming more than \
allowed")

      if differenceCurrentAndOriginal == deformableLength:
        self.NoContNoElong = True
        logger.debug("a cross component has reached its deformation limit and \
is no longer allowed to deform")

    else:
      if abs(currentDiffOfNodes) != deformableLength:
        logger.debug("a cross component has indicated that this deformation \
step has violated an assumption of moving after finishing deforming")
        self.deformationStepIsValid = 0
        self.failureCausingCrossMember = self 
