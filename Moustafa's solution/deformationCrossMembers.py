import member
import node
import loadpath
import structure
import logging

logger = logging.getLogger('deformationCrossMembers')

def getDeformLeadNodes(elementTreeBranch):

  deformLeadNodes = []

  for i in elementTreeBranch:
    deformLeadNodes.append(i.leftNode)

  return deformLeadNodes


def deformAmountCrossMembers(deformLeadNodesList , crossMembersList):

  crossMembersDeformLength = 100000 #some big value

  if crossMembersList != None:
    for i in crossMembersList:
    
      decidorValueRight = 0
      decidorValueLeft = 0
    
      for j in deformLeadNodesList:
      
        if i.firstNode.loadpathLevel == j.loadpathLevel and i.firstNode.position <= j.position:
          decidorValueRight += 1
        if i.firstNode.loadpathLevel == j.loadpathLevel and i.firstNode.position >= j.position:
          decidorValueLeft +=1

      if decidorValueRight  == 1:  #the bounding limits here are 0 and 2 because it was assumed that a cross member can only have 2 nodes
        if decidorValueLeft  == 1:
          crossMembersDeformLength = min(crossMembersDeformLength , i.horizDefLength)

    logger.debug("deformation of the available cross members equal to {}".format(crossMembersDeformLength))
  return crossMembersDeformLength
