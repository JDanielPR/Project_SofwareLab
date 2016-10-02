import logging
import otherFunctions as others

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
               loadpathLevel,
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

  def calc_length(self):
    return abs(self.leftNode.position - self.rightNode.position)

  def deform(self,deformationStep):
    '''
    Function deforms component and transfers motion to next.
    This function stores first the states of the component before
    defromation.Then it deforms the component, and finally
    transfers this movement to its right member if it exists
    by calling the function propagate()
    '''
    # storing the current configuration before defroming the member
    others.storeMembersConfig(self)
    logger.debug("component {} has deformed with amount {}"
                 .format(self.name,deformationStep))
    self.rightNode.changePosition(x)
    if self.rightComponent != None:
      logger.debug("a motion transfered from component {} to component {}"
                   .format(self.name,self.rightComponent.name))
      self.propagate(x)

  def propagate(self,deformationStep):
    '''
    Function moves next component then transfers motion to next.
    This function first stores the states of the adjacent component
    on the right, then it transfers the motion to it. At the end, it
    transfers again the same motion to the adjacent component
    if it exists
    '''
    # storing the current configuration before deforming the left member
    others.storeMembersConfig(self.rightComponent)
    self.rightComponent.rightNode.changePosition(x)
    logger.debug("a motion has been transfered from member {} to
                 its adjacent \member {}".format(self.name, self.leftMember.name))
    if self.rightComponent.rightComponent != None:
      self.rightComponent.propagate(deforationStep)

  def change_perminantlyBlockedDefromation(self,newValue):
  '''
  Function changes the attribute perminantlyBlockedDefromation.
  '''
    logger.debug("component {} changed erminantlyBlockedDefromation from {} to {}"
                 .format(self.name, self.perminantlyBlockedDefromation, newValue))
    self.erminantlyBlockedDefromation = newValue

  def change_temporarilyBlockedDeformation(self, newValue):
  '''
  Function changes the attribute temporarilyBlockedDeformation.
  '''
    logger.debug("component {} changed temporarilyBlockedDeformation from {} to {}"
                 .format(self.name, self.temporarilyBlockedDeformation,newValue))
    self.temporarilyBlockedDeformation = newValue
