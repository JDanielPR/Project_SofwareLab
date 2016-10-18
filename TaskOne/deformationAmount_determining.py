
def determine_deformation_amount( possibilitiesTuple , listCrossComponents ):

   # Calculation of the motion to be carried out from the deformable length
   # of components
   # First, assume some big value to the initial deformation amount
    deformationAmount = 10000.00000

    # Loop over the components in the passed possibilities tuple to determine
    # the minimum amount of deformation amount
    for component in branch:
      if (component.calc_length() - component.rigidLength) < deformationAmount:
        deformationAmount = component.calc_length() - component.rigidLength
      else:
        pass
      deformationAmount = round(deformationAmount,1)
        
    #Get the nodes that are leading the deformation
    deformationLeadingNodes = get_deformation_nodes(branch)
        
    # Calculate the deformation that is allowed by the whole deforming
    # cross-components
    deformationAmountCrossComponents = (
      deformation_amount_cross_components(
        deformationLeadingNodes,
        self.listCrossComponents
        )
      )

  if deformationAmountCrossComponents < deformationAmount:
    deformationAmount = deformationAmountCrossComponents
  else:
    pass

  return deformationAmount

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
    
  # "affectedCrossComponents" is a list contains cross-components that are 
  # going to be deformed due to the current deformation step
  affectedCrossComponents = []
  for crossComponent in listCrossComponents:
    toTheRight = 0
    toTheLeft = 0

    for deformationNode in defomationLeadingNodes:
      crossComponentNode = None
      #everything to the right of the deformationNode is moving, and everything to the left is not moving
      #if the cross component has one node in the moving side and another node in the static side, then we have to include it in the list of a affected cross components
      loadpathLevel = deformationNode.loadpathLevel
      firstNode = crossComponent.firstNode
      secondNode = crossComponent.secondNode
        
      if firstNode.loadpathLevel == loadpathLevel:
        crossComponentNode = firstNode
      if secondNode.loadpathLevel == loadpathLevel:
        crossComponentNode = secondNode
      if firstNode.loadpathLevel != loadpathLevel and secondNode.loadpathLevel != loadpathLevel:
        crossComponentNode = None
      if crossComponentNode != None:
        if crossComponentNode.position >= deformationNode.position:
          toTheRight += 1
        else:
          toTheLeft += 1
      else:
        toTheRight = 0
        toTheLeft = 0
          
    if toTheRight == 1 and toTheLeft == 1:
      affectedCrossComponents.append(crossComponent)

  for crossComponent in affectedCrossComponents:
    crossComponentsDeformationAmount = min(
      crossComponentsDeformationAmount , abs(
        crossComponent.firstNode.position - crossComponent.secondNode.position - crossComponent.rigidLength
        )
      )

  logger.debug("deformation of the available cross members equal to {}".format(
    crossComponentsDeformationAmount))
    
  return crossComponentsDeformationAmount
