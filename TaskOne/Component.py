import logging
import otherFunctions as others

logger = logging.getLogger('component')
logging.basicConfig(level=logging.DEBUG)

class Component():

  def __init__(self, leftNode, rightNode, rigidLength, componentsName, rightComponent, loadpathLevel, effectiveness=True,gapIndex = None):
    self.memberIndex = 0
    self.leftNode = leftNode
    self.rightNode = rightNode
    self.rigidLength = rigidLength
    self.length = self.calLength()
    self.name = componentsName
    self.rightComponent = rightComponent
    #Component's state defines the ability of the component to deform, so when the component reaches its deformation limit, its state changes to False
    self.state = True
    #This attribute changes to False when a component is not allowed to deform due to the presence of another component along the same loadpath that has not finished its deformation
    self.deformPossibility = True

    #assigning the loadpathLevel to the nodes
    self.leftNode.loadpathLevel = loadpathLevel
    self.rightNode.loadpathLevel = loadpathLevel

    #Attribute introduced to account for gaps
    self.structural = effectiveness  #self.structural = True if the component was  a structural element and self.structural = False if the component was a gap
    self.gapIndex = gapIndx  #index (position) of the gap with respect to the rest of the gaps within the loadpath (ex. 1,2,3,...)

    #History list where all of the previous states of the component are going to be saved
    self.history = []
    
  def calLength(self):
    return abs(self.leftNode.position - self.rightNode.position)

  def deform(self,deformationStep):
    #storing the current configuration before defroming the member
    others.storeMembersConfig([self])
    logger.debug("component {} has deformed with amount {}".format(self.name,deformationStep))
    self.rightNode.changePosition (x)
    if self.rightComponent != None:
      logger.debug("a motion has been transfered from component {} to its adjacent component {}".format(self.name,self.rightComponent.name))
      self.propagate(x)

  def propagate(self,deformationStep):
    #storing the current configuration before deforming the left member
    others.storeMembersConfig([self.rightComponent])
    self.rightComponent.rightNode.changePosition(x)
    logger.debug("a motion has been transfered from member {} to its adjacent member {}".format(self.name,self.leftMember.name))
    if self.rightComponent.rightComponent != None:
      self.rightComponent.propagate(deforationStep)

  def changeState(self,newState):
    logger.debug("member {} has changed its state from {} to {}".format(self.name, self.state, newState))
    self.state = newState

  def canDeform(self, newDeformPossibility):
    logger.debug("member {} has changed its deformPossibility from {} to {}".format(self.name, self.deformPossibility, newDeformPossibility))
    self.deformPossibility = newDeformPossibility
