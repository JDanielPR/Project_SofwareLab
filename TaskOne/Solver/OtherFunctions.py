import HistoryComponent
import HistoryCrossComponent
import logging 

logger = logging.getLogger('OtherFunctions')

'''
Module Describtion:
This file groups all of the functions that are used some where in the
implementation of the OoD solver
'''

def indexor(listLoadpaths):
  '''Function assigns indeces to the components.

  Function assigns indeced to both the structural components and gaps according
  to their position in their respective loadpath from left to the right.
  '''
  for loadpath in listLoadpaths:
    index = 0
    for component in loadpath.listComponents:
      component.index = index
      index += 1


def restore_components_config(branch):
  '''Function restores history of the passed branch and its right components.

  Function restores the history of the passed branch and all of the components
  that are situated to the right of this branch. The branch here is the part of
  the possibilites tree that is deforming.
  '''
  
  for component in branch:
    
    historyLength = len(component.history)
    
    logger.debug("component {} is restoring its previous states"
                 .format(component.name))
    
    component.rightNode.position = component.history[
      historyLength - 1].rightNodePosition
    
    component.perminantlyBlockedDeformation = component.history[
      historyLength - 1].perminantlyBlockedDeformation
    
    component.temporarilyBlockedDeformation = component.history[
      historyLength - 1].temporarilyBlockedDeformation
    
    rightComponent = component.rightComponent
    
    while rightComponent != None:
      
      historyLength = len(rightComponent.history)
      
      logger.debug("component {} is restoring its previous states"
                   .format(rightComponent.name))
      
      rightComponent.rightNode.position = rightComponent.history[
        historyLength - 1].rightNodePosition
      
      rightComponent.perminantlyBlockedDeformation = rightComponent.history[
        historyLength - 1].perminantlyBlockedDeformation
      
      rightComponent.temporarilyBlockedDeformation = rightComponent.history[
        historyLength - 1].temporarilyBlockedDeformation
      
      rightComponent.history.remove(rightComponent.history[historyLength - 1])
      
      rightComponent = rightComponent.rightComponent
  
def store_component_config(component):
  '''Function stores the key attributes of component in its history list.

  Function that stores the key attributes of the component such as the right
  position of its right node, its attribute temporarilyBlockedDeformation and
  its attribute perminantlyBlockedDeformation. Therefore, while getting deeper
  in solution, these variables are stored for the moment when getting up in the
  tree again to find new possibilities for solutions
  '''
  logger.debug("parameters of the component {} are being stored as a history"
               .format(component.name))
    
  historyElement = HistoryComponent.HistoryComponent (
    component.rightNode.position,
    component.perminantlyBlockedDeformation,
    component.temporarilyBlockedDeformation)
    
  component.history.append(historyElement)
  
  print("member",component.name," history is")
  for i in component.history:
    print("state: ",i.perminantlyBlockedDeformation)

def restore_cross_components_config(listCorssComponents):
  '''Function restores the history of the passed list of cross-components

  '''
  logger.debug("Cross-components are restoring their previous states")
  
  for crossComponent in listCorssComponents:
    historyLength = len(crossComponent.history)
    
    crossComponent.noContNoElong = crossComponent.history[
      historyLength - 1].noContNoElong
    
    crossComponent.deformationStepIsValid = crossComponent.history[
      historyLength - 1].deformationStepIsValid
    
    crossComponent.failureCausingCrossMember = crossComponent.history[
      historyLength - 1].failureCausingCrossComponent
    
    crossComponent.history.remove(crossComponent.history[historyLength - 1])

def store_cross_component_config(crossComponent):
  '''Function stores the key attributes of cross-component in its history list.

  Functin that stores the attributes of the cross-components noContNoElong, the
  attribute deformationStepIsValud and the attribute failureCausingCrossCompon-
  ent. Therefore, while getting deeper in solution, these variables are stored
  for the moment when getting up in the tree again to find new possibilities f-
  or solutions
  '''
  logger.debug("parameters of cross-component are being stored as a history")
  
  historyElement = HistoryCrossComponent.HistoryCrossComponent (
    crossComponent.noContNoElong,
    crossComponent.deformationStepIsValid,
    crossComponent.failureCausingCrossComponent)
    
  crossComponent.history.append(historyElement)

def restore(branch, listLoadpaths, listCrossComponents):
  '''Function restores the history of components and all cross-components.

  Function restores the history of attribute of the passed branch, the right
  components to this branch and the list of cross-components.
  '''
  for member in branch:
    x = len(member.history)
    print(member.name)
    print("the value of x is: ",x)

  for comp in branch:
    print("components names is:",comp.name)
  for component in branch:
    
    historyLength = len(component.history)
    print("current component is:",component.name)
    if (component.perminantlyBlockedDeformation != component.history[
      historyLength - 1].perminantlyBlockedDeformation) :
      print("noComponentsNotDeformable have been decreased")
      listLoadpaths[
        component.leftNode.loadpathLevel
        ].decrease_noComponentsNotDeformable()
      print("noComponentsNotDeformable is",listLoadpaths[component.leftNode.loadpathLevel].noComponentsNotDeformable)
      
  restore_components_config(branch)
  restore_cross_components_config(listCrossComponents)

def get_deformation_nodes(branch):
  '''Function returns list of the nodes that are deforming their components.
  '''

  deformationNodes = []

  for component in branch:
    deformationNodes.append(component.rightNode)

  return deformationNodes

def deformation_amount_cross_components(
  defomationLeadingNodes,
  listCrossComponents):
  '''Function returns the amount of deformation based on cross-components.
  
  Deformation amount is calculated by the deformable length the affected cross-
  components have. Affected cross-components are those that will get deformed 
  due to the current deformation step.
  '''

  crossComponentsDeformationAmount = 100000 #some big value

  if listCrossComponents is not None:
    
    decidor = 0
    
    # "affectedCrossComponents" is a list contains cross-components that are 
    # going to be deformed due to the current deformation step
    affectedCrossComponents = []
    
    for crossComponent in listCrossComponents:
      for deformationNode in defomationLeadingNodes:
        firstNode = crossComponent.firstNode
        secondNode = crossComponent.secondNode
        if firstNode == deformationNode or secondNode == deformationNode:
          decidor += 1
      # If a cross-component to be affected by the deformation step, it needs to
      # have just one of its nodes as a defomationNode; therefore, the value of
      # decidor should be one
      if decidor == 1:
        affectedCrossComponents.append(crossComponent)

    for crossComponent in affectedCrossComponents:
      decidorValueRight = 0
      decidorValueLeft = 0
    
      for deformationNode in defomationLeadingNodes:
      
        if (crossComponent.firstNode.loadpathLevel
            == deformationNode.loadpathLevel and
            crossComponent.firstNode.position
            <= deformationNode.position):
          decidorValueRight += 1

        if (crossComponent.firstNode.loadpathLevel
            == deformationNode.loadpathLevel and
           crossComponent.firstNode.position
            >= deformationNode.position):
          decidorValueLeft +=1

      if decidorValueRight  == 1 and decidorValueLeft == 1:
        crossComponentsDeformationAmount = min(crossComponentsDeformationAmount,
                                              abs(crossComponent.firstNode.position 
                                                  - crossComponent.secondNode.position 
                                                  - crossComponent.rigidLength ) )

    logger.debug("deformation of the available cross members equal to {}"
                 .format(crossComponentsDeformationAmount))
    
  return crossComponentsDeformationAmount

