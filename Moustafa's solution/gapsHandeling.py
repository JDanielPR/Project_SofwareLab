import logging
import node
import member

gapsHandelingLogger = logging.getLogger('gapsHandeling')
logging.basicConfig(level=logging.DEBUG)


def gapsInsertor(listLPs):

  gapsHandelingLogger.debug('stepped inside the "gapsInsertor" function')

  #This function will take as an input the loadpaths that have been created from the xml. files
  #and it will insert gaps within these loadpaths; furthermore, it will set the gaps laying in the
  #front ON and the rest of the members within the same loadpath OFF

  #FIRST STEP: determine the minimum "x" value that any of the loadpaths start from
  minimumXcoord = 100000
  for i in listLPs.listOfLoadpaths:
    if minimumXcoord > i.listOfMembers[0].leftNode.position:  #here I assume that the xml. file will list the members in order
      minimumXcoord = i.listOfMembers[0].leftNode.position
  gapsHandelingLogger.debug('first step has been finished')

  #SECOND STEP: insert gaps whenever there is a dismatch in the "x" coordinate between two
  #adjacent members
  modifier = 0
  loadpathCounter = 0
  for i in listLPs.listOfLoadpaths:
    for memberCounter in range(len(i.listOfMembers)-1):

      if i.listOfMembers[memberCounter+modifier].rightNode.position != i.listOfMembers[memberCounter+1+modifier].leftNode.position:  #here we compare between the positions of the right and left nodes
        gapsLeftNode = i.listOfMembers[memberCounter+modifier].rightNode
        gapsRightNode = i.listOfMembers[memberCounter+1+modifier].leftNode
        gapsName = 'gap'+str(loadpathCounter+1)+str(1+modifier)
        gapLeftMember = i.listOfMembers[memberCounter+modifier]
        i.listOfMembers.insert(memberCounter+modifier+1 , member.member(gapsLeftNode,gapsRightNode,1,gapsName,gapLeftMember,False,0) )  #gapIndex was set to zero just because I want to give a numerical value
        i.listOfMembers[memberCounter+2+modifier].addAdjacentMember(i.listOfMembers[memberCounter+1+modifier])  #make the created gap as a leftMember to its adjacent structural member to the right
        modifier += 1
        
    loadpathCounter += 1
    modifier = 0
  gapsHandelingLogger.debug('second step has been finished')

  #THIRD STEP: go through each loadpath, and insert a gap member in its front if it starts at
  #an "x" coordinate bigger than the minimumXcoord; furthermore, we turn off all of the other
  #members within the loadpath that has gotten a new gap at the front and keep this gap on
  counter = 0
  for i in listLPs.listOfLoadpaths:
    
    if  i.listOfMembers[0].leftNode.position > minimumXcoord:
      frontalGapLeftNode = node.node(0)
      frontalGapRightNode = i.listOfMembers[0].leftNode
      gapsName = 'gap'+str(counter+1)+str(1)  #gap(loadpath_index)(member_index)
      i.listOfMembers.insert(0,member.member(frontalGapLeftNode,frontalGapRightNode,1,gapsName,None,False,0))
      gapsHandelingLogger.debug('a new gap in the front of loadpath #{} has been created'.format(counter))
      
      for j in i.listOfMembers:  #turn ON the gap that lies in the front and OFF for the rest of members
        if j.name != gapsName:
          j.canDeform(False)

    else:  #if the current loadpath doesn't have a gap at the front
      for j in i.listOfMembers:  #this loop will search for gaps in between, and it will turn the first of them ON
        if j.structural == False:
          j.deformPossibility = True
          for k in i.listOfMembers:  #this loop will turn all of the other members OFF 
            if k.name != j.name:
              k.deformPossibility = False
          break
          
    counter += 1
  gapsHandelingLogger.debug('third step has been finished')

  #FOURTH STEP: give the gaps their indices
  counter = 0
  for i in listLPs.listOfLoadpaths:
    for j in i.listOfMembers:
      if j.structural == False:
        j.gapIndex = counter
        counter += 1
    counter = 0

  #everythings now is done, and the structure has been modified with the all the gaps

#finction that turns the gap that has completely closed OFF, and turns the next one ON (if found)
#;in addition, it turns all of the other members OFF
def treatThisGap(currentGap, listLPs):

  currentGap.changeState(False)  #change the state of the current gap to False for elimination
  currentGap.canDeform(False) #this can cant deform temporarly any more

  isThereNextGap = False

  nextGapIndex = currentGap.gapIndex + 1  #index of the next gap (if available)

  for memb in listLPs[memb.leftNode.loadpathIndex]:
    if memb.structural == False:
      if memb.gapindex == nextGapIndex:
        memb.canDeform(True)
        isThereNextGap = True
      else:
        memb.canDeform(False)

  if isThereNextGap == False:
    for memb in listLPs[memb.leftNode.loadpathIndex]:  #if no more gaps are there after the currentGap, then perform this
      if memb.index != currentGap.index:
        memb.canDeform(True)

  return localtree        
