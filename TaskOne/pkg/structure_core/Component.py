import logging

logger = logging.getLogger('component')
logging.basicConfig(level=logging.DEBUG)

class Component():
  '''
  Component class contains all of the information
  related to both structural and gap components
  and the methods that act upon these attributes
  '''
  def __init__(self,
               leftNode, rightNode,
               rigidLength,
               componentsName,
               rightComponent = None,
               isStructural=True,
               gapIndex = None):
    
    self.name = componentsName
    self.leftNode = leftNode
    self.rightNode = rightNode
    self.length = self.calc_length()
    self.rigidLength = rigidLength
    self.perminantlyBlockedDefromation = True 
    self.temporarilyBlockedDeformation = True 
    self.isStructural = isStructural  
    self.gapIndex = gapIndex  
    self.history = [ ]
    self.componentIndex = 0 
    self.rightComponent = None

  def __repr__(self):
    return self.name

  def calc_length(self):
    return abs(self.leftNode.position - self.rightNode.position)

  def deformable_length(self):
    return self.calc_length() - self.rigidLength

  def deform(self, deformationStep, savers):
    '''
    Function deforms component and transfers motion to next.
    This function stores first the states of the component before
    defromation.Then it deforms the component, and finally
    transfers this movement to its right member if it exists
    by calling the function propagate()
    '''
    # storing the current configuration before defroming the member
    logger.debug("component {} has deformed with amount {}"
                 .format(self.name,deformationStep))
    self.rightNode.change_position(deformationStep)
    if self.rightComponent:
      self.rightComponent.propagate(deformationStep, savers)

    # save
    for saver in savers:
      saver.save(self, 'd', deformationStep)
      
  def moves(self, list_of_nodes):
    return any(node.loadpathLevel == self.leftNode.loadpathLevel
               and
               node.position <= self.leftNode.position
               for node in list_of_nodes)
    
    
  def propagate(self, deformationStep, savers):
    '''
    Function moves next component then transfers motion to next.
    This function first stores the states of the adjacent component
    on the right, then it transfers the motion to it. At the end, it
    transfers again the same motion to the adjacent component
    if it exists
    '''
    # storing the current configuration before deforming the left member
    self.rightNode.change_position(deformationStep)
    logger.debug("a motion transfered to component {}"
                 .format(self.name))
    if self.rightComponent:
      self.rightComponent.propagate(deformationStep, savers)

    # save
    for saver in savers:
      saver.save(self, 'm', deformationStep)

  def change_perminantlyBlockedDefromation(self, newValue):
    '''
    Function changes the attribute perminantlyBlockedDefromation.
    '''
    logger.debug("component {} changed erminantlyBlockedDefromation from {} \
to {}".format(self.name, self.perminantlyBlockedDefromation, newValue))
    self.erminantlyBlockedDefromation = newValue

  def change_temporarilyBlockedDeformation(self, newValue):
    '''
    Function changes the attribute temporarilyBlockedDeformation.
    '''
    logger.debug("component {} changed temporarilyBlockedDeformation from {} \
to {}".format(self.name, self.temporarilyBlockedDeformation,newValue))
    self.temporarilyBlockedDeformation = newValue

  def change_gap_index(self,newGapIndex):

    self.gapIndex = newGapIndex
