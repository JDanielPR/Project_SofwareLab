import logging
import crossMemberClass

logger = logging.getLogger('deformingLogging')

def deforming(deformotion, decidor, localtree, counter, ledByNormalMember, localCrossMembsList, validToCrossMembers):
  if deformotion != 0.0 and decidor == len(localtree[counter]):
        
    count = 0  #determines the loadpath the following member belongs to
        
    for j in localtree[counter]:

      j.deform(deformotion)

      #since I have realized that the crossMembers list is UNCOUPLED with the localtree, I will move the nodes of the cross members here
      for i in localCrossMembsList:
        
        if i.firstNode.loadpathLevel == j.leftNode.loadpathLevel:
          if i.firstNode.position <= j.leftNode.position:
            logger.debug("cross member has moved its first Node by {}".format(deformotion))
            i.firstNode.position += deformotion

            
        if i.secondNode.loadpathLevel == j.leftNode.loadpathLevel:
          if i.secondNode.position <= j.leftNode.position:
            logger.debug("cross member has moved its second Node by {}".format(deformotion))
            i.secondNode.position += deformotion
         
      if j.calLength() == j.rigidLength:
        logger.debug("member {} has reached its maximum deformation length".format(j.name))
        if j.structural == True:
          j.changeState(False)
          j.canDeform(False)
          for k in localtree: #Switch all of the members along the loadpath containing member j on again
            if k[count].name != j.name:
              k[count].canDeform(True)
        else:  #here we know that this member was a gap, and we treat it in another way
          localtree = gapsHandeling.treatThisGap(j, localtree,count)
            
      else: ##further improvement to this method is to introduce a list the contains the tuple of members that cant deform together due to the deformation of the current crossMember
        logger.debug("member {} has NOT reached its maximum deformation length".format(j.name))
        if ledByNormalMember == True:
          j.canDeform(True) #member j will keep leading the deformation in its own loadpath
          for k in localtree: #Switch all of the members along the loadpath containing member j off so they dont deform untill member j is done
            if k[count].name != j.name:
              k[count].canDeform(False)
                 
        else:
          logger.debug("the procedure to deal with defomation led by crossMember has been called")
          for k in localtree:
            k[count].canDeform(True)
                
      count = count + 1

    #this part of the function is to determine whether this carried out deformation is valid with respect to the list of cross members
    for crossMemb in localCrossMembsList:
      crossMemb.checkNewCrossMembConfig()
      validToCrossMembers = validToCrossMembers + crossMemb.validToResume

    return validToCrossMembers

          
