def gapsInsertor(listOfLoadpaths):

  #This function will take as an input the loadpaths that have been created from the xml. files
  #and it will insert gaps within these loadpaths; furthermore, it will set the gaps laying in the
  #front ON and the rest of the members within the same loadpath OFF

  #FIRST STEP: determine the minimum "x" value that any of the loadpaths start from
  minimumXcoord = 0
  temporaryValue = 0
  for i in listOfLoadpaths:
    if temporaryValue > i.listOfMembers[0].leftNode.pisition:  #here I assume that the xml. file will list the members in order
      minimumXcoord = temporaryValue

  #SECOND STEP: insert gaps whenever there is a dismatch in the "x" coordinate between two
  #adjacent members
  modifier = 0
  for i in listOfLoadpaths:
    loadpathCounter = 0
    for memberCounter in len(i.listOfMembers):
      if memberCounter< (len(i.listOfMembers)-1):#here we ensure that the loop will go untill the member before the last
        if i.listOfMembers[memberCounter+modifier].rightNode.position != i.listOfMembers[memberCounter+1+modifier].leftNode.position:  #here we compare between the positions of the right and left nodes
          gapsLeftNode = i.listOfMembers[memberCounter+modifier].rightNode.position
          gapsRightNode = i.listOfMembers[memberCounter+1+modifier].leftNode.position
          gapsName = 'gap'+str(loadpathCounter)+str(memberCounter)
          i.listOfMembers.insert(memberCounter , member(gapsLeftNode,gapsRightNode,1,gapsName,None,False) )
          modifier += 1
    loadpathCounter += 1

  #THIRD STEP: go through each loadpath, and insert a gap member in its front if it starts at
  #an "x" coordinate bigger than the minimumXcoord; furthermore, we turn off all of the other
  #members within the loadpath that has gotten a new gap at the front and keep this gap on
  counter = 0
  for i in listOfLoadpaths:
    if  i.listOfMembers[0].leftNode.pisition > minimumXcoord:
      firstStrcturalMember = i.listOfMembers[0].leftNode.pisition
      gapsName = 'gap'+str(counter)+str(0)  #gap(loadpath_index)(member_index)
      i.listOfMembers.insert(0,member(0,firstStrcturalMember,1,gapsName,None,False))
      
      for j in i:  #turn ON the gap that lies in the front and OFF for the rest of members
        if j.name != gapsName:
          j.changeState(False)

    else:  #if the current loadpath doesn't have a gap at the front
      for j in i:  #this loop will search for gaps in between, and it will turn them ON
        if j.structural == False:
          j.state = True
          for k in i:  #this loop will trun all of the other members OFF 
            if k.name != j.name:
              k.state = False
          break
          
    counter += 1

  #everythings now is done, and the structure has been modified with the all the gaps 



  
        
