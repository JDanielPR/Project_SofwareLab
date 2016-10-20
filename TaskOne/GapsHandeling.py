import logging
from structure_core import Node, Component

gapsHandelingLogger = logging.getLogger('gapsHandeling')
logging.basicConfig(level=logging.DEBUG)


def gapsInsertor(listOfLoadpaths):
  '''Function inserts gaps within the loadpaths

  This function will take as an input the loadpaths that have been created from
  the xml file, and it will insert gaps within these loadpaths; furthermore, it
  will set the gap's attribute temporarilyBlockedDeformation laying in the front
  if it exists True and the rest of the components and gaps' same attribute 
  within the same loadpath False
  '''
  gapsHandelingLogger.debug('Stepped inside the "gapsInsertor" function')

  # First step is to determine the maximum x-coordinate that any of the
  # loadpaths start from
  
  minimumX = 100000
  for loadpath in listOfLoadpaths:
    if minimumX > loadpath.listComponents[0].leftNode.position:
      minimumX = loadpath.listComponents[0].leftNode.position
  gapsHandelingLogger.debug('First step has been finished')

  # Second step is to insert gaps wherever there is a dismatch in the  
  # x-coordinate between two adjacent component

  # Loop over all of the loadpaths
  for loadpath in listOfLoadpaths:
    # gapsCounter increases whenever new gap is added
    gapsCounter = 0

    # Loop over all of the components within a loadpath
    for componentCounter in range(len(loadpath.listComponents)-1):
      
      # rightNode is meant to be the node that bounds the current component
      # the componentCounter determines to the right
      rightNodePosition = (loadpath.listComponents
                           [componentCounter+gapsCounter].rightNode.position)

      # leftNode is meant to be the node that bounds the right component to
      # the current component determined by componentCounter to the left
      leftNodePosition = (loadpath.listComponents
                          [componentCounter+1+gapsCounter].leftNode.position)

      # If there is a dismatch in the x-coordinate between the rightNode and
      # the leftNode, then perform this
      if rightNodePosition != leftNodePosition:

        # Define the newly created gap's left node, which is the same node
        # of the currently looped over component's right node
        gapLeftNode = loadpath.listComponents[
          componentCounter+gapsCounter].rightNode

        # Define the newly created gap's right node, which is the same node
        # of the right component of the currently looped over component's
        # left node
        gapRightNode = loadpath.listComponents[
          componentCounter+1+gapsCounter].leftNode

        # Define the newly created gap's name
        gapName = 'gap'+str(gapLeftNode.loadpathLevel)+str(gapsCounter+1)

        # Define the newly created gap's adjacent component to the right
        gapRightComponent = loadpath.listComponents[
          componentCounter+1 +gapsCounter]

        # Create the new gap
        loadpath.listComponents.insert (
          (componentCounter + gapsCounter + 1),
          Component.Component (
            gapLeftNode,
            gapRightNode,
            0,
            gapName,
            gapRightComponent,
            False,
            0)
          )
        
        # Make the newly created gap as a rightComponent to its adjacent
        # structural component to the left
        loadpath.listComponents [
          componentCounter+gapsCounter
          ].add_rightComponent (
          loadpath.listComponents[componentCounter+1+gapsCounter]
          )
        
        gapsCounter += 1
        
  gapsHandelingLogger.debug('second step has been finished')

  # Third step involves going through each loadpath, and insert a gap component
  # in the barrier side if the loadpath starts at an x-coordinate less than the
  # maximumX; furthermore, it will switch the attribute
  # temporarilyBlockedDeformation of all  other components within the loadpath
  # that has gotten a new gap at the front to True and this gap's to False

  # Loop over all of the loadpaths 
  for loadpath in listOfLoadpaths:

    # Define the first node in the currently looped on loadpath as leftNode
    leftNode = loadpath.listComponents[0].leftNode

    # If this leftNode lies to the right of the minimum x-coordinate, then
    # perform this
    if  leftNode.position > minimumX:

      # Define the newly created frontal gap's right component, which is the first
      # component the loadpath used to have
      gapsRightComponent = loadpath.listComponents[0]

      # Define the newly created frontal gap's right node, which is the same as
      # the previously defined leftNode
      frontalGapRightNode = leftNode

      # Define the newly created frontal gap's left node, which is the same as
      # its right component's left node
      frontalGapLeftNode = Node.Node(minimumX, leftNode.loadpathLevel)

      # Define the newly created gap's name
      gapsName = 'gap'+str(leftNode.loadpathLevel)+'front'  

      # Create the new frontal gap
      loadpath.listComponents.insert (
        0,
        Component.Component (
          frontalGapLeftNode,
          frontalGapRightNode,
          0,
          gapsName,
          gapsRightComponent,
          False,
          0))

      gapsHandelingLogger.debug(
        'a new gap in the front of loadpath {} has been created'.format(
          leftNode.loadpathLevel)
        )
      
      # Switch the newly create frontal gap's attribute
      # temporarilyBlockedDeformation to True and all of the other components'
      # to False
      #for componentCounter in range(len(loadpath.listComponents)-1):
      for component in loadpath.listComponents:
        #if componentCounter == 0:
        if component.name == 'gap'+str(component.leftNode.loadpathLevel)+'front':
          pass
        else:
         # loadpath.listComponents[
         #   componentCounter].change_temporarilyBlockedDeformation(False)
         component.change_temporarilyBlockedDeformation(False)

    # If the current loadpath will not be having a gap at the front, then this
    # loop will search for gaps in between, and it will turn the attribute
    # temporarilyBlockedDeformation of the first gap to find to True and the
    # rest of the component's to False
    else:  
      for component in loadpath.listComponents:  
        if component.isStructural is False:
          component.change_temporarilyBlockedDeformation(True)
          for otherComponent in loadpath.listComponents:  
            if otherComponent.name != component.name:
              otherComponent.change_temporarilyBlockedDeformation(False)
          break
          
  gapsHandelingLogger.debug('third step has been finished')

  # Forth step involves giving indeces to the gaps depending on their order
  # from right to left
  gapIndex = 0
  for loadpath in listOfLoadpaths:
    for component in loadpath.listComponents:
      if component.isStructural is False:
        component.change_gap_index(gapIndex)
        gapIndex += 1
    gapIndex = 0

  # Everythings related to setting up the gaps is now done
    
#finction that turns the gap that has completely closed OFF, and turns the next one ON (if found)
#;in addition, it turns all of the other members OFF
def treat_this_gap(currentGap, listLoadpaths):
  '''Function deals with the deforming component if it was a gap

  makes the current Gap not to defrom anymore and gives defromation ability to
  the next. Function that turns the gap that has completely closed Off, and turns the next
  one On (if found); in addition, it turns all of the other members Off of there was
  another gap, and On if there wasn't
  '''
  #change the state of the current gap to False for elimination
  currentGap.change_perminantlyBlockedDeformation(False)
  #this gap cant deform temporarly any more
  currentGap.change_temporarilyBlockedDeformation(False) 

  isThereNextGap = False
  
  #index of the next gap (if available)
  nextGapIndex = (currentGap.gapIndex) + 1  

  for component in listLoadpaths[currentGap.leftNode.loadpathLevel].listComponents:
    if component.isStructural is False:
      if component.gapIndex == nextGapIndex:
        component.change_temporarilyBlockedDeformation(True)
        #component.change_perminantlyBlockedDeformation(True)
        isThereNextGap = True
      else:
         component.change_temporarilyBlockedDeformation(False)

  #if no more gaps are there after the currentGap, then perform this
  if isThereNextGap is False:
    for component in listLoadpaths[currentGap.leftNode.loadpathLevel].listComponents :
      if component.componentIndex != currentGap.componentIndex:
        component.change_temporarilyBlockedDeformation(True)
      
    
