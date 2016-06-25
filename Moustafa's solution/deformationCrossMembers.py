def getDeformLeadNodes(elementTreeBranch):

  deformLeadNodes = []

  for i in elementTreeBranch:
    deformLeadNodes.append(i.leftNode.position)

  return deformLeadNodes


def deformAmountCrossMembers(deformLeadNodesList , crossMembersList):

  crossMembersDeformLength = 100000

  for i in crossMembersList:
    
    decidorValueRightNodes = 0
    
    for j in deformLeadNodeslist:
      
      if i.firstNode.loadpathLevel = j.loadpathLevel and i.firstNode.position >= j.position:
          decidorValueRightNodes += 1

      if i.leftNode.loadpathLevel = j.loadpathLevel and i.firstNode.position >= j.position:
          decidorValueRightNodes += 1

    if decidorValueRightNodes  = 0 or decidorValueRightNodes  = 2:
      crossMembersDeformLength = min(crossMembersDeformLength , i.horizDefLength)

  return crossMembersDeformLength
