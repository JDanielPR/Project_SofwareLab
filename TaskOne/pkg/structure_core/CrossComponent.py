import logging
logger = logging.getLogger('CrossComponentLogger')

class CrossComponent():
  '''
  This class stores the information related to a cross component
  and a method that checks whether a deformation step is valid
  with respect to this cross component
  '''

  def __init__(self,
               name,
               leftNode, rightNode,
               rigidLength):
    # the first node is chosen as the one closer to the barrier
    assert leftNode.position < rightNode.position
    self.name = name
    self.leftNode = leftNode 
    self.rightNode = rightNode

# THIS CHANGES DURING DEFORMATION !!!
    self.rigidLength = rigidLength
    self.originalDiffOfNodes = self.leftNode.position - self.rightNode.position
    self.noContNoElong = False 
    self.deformationStepIsValid = 1
    self.failureCausingCrossComponent = None

    #list where the history of the states of the cross component are stored
    self.history = [ ]

# this function checks the configuration of the crossMember after the carried 
# out branch of possibilitiesTree if this cofiguration violates the porposed 
# assumptions, then it will return False, otherwise True

  def left_deforms(self, list_of_nodes):
    """True if the given deformation leading nodes would move the leftNode."""
    return any(node.loadpathLevel == self.leftNode.loadpathLevel 
               and 
               node.position <= self.leftNode.position 
               for node in list_of_nodes)

  def right_deforms(self, list_of_nodes):
    """True if the given deformation leading nodes would move the rightNode."""
    return any(node.loadpathLevel == self.rightNode.loadpathLevel 
               and 
               node.position <= self.rightNode.position 
               for node in list_of_nodes)
  
  def length(self):
    """Returns the length in x direction of the crossComponent."""
    return self.rightNode.position - self.leftNode.position
  
  def deformable_length(self):
    """Returns the deformable length in x direction of the crossComponent."""
    return self.length() - self.rigidLength
    
  def check_new_cross_component_config(self):
    '''
    Function checks whether a defromation step is valid to the cross component
    '''
    
    #store the state of the cross member

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
